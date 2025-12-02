# Vector Embeddings Guide

Complete guide to setting up and using vector embeddings for semantic search in the EOC Log Analyzer.

## 📋 Table of Contents

- [Overview](#overview)
- [Backend Options](#backend-options)
- [Quick Start (ChromaDB - Local)](#quick-start-chromadb---local)
- [Using Databricks Vector Search (Cloud)](#using-databricks-vector-search-cloud)
- [Generating Embeddings](#generating-embeddings)
- [Switching Backends](#switching-backends)
- [Troubleshooting](#troubleshooting)

---

## Overview

The EOC Log Analyzer supports **vector embeddings** for semantic search over documentation. This enables the AI to find relevant context even when exact keywords don't match.

**Key Benefits:**
- 🎯 **Semantic Search**: Finds relevant docs based on meaning, not just keywords
- 💰 **Free Option**: ChromaDB runs locally with zero cloud costs
- ☁️ **Cloud Option**: Databricks Vector Search scales to large datasets
- 🔄 **Easy Switch**: Change backends via config, no code changes

---

## Backend Options

### Option 1: ChromaDB (Local) 🏠

**Best for:**
- Development and testing
- Small to medium documentation sets (<1000 files)
- Zero cloud costs
- Full offline operation

**Pros:**
- ✅ FREE - No cloud costs
- ✅ Fast setup (< 5 minutes)
- ✅ Works offline
- ✅ No external dependencies

**Cons:**
- ⚠️ Limited to single machine
- ⚠️ Manual embedding regeneration
- ⚠️ No multi-user support

---

### Option 2: Databricks Vector Search (Cloud) ☁️

**Best for:**
- Production deployments
- Large documentation sets (>1000 files)
- Multi-user environments
- Auto-sync with GitLab

**Pros:**
- ✅ Scalable to massive datasets
- ✅ Auto-sync from GitLab
- ✅ Multi-user support
- ✅ Enterprise features

**Cons:**
- 💰 Costs ~$0.0001/query
- 💰 Embedding generation ~$0.01
- 🔐 Requires Databricks workspace
- 🌐 Requires internet connection

---

## Quick Start (ChromaDB - Local)

### 1. Install Dependencies

```bash
cd eoc-log-analyzer
pip install -r requirements.txt
```

This installs:
- `chromadb>=0.4.22` - Vector database
- `sentence-transformers>=2.3.1` - Embedding model

### 2. Configure Environment

Edit your `.env` file:

```bash
# Enable vector search
ENABLE_VECTOR_SEARCH=true

# Use ChromaDB backend
VECTOR_BACKEND=chroma

# ChromaDB storage path (default: ./data/chroma_db)
CHROMA_DB_PATH=./data/chroma_db

# Collection name (default: eoc_knowledge)
CHROMA_COLLECTION_NAME=eoc_knowledge
```

### 3. Prepare Knowledge Base

Ensure you have markdown files in:
```
eoc-log-analyzer/tools/knowledge_server/knowledge_base/
```

Organize files by category:
```
knowledge_base/
├── apis/
│   ├── ManageOrder.md
│   └── SubmitOrder.md
├── processes/
│   ├── InstallOptions.md
│   └── OrderValidation.md
└── errors/
    ├── CommonErrors.md
    └── ErrorHandling.md
```

### 4. Generate Embeddings

**Option A: Via Streamlit UI** (Recommended)

1. Start the app:
   ```bash
   streamlit run streamlit_app.py
   ```

2. Open sidebar (click `>` icon in top-left)

3. Scroll to "📦 Generate Embeddings"

4. Click "🚀 Generate Embeddings"

5. Wait for completion (progress shown in UI)

**Option B: Via Command Line**

```bash
python generate_embeddings.py
```

When prompted:
```
Do you want to proceed? (yes/no): yes
Clear existing embeddings? (yes/no): yes  # if regenerating
```

**What Happens:**
1. Loads all `.md` files from `knowledge_base/`
2. Chunks documents into ~1000 character segments with 200 char overlap
3. Generates embeddings using `all-MiniLM-L6-v2` model (~384 dimensions)
4. Stores in ChromaDB at `./data/chroma_db/`

**Time Estimate:**
- 100 files: ~2-3 minutes
- 500 files: ~10-15 minutes
- 1000 files: ~20-30 minutes

### 5. Verify Setup

```bash
streamlit run streamlit_app.py
```

Check the top header:
- Should show: `🔍 ChromaDB: X docs` (where X is your document count)

---

## Using Databricks Vector Search (Cloud)

For production deployments on Databricks.

### 1. Set Up Databricks Project

The `eoc-vector-embeddings` project handles Databricks setup:

```bash
cd ../eoc-vector-embeddings
```

Follow: `eoc-vector-embeddings/DATABRICKS_SETUP.md`

### 2. Configure eoc-log-analyzer

Edit `.env`:

```bash
# Enable vector search
ENABLE_VECTOR_SEARCH=true

# Use Databricks backend
VECTOR_BACKEND=databricks

# Databricks vector index name
DATABRICKS_VECTOR_INDEX=ordercare_knowledge_index
```

### 3. Ensure Databricks Credentials

Already configured in `.env`:
```bash
DATABRICKS_TOKEN=dapi-your-token
DATABRICKS_BASE_URL=https://dbc-xxx.cloud.databricks.com/serving-endpoints/...
```

### 4. Test Connection

Start the app and check header:
- Should show: `🔍 Databricks ✅`

---

## Generating Embeddings

### When to Regenerate

- ✅ After adding new documentation files
- ✅ After updating existing documentation
- ✅ After changing chunking strategy
- ✅ When switching knowledge base content

### Best Practices

1. **Backup First**: The generator asks if you want to clear existing embeddings
2. **Test Files**: Start with a small subset to test quality
3. **Monitor Progress**: Watch terminal output for errors
4. **Verify After**: Check document count in UI header

### Embedding Model Details

**Model Used**: `all-MiniLM-L6-v2` (SentenceTransformers)

- **Size**: 80 MB (downloads automatically on first run)
- **Dimensions**: 384
- **Speed**: ~1000 sentences/second on CPU
- **Quality**: Good balance of speed and accuracy
- **License**: Apache 2.0 (free for commercial use)

### Chunking Strategy

Documents are split into overlapping chunks:

```python
chunk_size = 1000 characters
overlap = 200 characters
```

**Why Chunking?**
- Preserves context within chunks
- Avoids hitting model token limits
- Improves retrieval precision
- Allows fine-grained matching

**Example:**

```
Document: 3000 characters
Result:
  - Chunk 0: chars 0-1000
  - Chunk 1: chars 800-1800 (overlaps 200)
  - Chunk 2: chars 1600-2600 (overlaps 200)
  - Chunk 3: chars 2400-3000 (overlaps 200)
```

---

## Switching Backends

You can easily switch between ChromaDB and Databricks without code changes.

### From ChromaDB → Databricks

1. Update `.env`:
   ```bash
   VECTOR_BACKEND=databricks
   ```

2. Ensure Databricks index is set up (see `eoc-vector-embeddings` project)

3. Restart app

### From Databricks → ChromaDB

1. Update `.env`:
   ```bash
   VECTOR_BACKEND=chroma
   ```

2. Generate embeddings locally (if not already done)

3. Restart app

### Disable Vector Search Entirely

To use only file-based search:

```bash
ENABLE_VECTOR_SEARCH=false
```

App will fall back to keyword-based file search (free, fast, but less accurate).

---

## Troubleshooting

### Issue: "ChromaDB is empty"

**Cause**: No embeddings have been generated yet.

**Fix**:
```bash
python generate_embeddings.py
```

---

### Issue: "Embedding generation timed out"

**Cause**: Large documentation set taking >10 minutes.

**Fix**: Run manually in terminal (no timeout):
```bash
python generate_embeddings.py
```

---

### Issue: "No module named 'chromadb'"

**Cause**: Dependencies not installed.

**Fix**:
```bash
pip install -r requirements.txt
```

---

### Issue: "Permission denied" writing to ChromaDB

**Cause**: ChromaDB directory not writable.

**Fix**:
```bash
mkdir -p data/chroma_db
chmod 755 data/chroma_db
```

Or change path in `.env`:
```bash
CHROMA_DB_PATH=/tmp/chroma_db
```

---

### Issue: Vector search returns no results

**Possible Causes:**
1. Embeddings not generated
2. Query too specific
3. Score threshold too high

**Fix**:
1. Check header shows: `🔍 ChromaDB: X docs` (X > 0)
2. Try broader queries
3. Lower `score_threshold` in `knowledge_tools.py` (default: 0.5)

---

### Issue: "Databricks Vector Search failed"

**Possible Causes:**
1. Index not created
2. Invalid credentials
3. Network connectivity

**Fix**:
1. Verify index exists in Databricks workspace
2. Check `DATABRICKS_TOKEN` and `DATABRICKS_BASE_URL` in `.env`
3. Test network: `curl -H "Authorization: Bearer $DATABRICKS_TOKEN" $DATABRICKS_BASE_URL/health`

---

## Performance Tuning

### ChromaDB Performance

**Fast Queries:**
- Queries are <100ms on modern hardware
- No optimization needed for <10,000 documents

**Embedding Generation:**
- CPU: ~1000 docs/minute
- GPU: ~5000 docs/minute (if available)

To use GPU (CUDA):
```bash
pip install sentence-transformers[cuda]
```

### Search Quality Tuning

Edit `knowledge_tools.py`:

```python
# Increase results returned
num_results = 10  # default: 5

# Lower threshold for more results (less precise)
score_threshold = 0.3  # default: 0.5

# Higher threshold for fewer results (more precise)
score_threshold = 0.7  # default: 0.5
```

---

## Cost Comparison

| Backend | Query Cost | Embedding Cost | Storage Cost | Total (1000 queries/day) |
|---------|-----------|----------------|--------------|--------------------------|
| **ChromaDB** | $0.00 | $0.00 | $0.00 | **$0.00/month** ✅ |
| **Databricks** | $0.0001 | $0.01 (one-time) | $0.05/GB/month | **~$3-5/month** |

**ChromaDB** is completely FREE when running locally! 🎉

---

## Next Steps

- ✅ [Generate embeddings](#generating-embeddings)
- ✅ Test semantic search in the Streamlit UI
- ✅ Add more documentation to `knowledge_base/`
- ✅ Fine-tune search quality settings
- ✅ Consider Databricks for production

---

## Support

For issues or questions:
1. Check [Troubleshooting](#troubleshooting) section
2. Review logs in terminal output
3. Check ChromaDB docs: https://docs.trychroma.com/
4. Check SentenceTransformers docs: https://www.sbert.net/

---

**Happy Searching! 🔍**

