"""
Knowledge Server Tools (Vector Search Edition)

Provides LangChain tools for agents to query system documentation via vector search.
Supports multiple backends:
- ChromaDB (local) - Free, runs on your machine
- Databricks Vector Search (cloud) - Scalable, requires Databricks

Falls back to file-based search if vector DB is unavailable.
"""

from typing import List, Dict, Any, Optional
from langchain.tools import Tool
from loguru import logger
import requests

from config import config

# Vector backends
from .chroma_vector_manager import get_chroma_manager

# Fallback to file-based search
from .mcp_server import knowledge_server


def search_knowledge_base(query: str, num_results: int = 5) -> Optional[str]:
    """
    Search knowledge base using vector search (ChromaDB or Databricks)
    
    Backend is controlled by VECTOR_BACKEND config:
    - "chroma" (default): Local ChromaDB - FREE, no cloud costs
    - "databricks": Databricks Vector Search - ~$0.0001/query
    
    Args:
        query: Search query
        num_results: Number of results to return
    
    Returns:
        Combined content from matching documents or None
    """
    # Check if vector search is enabled in config
    if not config.app.enable_vector_search:
        logger.debug("Vector search disabled in config, using file-based fallback")
        return None
    
    try:
        # Route to appropriate backend
        if config.app.vector_backend == "chroma":
            return _search_chroma(query, num_results)
        elif config.app.vector_backend == "databricks":
            return _search_databricks(query, num_results)
        else:
            logger.warning(f"Unknown vector backend: {config.app.vector_backend}")
            return None
    
    except Exception as e:
        logger.warning(f"Vector search failed: {e}")
        return None


def _search_chroma(query: str, num_results: int = 5) -> Optional[str]:
    """Search using local ChromaDB"""
    try:
        chroma = get_chroma_manager()
        
        # Check if collection has data
        stats = chroma.get_collection_stats()
        if stats.get("total_documents", 0) == 0:
            logger.warning("⚠️  ChromaDB is empty. Generate embeddings first.")
            return None
        
        # Search
        logger.debug(f"🔍 Searching ChromaDB: '{query[:50]}...'")
        results = chroma.search(query, num_results=num_results, score_threshold=0.5)
        
        if not results:
            logger.debug(f"⚠️  No vector matches in ChromaDB")
            return None
        
        # Combine matched chunks
        combined = "\n\n---\n\n".join([
            f"**Source:** {r['source_file']} (chunk {r['chunk_index']}, score: {r['score']:.2f})\n\n{r['content']}"
            for r in results
        ])
        
        logger.debug(f"✅ ChromaDB returned {len(results)} results")
        return combined
    
    except Exception as e:
        logger.warning(f"ChromaDB search failed: {e}")
        return None


def _search_databricks(query: str, num_results: int = 5) -> Optional[str]:
    """Search using Databricks Vector Search REST API"""
    try:
        # Extract workspace URL from LLM endpoint URL
        workspace_url = config.llm.databricks_base_url.rsplit("/serving-endpoints/", 1)[0]
        
        # Vector Search API endpoint
        index_name = config.app.databricks_vector_index
        api_url = f"{workspace_url}/api/2.0/vector-search/indexes/{index_name}/query"
        
        # Query the vector index
        logger.debug(f"🔍 Querying Databricks vector index: '{query[:50]}...'")
        
        response = requests.post(
            api_url,
            headers={
                "Authorization": f"Bearer {config.llm.databricks_token}",
                "Content-Type": "application/json"
            },
            json={
                "query_text": query,
                "num_results": num_results,
                "score_threshold": 0.5
            },
            timeout=10
        )
        
        if response.status_code != 200:
            logger.warning(f"Databricks Vector Search API error: {response.status_code}")
            return None
        
        data = response.json()
        results = data.get("result", {}).get("data_array", [])
        
        if not results:
            logger.debug(f"⚠️  No vector matches in Databricks")
            return None
        
        # Parse results: [doc_id, source_file, content, chunk_index, score]
        parsed_results = []
        for row in results:
            if len(row) >= 5:
                parsed_results.append({
                    "doc_id": row[0],
                    "source_file": row[1],
                    "content": row[2],
                    "chunk_index": row[3],
                    "score": row[4]
                })
        
        if parsed_results:
            # Combine matched chunks
            combined = "\n\n---\n\n".join([
                f"**Source:** {r['source_file']} (chunk {r['chunk_index']}, score: {r['score']:.2f})\n\n{r['content']}"
                for r in parsed_results
            ])
            logger.debug(f"✅ Databricks returned {len(parsed_results)} results")
            return combined
        
        return None
    
    except Exception as e:
        logger.warning(f"Databricks Vector Search failed: {e}")
        return None


def query_services_tool(search_term: str = "") -> str:
    """
    Query the service catalog to find services.
    Uses vector search for semantic matching.
    
    Args:
        search_term: Service name or description (e.g., "ManageOrder", "customer order")
    
    Returns:
        Matching services with descriptions
    """
    try:
        # Try vector search first
        query = f"Service catalog: {search_term}" if search_term else "List all services"
        result = search_knowledge_base(query, num_results=5)
        
        if result:
            return result
        
        # Fallback to file-based search
        logger.info("   Using fallback file-based search...")
        services = knowledge_server.query_services(search_term)
        
        if not services:
            return f"⚠️  No services found for '{search_term}'. Context not available."
        
        import json
        return json.dumps({"total": len(services), "services": services}, indent=2)
    
    except Exception as e:
        logger.error(f"Error querying services: {e}")
        return f"❌ Error: {str(e)}"


def get_api_contract_tool(service_name: str = "") -> str:
    """
    Get API contract details for a service.
    Uses vector search for semantic matching.
    
    Args:
        service_name: Name of the service (e.g., "ManageOrder")
    
    Returns:
        API contract with request/response structures
    """
    try:
        # Try vector search first
        query = f"API contract for {service_name}: request and response structure, parameters, error codes"
        result = search_knowledge_base(query, num_results=3)
        
        if result:
            return result
        
        # Fallback to file-based search
        logger.info("   Using fallback file-based search...")
        contract = knowledge_server.get_api_contract(service_name)
        
        if not contract:
            return f"⚠️  No API contract found for '{service_name}'. Context not available."
        
        return contract.get('content', 'No content available')
    
    except Exception as e:
        logger.error(f"Error getting API contract: {e}")
        return f"❌ Error: {str(e)}"


def get_process_flow_tool(process_name: str = "") -> str:
    """
    Get business process flow details.
    Uses vector search for semantic matching.
    
    Args:
        process_name: Name of the process (e.g., "InstallOptions", "OM.quoteToOrder", 
                     "CustomerOrderManagement:CustomerOrderManagement/CommitCustomerOrder")
    
    Returns:
        Process flow with steps, expected behavior, errors
    """
    try:
        # Try vector search first
        query = f"Process flow for {process_name}: expected steps, behavior, timing, common errors, install types"
        result = search_knowledge_base(query, num_results=5)
        
        if result:
            return result
        
        # Fallback to file-based search
        logger.info("   Using fallback file-based search...")
        flow = knowledge_server.get_process_flow(process_name)
        
        if not flow:
            return f"⚠️  No process flow found for '{process_name}'. Context not available."
        
        if 'available_processes' in flow:
            import json
            return json.dumps(flow, indent=2)
        
        return flow.get('content', 'No content available')
    
    except Exception as e:
        logger.error(f"Error getting process flow: {e}")
        return f"❌ Error: {str(e)}"


def search_documentation_tool(query: str) -> str:
    """
    Search across all documentation using vector similarity.
    
    Args:
        query: Natural language query (e.g., "How does install type recalculation work?")
    
    Returns:
        Relevant documentation sections
    """
    try:
        # Vector search
        result = search_knowledge_base(query, num_results=5)
        
        if result:
            return result
        
        # Fallback to file-based search
        logger.info("   Using fallback file-based search...")
        results = knowledge_server.search(query)
        
        if not results:
            return f"⚠️  No documentation found for '{query}'. Context not available."
        
        import json
        return json.dumps(results, indent=2)
    
    except Exception as e:
        logger.error(f"Error searching documentation: {e}")
        return f"❌ Error: {str(e)}"


def get_system_overview_tool(_: str = "") -> str:
    """
    Get high-level system overview and architecture.
    
    Returns:
        System overview documentation
    """
    try:
        # Try vector search
        result = search_knowledge_base("System architecture overview: high-level components, services, data flow", num_results=3)
        
        if result:
            return result
        
        # Fallback
        logger.info("   Using fallback file-based search...")
        return knowledge_server.get_system_overview()
    
    except Exception as e:
        logger.error(f"Error getting system overview: {e}")
        return f"❌ Error: {str(e)}"


def get_error_handling_info_tool(_: str = "") -> str:
    """
    Get information about error handling patterns.
    
    Returns:
        Error handling documentation
    """
    try:
        # Try vector search
        result = search_knowledge_base("Error handling patterns: common errors, error codes, resolution steps", num_results=5)
        
        if result:
            return result
        
        # Fallback
        logger.info("   Using fallback file-based search...")
        return knowledge_server.get_error_handling_info()
    
    except Exception as e:
        logger.error(f"Error getting error handling info: {e}")
        return f"❌ Error: {str(e)}"


# Create LangChain tools
KNOWLEDGE_TOOLS = [
    Tool(
        name="query_services",
        func=query_services_tool,
        description="Search the service catalog using semantic matching. "
                   "Example: 'customer order services' or 'ManageOrder'"
    ),
    Tool(
        name="get_api_contract",
        func=get_api_contract_tool,
        description="Get API contract details using semantic search. "
                   "Example: 'ManageOrder' or 'order submission API'"
    ),
    Tool(
        name="get_process_flow",
        func=get_process_flow_tool,
        description="Get business process flow using semantic search. "
                   "Example: 'InstallOptions', 'Legacy Submit Order', 'OM.quoteToOrder'"
    ),
    Tool(
        name="search_documentation",
        func=search_documentation_tool,
        description="Search all documentation using natural language. "
                   "Example: 'How does install type recalculation work?' or 'validation errors'"
    ),
    Tool(
        name="get_system_overview",
        func=get_system_overview_tool,
        description="Get high-level system architecture and overview. "
                   "Use this at the start of analysis."
    ),
    Tool(
        name="get_error_handling_info",
        func=get_error_handling_info_tool,
        description="Get error handling patterns and common errors. "
                   "Use this when troubleshooting errors."
    ),
]
