"""
MCP Knowledge Server
Provides AI agents access to system documentation and code context
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from loguru import logger


class KnowledgeServer:
    """
    MCP Knowledge Server for EOC OrderCare documentation
    
    Provides:
    - Service catalog lookup
    - API contract information
    - Process flow documentation
    - File path resolution for code fetching
    """
    
    def __init__(self, docs_dir: str = "tools/knowledge_server/docs"):
        self.docs_dir = Path(docs_dir)
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        
        self.documentation: Dict[str, Any] = {}
        self.last_loaded: Optional[datetime] = None
        
        # Load documentation if available
        self._load_documentation()
        
        logger.info(f"Knowledge Server initialized - Docs: {len(self.documentation)} sections")
    
    def _load_documentation(self):
        """Load all markdown documentation into memory"""
        
        doc_files = {
            "home": "00-Home.md",
            "system_overview": "01-System-Overview.md",
            "service_catalog": "02-Service-Catalog.md",
            "expected_flows": "03-Expected-Flows.md",
            "api_contracts": "04-API-Contracts.md",
            "error_handling": "05-Error-Handling.md",
            "component_map": "06-Component-Map.md",
            "quick_reference": "07-Agent-Quick-Reference.md"
        }
        
        for key, filename in doc_files.items():
            file_path = self.docs_dir / filename
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        self.documentation[key] = f.read()
                except Exception as e:
                    logger.warning(f"Failed to load {filename}: {e}")
        
        if self.documentation:
            self.last_loaded = datetime.now()
            logger.info(f"Loaded {len(self.documentation)} documentation sections")
    
    def query_services(self, search_term: str = "") -> List[Dict[str, str]]:
        """
        Query service catalog
        
        Returns list of services matching search term
        """
        if "service_catalog" not in self.documentation:
            return []
        
        content = self.documentation["service_catalog"]
        services = []
        
        # Parse markdown to extract service entries
        lines = content.split('\n')
        current_service = {}
        
        for line in lines:
            if line.startswith('### '):
                # New service found
                if current_service:
                    services.append(current_service)
                current_service = {"name": line.replace('### ', '').strip()}
            
            elif '**Path:**' in line:
                # Extract file path
                path = line.split('`')[1] if '`' in line else ""
                current_service["file_path"] = path
            
            elif '**Responsibility:**' in line:
                current_service["responsibility"] = line.split('**Responsibility:**')[1].strip()
        
        # Add last service
        if current_service:
            services.append(current_service)
        
        # Filter by search term
        if search_term:
            search_lower = search_term.lower()
            services = [s for s in services if search_lower in s.get('name', '').lower()]
        
        return services
    
    def get_api_contract(self, service_name: str = "") -> Optional[Dict[str, Any]]:
        """
        Get API contract details for a service
        
        Returns contract information including request/response structures
        """
        if "api_contracts" not in self.documentation:
            return None
        
        content = self.documentation["api_contracts"]
        
        if not service_name:
            return {"content": content[:1000]}  # Return first 1000 chars
        
        # Search for specific service
        lines = content.split('\n')
        in_contract = False
        contract_lines = []
        
        for line in lines:
            if line.startswith('## ') and service_name.lower() in line.lower():
                in_contract = True
            
            if in_contract:
                contract_lines.append(line)
                
                # Stop at next contract
                if line.startswith('## ') and len(contract_lines) > 1:
                    break
        
        return {"content": '\n'.join(contract_lines)} if contract_lines else None
    
    def get_process_flow(self, process_name: str = "") -> Optional[Dict[str, Any]]:
        """
        Get business process flow details
        
        Returns process steps and expected behavior
        """
        if "expected_flows" not in self.documentation:
            return None
        
        content = self.documentation["expected_flows"]
        
        if not process_name:
            # Return list of available processes
            processes = []
            for line in content.split('\n'):
                if line.startswith('## '):
                    processes.append(line.replace('## ', '').strip())
            return {"available_processes": processes}
        
        # Search for specific process
        lines = content.split('\n')
        in_process = False
        process_lines = []
        
        for line in lines:
            if line.startswith('## ') and process_name.lower() in line.lower():
                in_process = True
            
            if in_process:
                process_lines.append(line)
                
                # Stop at next process
                if line.startswith('## ') and len(process_lines) > 1:
                    break
        
        return {"content": '\n'.join(process_lines)} if process_lines else None
    
    def get_file_path(self, service_or_component: str) -> Optional[str]:
        """
        Get file path for a service or component
        
        Returns GitLab file path for fetching actual code
        """
        services = self.query_services(service_or_component)
        
        if services and len(services) > 0:
            return services[0].get('file_path')
        
        return None
    
    def get_system_overview(self) -> str:
        """Get high-level system overview"""
        return self.documentation.get("system_overview", "Documentation not available")
    
    def get_error_handling_info(self) -> str:
        """Get error handling patterns and strategies"""
        return self.documentation.get("error_handling", "Error handling documentation not available")
    
    def search(self, query: str) -> List[Dict[str, Any]]:
        """
        Search across all documentation
        
        Returns relevant sections matching the query
        """
        results = []
        query_lower = query.lower()
        
        for section_name, content in self.documentation.items():
            if query_lower in content.lower():
                # Find context around match
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if query_lower in line.lower():
                        # Get 3 lines of context
                        context_start = max(0, i - 3)
                        context_end = min(len(lines), i + 4)
                        context = '\n'.join(lines[context_start:context_end])
                        
                        results.append({
                            "section": section_name,
                            "match": line.strip(),
                            "context": context
                        })
                        
                        if len(results) >= 10:  # Limit results
                            return results
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """Get knowledge base statistics"""
        return {
            "total_sections": len(self.documentation),
            "last_loaded": self.last_loaded.isoformat() if self.last_loaded else None,
            "available_sections": list(self.documentation.keys()),
            "docs_directory": str(self.docs_dir)
        }
    
    def reload(self):
        """Reload documentation from disk"""
        logger.info("Reloading documentation...")
        self.documentation = {}
        self._load_documentation()
        return {"status": "success", "sections_loaded": len(self.documentation)}


# Global instance
knowledge_server = KnowledgeServer()

