"""
Generate Vector Embeddings Script

Generates embeddings from knowledge base files and stores them in ChromaDB.
Run this manually when you want to update the vector database.

⚠️  This process can take several minutes depending on documentation size.
⚠️  FREE when using ChromaDB locally (no cloud costs).

Usage:
    python generate_embeddings.py
    
Or from Streamlit UI: Click the "Generate Embeddings" button
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any
import json
import time

from loguru import logger
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import config
from tools.knowledge_server.chroma_vector_manager import get_chroma_manager

console = Console()


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Split text into overlapping chunks for better context preservation
    
    Args:
        text: Text to chunk
        chunk_size: Size of each chunk in characters
        overlap: Overlap between chunks
    
    Returns:
        List of text chunks
    """
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # Find the last sentence boundary within the chunk
        if end < len(text):
            last_period = text.rfind('.', start, end)
            if last_period > start + chunk_size // 2:
                end = last_period + 1
        
        chunks.append(text[start:end].strip())
        start = end - overlap
    
    return chunks


def load_markdown_files(knowledge_dir: Path) -> List[Dict[str, Any]]:
    """
    Load all markdown files from the knowledge base directory
    
    Args:
        knowledge_dir: Path to knowledge base directory
    
    Returns:
        List of documents with content and metadata
    """
    documents = []
    
    if not knowledge_dir.exists():
        logger.warning(f"⚠️  Knowledge directory not found: {knowledge_dir}")
        return documents
    
    # Find all markdown files
    md_files = list(knowledge_dir.rglob("*.md"))
    
    if not md_files:
        logger.warning(f"⚠️  No markdown files found in {knowledge_dir}")
        return documents
    
    logger.info(f"📁 Found {len(md_files)} markdown files")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console
    ) as progress:
        
        task = progress.add_task("Loading markdown files...", total=len(md_files))
        
        for md_file in md_files:
            try:
                # Read file content
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Skip empty files
                if not content.strip():
                    continue
                
                # Get relative path for metadata
                rel_path = md_file.relative_to(knowledge_dir)
                
                # Chunk the content
                chunks = chunk_text(content, chunk_size=1000, overlap=200)
                
                # Create document for each chunk
                for i, chunk in enumerate(chunks):
                    documents.append({
                        "content": chunk,
                        "metadata": {
                            "source_file": str(rel_path),
                            "chunk_index": i,
                            "total_chunks": len(chunks),
                            "file_type": "markdown"
                        },
                        "id": f"{rel_path.stem}_chunk_{i}"
                    })
                
                progress.update(task, advance=1)
            
            except Exception as e:
                logger.error(f"❌ Error loading {md_file}: {e}")
                progress.update(task, advance=1)
                continue
    
    logger.info(f"✅ Loaded {len(documents)} document chunks from {len(md_files)} files")
    return documents


def generate_embeddings():
    """Main function to generate and store embeddings"""
    
    console.print("\n[bold cyan]🚀 Vector Embedding Generation[/bold cyan]\n")
    console.print("[yellow]⚠️  This process will:[/yellow]")
    console.print("  1. Load all markdown files from knowledge base")
    console.print("  2. Chunk documents for better context")
    console.print("  3. Generate embeddings using SentenceTransformers")
    console.print("  4. Store embeddings in ChromaDB (local)")
    console.print("\n[green]💰 Cost: FREE (runs locally, no cloud costs)[/green]\n")
    
    # Confirm with user
    response = input("Do you want to proceed? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        console.print("[red]❌ Cancelled[/red]")
        return
    
    start_time = time.time()
    
    # Get ChromaDB manager
    console.print("\n[cyan]🔄 Initializing ChromaDB...[/cyan]")
    chroma = get_chroma_manager()
    
    # Get current stats
    stats = chroma.get_collection_stats()
    console.print(f"[cyan]📊 Current collection: {stats['total_documents']} documents[/cyan]")
    
    # Ask if user wants to clear existing data
    if stats['total_documents'] > 0:
        response = input("\nClear existing embeddings? (yes/no): ").strip().lower()
        if response in ['yes', 'y']:
            console.print("[yellow]🗑️  Clearing existing data...[/yellow]")
            chroma.clear_collection()
    
    # Load markdown files
    console.print("\n[cyan]📂 Loading knowledge base files...[/cyan]")
    knowledge_dir = Path(__file__).parent / "tools" / "knowledge_server" / "knowledge_base"
    documents = load_markdown_files(knowledge_dir)
    
    if not documents:
        console.print("[red]❌ No documents found to process[/red]")
        return
    
    # Estimate processing time (rough estimate: ~2 seconds per document)
    estimated_minutes = (len(documents) * 2) // 60
    console.print(f"\n[yellow]⏱️  Estimated processing time: ~{estimated_minutes} minutes[/yellow]")
    
    # Generate and store embeddings
    console.print("\n[cyan]🔄 Generating embeddings...[/cyan]")
    
    # Prepare data for ChromaDB
    doc_contents = [doc["content"] for doc in documents]
    doc_metadatas = [doc["metadata"] for doc in documents]
    doc_ids = [doc["id"] for doc in documents]
    
    # Add to ChromaDB (this will generate embeddings)
    success = chroma.add_documents(
        documents=doc_contents,
        metadatas=doc_metadatas,
        ids=doc_ids
    )
    
    if success:
        elapsed_time = time.time() - start_time
        elapsed_minutes = int(elapsed_time // 60)
        elapsed_seconds = int(elapsed_time % 60)
        
        # Get final stats
        final_stats = chroma.get_collection_stats()
        
        console.print(f"\n[bold green]✅ Embedding generation complete![/bold green]")
        console.print(f"[green]📊 Total documents in ChromaDB: {final_stats['total_documents']}[/green]")
        console.print(f"[green]⏱️  Time taken: {elapsed_minutes}m {elapsed_seconds}s[/green]")
        console.print(f"\n[cyan]💡 Vector search is now ready to use![/cyan]")
        console.print(f"[cyan]   Set ENABLE_VECTOR_SEARCH=true in .env to enable[/cyan]")
    else:
        console.print("\n[bold red]❌ Failed to generate embeddings[/bold red]")
        console.print("[red]Check logs for details[/red]")


if __name__ == "__main__":
    try:
        generate_embeddings()
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Cancelled by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[bold red]❌ Error: {e}[/bold red]")
        logger.exception("Error during embedding generation")
        sys.exit(1)

