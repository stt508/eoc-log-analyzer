# ChromaDB Quick Start Guide

## 🚀 Get Started in 5 Minutes!

### Step 1: Install Dependencies

```bash
cd c:\Code\log-ai\eoc-log-analyzer
pip install -r requirements.txt
```

This installs:
- `chromadb>=0.4.22` - Local vector database
- `sentence-transformers>=2.3.1` - Embedding model

---

### Step 2: Configure .env File

Create or update `.env` file:

```bash
# Enable vector search
ENABLE_VECTOR_SEARCH=true

# Use ChromaDB (local, FREE)
VECTOR_BACKEND=chroma

# ChromaDB storage location
CHROMA_DB_PATH=./data/chroma_db
CHROMA_COLLECTION_NAME=eoc_knowledge
```

---

### Step 3: Generate Embeddings

**Option A: Via UI (Recommended)**

1. Start the app:
   ```bash
   streamlit run streamlit_app.py
   ```

2. Click the `>` icon (top-left) to open sidebar

3. Scroll down to "📦 Generate Embeddings"

4. Click "🚀 Generate Embeddings" button

5. Wait for completion (progress shown in UI)

**Option B: Via Command Line**

```bash
python generate_embeddings.py
```

Answer "yes" to prompts.

---

### Step 4: Verify Setup

Check the top header of the Streamlit app:
- Should show: `🔍 ChromaDB: X docs` (where X > 0)

Example: `🔍 ChromaDB: 150 docs` ✅

---

### Step 5: Start Analyzing!

Vector search now works automatically! Just use the app normally:

1. Select search type (e.g., "Order Number (DPI)")
2. Enter order number
3. Click "🔍 Analyze"

The AI will automatically:
- Detect flows from logs
- Query ChromaDB for relevant documentation
- Use context for better analysis

---

## 💰 Cost

**ChromaDB is 100% FREE!**
- ✅ No cloud costs
- ✅ Runs locally
- ✅ No API keys needed
- ✅ No usage limits

---

## 📊 What You'll See

### Before ChromaDB:
```
⚠️  No context found for 'InstallOptions'. 
    Analyzing with limited information...
```

### After ChromaDB:
```
✅ Found relevant documentation:
   - InstallOptions.md (score: 0.87)
   - OrderValidation.md (score: 0.72)
   
   Using context for detailed analysis...
```

**Result:** More accurate, contextual AI analysis! 🎯

---

## 🔄 When to Regenerate

Regenerate embeddings when you:
- ✅ Add new documentation files
- ✅ Update existing docs
- ✅ Change knowledge base structure

Just click the button in the sidebar again!

---

## 🆘 Troubleshooting

### "ChromaDB: 0 docs"
**Fix:** Run `python generate_embeddings.py`

### "No module named 'chromadb'"
**Fix:** Run `pip install -r requirements.txt`

### "Permission denied"
**Fix:** Make sure `./data/chroma_db` is writable

---

## 📚 More Info

- **Full Guide**: `VECTOR_EMBEDDINGS_GUIDE.md`
- **Implementation Details**: `CHROMADB_IMPLEMENTATION_SUMMARY.md`
- **ChromaDB Docs**: https://docs.trychroma.com/

---

## 🎉 You're Ready!

Your AI log analyzer now has semantic search superpowers! 🚀

**Happy analyzing!** 🔍

