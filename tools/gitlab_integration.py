"""
GitLab Integration for Oracle Log Analyzer

Provides secure access to GitLab repositories for code analysis.
Integrates with LangChain agents to fetch and analyze code for better troubleshooting.
"""

import json
import base64
import requests
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from urllib.parse import quote_plus
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

from config import config

class GitLabClient:
    """Secure GitLab API client for code access"""
    
    def __init__(self):
        # Get GitLab configuration from environment
        self.gitlab_url = getattr(config.app, 'gitlab_url', None)
        self.gitlab_token = getattr(config.app, 'gitlab_token', None)
        self.gitlab_project_id = getattr(config.app, 'gitlab_project_id', None)
        
        # Set up headers for API calls
        self.headers = {
            "PRIVATE-TOKEN": self.gitlab_token if self.gitlab_token else None,
            "Content-Type": "application/json"
        }
        
        # Remove None headers
        self.headers = {k: v for k, v in self.headers.items() if v is not None}
        
        # API endpoints
        self.api_base = f"{self.gitlab_url}/api/v4" if self.gitlab_url else None
        
        logger.info(f"GitLab client initialized - URL: {self.gitlab_url}")
    
    def is_configured(self) -> bool:
        """Check if GitLab is properly configured"""
        return all([
            self.gitlab_url,
            self.gitlab_token,
            self.gitlab_project_id
        ])
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=8))
    def _make_request(self, endpoint: str, method: str = "GET", **kwargs) -> Dict[str, Any]:
        """Make authenticated request to GitLab API"""
        
        if not self.is_configured():
            raise ValueError("GitLab not configured. Set GITLAB_URL, GITLAB_TOKEN, and GITLAB_PROJECT_ID")
        
        url = f"{self.api_base}/{endpoint}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                timeout=30,
                **kwargs
            )
            
            response.raise_for_status()
            
            # Handle different content types
            if response.headers.get('content-type', '').startswith('application/json'):
                return response.json()
            else:
                return {"content": response.text, "binary": False}
        
        except requests.exceptions.RequestException as e:
            logger.error(f"GitLab API request failed: {e}")
            raise
    
    def get_project_info(self) -> Dict[str, Any]:
        """Get project information"""
        return self._make_request(f"projects/{self.gitlab_project_id}")
    
    def list_repository_files(self, 
                             path: str = "", 
                             ref: str = "main",
                             recursive: bool = True) -> List[Dict[str, Any]]:
        """
        List files in repository with proper deep traversal
        
        For deep directory structures, recursively traverses subdirectories
        to find all files (blobs), not just top-level directories.
        """
        
        if recursive:
            # Use deep traversal to find all files
            return self._traverse_directory_tree(path, ref)
        else:
            # Simple single-level listing
            params = {
                "ref": ref,
                "recursive": False
            }
            
            if path:
                params["path"] = path
            
            return self._make_request(
                f"projects/{self.gitlab_project_id}/repository/tree",
                params=params
            )
    
    def _traverse_directory_tree(self, path: str, ref: str, max_depth: int = 5) -> List[Dict[str, Any]]:
        """
        Recursively traverse directory tree to find all files
        
        GitLab's recursive=True hits pagination limits, so we manually traverse.
        """
        
        all_files = []
        dirs_to_process = [(path, 0)]  # (path, depth)
        
        while dirs_to_process:
            current_path, depth = dirs_to_process.pop(0)
            
            if depth > max_depth:
                continue
            
            try:
                params = {
                    "ref": ref,
                    "recursive": False,  # Get only this level
                    "per_page": 100
                }
                
                if current_path:
                    params["path"] = current_path
                
                items = self._make_request(
                    f"projects/{self.gitlab_project_id}/repository/tree",
                    params=params
                )
                
                for item in items:
                    if item.get("type") == "blob":
                        # It's a file, add it
                        all_files.append(item)
                    elif item.get("type") == "tree":
                        # It's a directory, add to queue
                        dirs_to_process.append((item["path"], depth + 1))
                
            except Exception as e:
                logger.warning(f"Failed to traverse {current_path}: {e}")
                continue
        
        return all_files
    
    def get_file_content(self, 
                        file_path: str, 
                        ref: str = "main") -> Dict[str, Any]:
        """Get content of a specific file"""
        
        encoded_path = quote_plus(file_path)
        
        try:
            file_data = self._make_request(
                f"projects/{self.gitlab_project_id}/repository/files/{encoded_path}",
                params={"ref": ref}
            )
            
            # Decode base64 content
            if "content" in file_data and file_data.get("encoding") == "base64":
                decoded_content = base64.b64decode(file_data["content"]).decode('utf-8')
                file_data["decoded_content"] = decoded_content
            
            return file_data
        
        except Exception as e:
            logger.error(f"Failed to get file {file_path}: {e}")
            return {"error": str(e), "file_path": file_path}
    
    def search_code(self, 
                   search_term: str, 
                   scope: str = "blobs") -> List[Dict[str, Any]]:
        """Search for code in repository"""
        
        params = {
            "search": search_term,
            "scope": scope  # blobs, commits, issues, merge_requests, milestones, projects, users, wiki_blobs
        }
        
        try:
            return self._make_request(
                f"projects/{self.gitlab_project_id}/search",
                params=params
            )
        except Exception as e:
            logger.error(f"Code search failed: {e}")
            return []
    
    def get_commits(self, 
                   path: str = None, 
                   since: str = None,
                   limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent commits, optionally filtered by path"""
        
        params = {
            "per_page": limit,
            "ref_name": "main"
        }
        
        if path:
            params["path"] = path
        if since:
            params["since"] = since
        
        try:
            return self._make_request(
                f"projects/{self.gitlab_project_id}/repository/commits",
                params=params
            )
        except Exception as e:
            logger.error(f"Failed to get commits: {e}")
            return []
    
    def get_file_blame(self, file_path: str, ref: str = "main") -> List[Dict[str, Any]]:
        """Get blame information for a file (who changed what lines)"""
        
        encoded_path = quote_plus(file_path)
        
        try:
            return self._make_request(
                f"projects/{self.gitlab_project_id}/repository/files/{encoded_path}/blame",
                params={"ref": ref}
            )
        except Exception as e:
            logger.error(f"Failed to get blame for {file_path}: {e}")
            return []
    
    def find_files_by_pattern(self, 
                             pattern: str,
                             file_extensions: List[str] = None) -> List[Dict[str, Any]]:
        """Find files matching a pattern"""
        
        all_files = self.list_repository_files(recursive=True)
        matching_files = []
        
        for file_info in all_files:
            if file_info.get("type") == "blob":  # Only files, not directories
                file_path = file_info.get("path", "")
                file_name = file_info.get("name", "")
                
                # Check pattern match
                if (pattern.lower() in file_path.lower() or 
                    pattern.lower() in file_name.lower()):
                    
                    # Check file extension if specified
                    if file_extensions:
                        if any(file_path.endswith(ext) for ext in file_extensions):
                            matching_files.append(file_info)
                    else:
                        matching_files.append(file_info)
        
        return matching_files
    
    def get_directory_structure(self, path: str = "") -> Dict[str, Any]:
        """Get organized directory structure"""
        
        files = self.list_repository_files(path=path, recursive=True)
        
        structure = {
            "path": path or "root",
            "files": [],
            "directories": {},
            "total_files": 0,
            "file_types": {}
        }
        
        for item in files:
            if item.get("type") == "blob":
                file_path = item.get("path", "")
                file_name = item.get("name", "")
                
                structure["files"].append({
                    "name": file_name,
                    "path": file_path,
                    "size": item.get("size", 0)
                })
                
                structure["total_files"] += 1
                
                # Track file types
                if "." in file_name:
                    ext = file_name.split(".")[-1].lower()
                    structure["file_types"][ext] = structure["file_types"].get(ext, 0) + 1
        
        return structure

# Global GitLab client instance
gitlab_client = GitLabClient()

# LangChain tool functions for agents
def get_file_content_tool(file_path: str, branch: str = "main") -> str:
    """LangChain tool to get file content from GitLab"""
    
    if not gitlab_client.is_configured():
        return "GitLab not configured. Set GITLAB_URL, GITLAB_TOKEN, and GITLAB_PROJECT_ID environment variables."
    
    try:
        result = gitlab_client.get_file_content(file_path, branch)
        
        if "error" in result:
            return f"Error accessing file {file_path}: {result['error']}"
        
        if "decoded_content" in result:
            return result["decoded_content"]
        else:
            return f"Could not decode content for file: {file_path}"
    
    except Exception as e:
        logger.error(f"GitLab file access failed: {e}")
        return f"Failed to access file {file_path}: {str(e)}"

def search_code_tool(search_term: str, max_results: int = 10) -> str:
    """LangChain tool to search code in GitLab"""
    
    if not gitlab_client.is_configured():
        return "GitLab not configured. Set GITLAB_URL, GITLAB_TOKEN, and GITLAB_PROJECT_ID environment variables."
    
    try:
        results = gitlab_client.search_code(search_term)
        
        if not results:
            return f"No code found matching: {search_term}"
        
        # Format results for agent consumption
        formatted_results = []
        for i, result in enumerate(results[:max_results]):
            formatted_results.append({
                "file_path": result.get("path", "Unknown"),
                "filename": result.get("filename", "Unknown"),
                "project_id": result.get("project_id"),
                "ref": result.get("ref", "main"),
                "startline": result.get("startline", 1)
            })
        
        return json.dumps(formatted_results, indent=2)
    
    except Exception as e:
        logger.error(f"GitLab code search failed: {e}")
        return f"Code search failed: {str(e)}"

def find_files_tool(pattern: str, extensions: str = "") -> str:
    """LangChain tool to find files by pattern"""
    
    if not gitlab_client.is_configured():
        return "GitLab not configured. Set GITLAB_URL, GITLAB_TOKEN, and GITLAB_PROJECT_ID environment variables."
    
    try:
        # Parse extensions
        file_extensions = [ext.strip() for ext in extensions.split(",")] if extensions else None
        
        results = gitlab_client.find_files_by_pattern(pattern, file_extensions)
        
        if not results:
            return f"No files found matching pattern: {pattern}"
        
        # Format results
        formatted_results = []
        for file_info in results[:20]:  # Limit to 20 results
            formatted_results.append({
                "name": file_info.get("name"),
                "path": file_info.get("path"),
                "size": file_info.get("size", 0)
            })
        
        return json.dumps(formatted_results, indent=2)
    
    except Exception as e:
        logger.error(f"GitLab file search failed: {e}")
        return f"File search failed: {str(e)}"

def get_recent_commits_tool(file_path: str = "", limit: int = 10) -> str:
    """LangChain tool to get recent commits"""
    
    if not gitlab_client.is_configured():
        return "GitLab not configured. Set GITLAB_URL, GITLAB_TOKEN, and GITLAB_PROJECT_ID environment variables."
    
    try:
        commits = gitlab_client.get_commits(path=file_path, limit=limit)
        
        if not commits:
            return "No commits found"
        
        # Format commits for agent
        formatted_commits = []
        for commit in commits:
            formatted_commits.append({
                "id": commit.get("short_id"),
                "title": commit.get("title"),
                "author": commit.get("author_name"),
                "date": commit.get("created_at"),
                "message": commit.get("message", "")[:200] + "..." if len(commit.get("message", "")) > 200 else commit.get("message", "")
            })
        
        return json.dumps(formatted_commits, indent=2)
    
    except Exception as e:
        logger.error(f"GitLab commits query failed: {e}")
        return f"Commits query failed: {str(e)}"

def get_project_structure_tool(path: str = "") -> str:
    """LangChain tool to get project directory structure"""
    
    if not gitlab_client.is_configured():
        return "GitLab not configured. Set GITLAB_URL, GITLAB_TOKEN, and GITLAB_PROJECT_ID environment variables."
    
    try:
        structure = gitlab_client.get_directory_structure(path)
        return json.dumps(structure, indent=2)
    
    except Exception as e:
        logger.error(f"GitLab structure query failed: {e}")
        return f"Project structure query failed: {str(e)}"

# Tool definitions for LangChain agents
GITLAB_TOOLS = [
    {
        "name": "get_file_content",
        "function": get_file_content_tool,
        "description": "Get the content of a specific file from GitLab repository. Input: file_path (string), optional branch (string, default: main)"
    },
    {
        "name": "search_code",
        "function": search_code_tool,
        "description": "Search for code patterns or text in the GitLab repository. Input: search_term (string), optional max_results (int, default: 10)"
    },
    {
        "name": "find_files",
        "function": find_files_tool,
        "description": "Find files matching a pattern or name. Input: pattern (string), optional extensions (comma-separated string like 'py,js,sql')"
    },
    {
        "name": "get_recent_commits",
        "function": get_recent_commits_tool,
        "description": "Get recent commits, optionally for a specific file path. Input: optional file_path (string), optional limit (int, default: 10)"
    },
    {
        "name": "get_project_structure",
        "function": get_project_structure_tool,
        "description": "Get the directory structure and file organization of the project. Input: optional path (string, default: root)"
    }
]
