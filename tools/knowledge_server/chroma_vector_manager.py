"""
ChromaDB Vector Manager

Manages local vector embeddings using ChromaDB for semantic search.
Provides a simple interface to generate, store, and query embeddings.

Cost: FREE - Runs locally, no cloud costs
"""

import os
from typing import List, Dict, Any, Optional
from pathlib import Path
import json

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from loguru import logger

from config import config


class ChromaVectorManager:
    """Manages vector embeddings using ChromaDB"""
    
    def __init__(self):
        """Initialize ChromaDB client and embedding model"""
        
        # Ensure ChromaDB directory exists
        db_path = Path(config.app.chroma_db_path)
        db_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=str(db_path),
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Get or create collection
        self.collection_name = config.app.chroma_collection_name
        try:
            self.collection = self.client.get_collection(name=self.collection_name)
            logger.info(f"✅ Loaded existing ChromaDB collection: {self.collection_name}")
        except Exception:
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "EOC Knowledge Base - Process flows, APIs, documentation"}
            )
            logger.info(f"✅ Created new ChromaDB collection: {self.collection_name}")
        
        # Initialize embedding model (all-MiniLM-L6-v2 is fast and good quality)
        self.embedding_model = None
        logger.info("✅ ChromaDB Vector Manager initialized")
    
    def _get_embedding_model(self) -> SentenceTransformer:
        """Lazy load embedding model (only when needed for generation)"""
        if self.embedding_model is None:
            logger.info("🔄 Loading embedding model (all-MiniLM-L6-v2)...")
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("✅ Embedding model loaded")
        return self.embedding_model
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector collection"""
        try:
            count = self.collection.count()
            return {
                "total_documents": count,
                "collection_name": self.collection_name,
                "backend": "chroma",
                "status": "ready" if count > 0 else "empty"
            }
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {"status": "error", "error": str(e)}
    
    def add_documents(
        self,
        documents: List[str],
        metadatas: List[Dict[str, Any]],
        ids: List[str]
    ) -> bool:
        """
        Add documents to the vector database
        
        Args:
            documents: List of text content to embed
            metadatas: List of metadata dicts (source_file, chunk_index, etc.)
            ids: Unique IDs for each document
        
        Returns:
            Success boolean
        """
        try:
            if not documents:
                logger.warning("⚠️  No documents to add")
                return False
            
            # Generate embeddings
            model = self._get_embedding_model()
            logger.info(f"🔄 Generating embeddings for {len(documents)} documents...")
            embeddings = model.encode(documents, show_progress_bar=True)
            
            # Add to ChromaDB
            logger.info(f"🔄 Adding {len(documents)} documents to ChromaDB...")
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids,
                embeddings=embeddings.tolist()
            )
            
            logger.info(f"✅ Added {len(documents)} documents to vector database")
            return True
        
        except Exception as e:
            logger.error(f"❌ Error adding documents: {e}")
            return False
    
    def search(
        self,
        query: str,
        num_results: int = 5,
        score_threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Search for similar documents
        
        Args:
            query: Search query text
            num_results: Number of results to return
            score_threshold: Minimum similarity score (0-1)
        
        Returns:
            List of matching documents with metadata and scores
        """
        try:
            # Check if collection is empty
            if self.collection.count() == 0:
                logger.warning("⚠️  Vector database is empty")
                return []
            
            # Generate query embedding
            model = self._get_embedding_model()
            query_embedding = model.encode([query])[0]
            
            # Search ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=num_results,
                include=["documents", "metadatas", "distances"]
            )
            
            # Parse results
            parsed_results = []
            if results and results['ids'] and len(results['ids']) > 0:
                for i in range(len(results['ids'][0])):
                    # Convert distance to similarity score (ChromaDB uses L2 distance)
                    distance = results['distances'][0][i]
                    similarity = 1 / (1 + distance)  # Convert distance to similarity
                    
                    if similarity >= score_threshold:
                        parsed_results.append({
                            "doc_id": results['ids'][0][i],
                            "content": results['documents'][0][i],
                            "metadata": results['metadatas'][0][i],
                            "score": similarity,
                            "source_file": results['metadatas'][0][i].get('source_file', 'unknown'),
                            "chunk_index": results['metadatas'][0][i].get('chunk_index', 0)
                        })
            
            logger.debug(f"✅ Found {len(parsed_results)} results for query: '{query[:50]}...'")
            return parsed_results
        
        except Exception as e:
            logger.error(f"❌ Error searching vector database: {e}")
            return []
    
    def clear_collection(self) -> bool:
        """Clear all documents from the collection"""
        try:
            logger.warning(f"🗑️  Clearing collection: {self.collection_name}")
            self.client.delete_collection(name=self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "EOC Knowledge Base - Process flows, APIs, documentation"}
            )
            logger.info("✅ Collection cleared")
            return True
        except Exception as e:
            logger.error(f"❌ Error clearing collection: {e}")
            return False


# Global instance
_chroma_manager = None

def get_chroma_manager() -> ChromaVectorManager:
    """Get or create global ChromaDB manager instance"""
    global _chroma_manager
    if _chroma_manager is None:
        _chroma_manager = ChromaVectorManager()
    return _chroma_manager

