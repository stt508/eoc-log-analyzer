# 🚀 EOC Log Analyzer - Quick Start Guide

## ⚡ Start the Application

```powershell
cd C:\Code\log-ai\eoc-log-analyzer
python -m streamlit run streamlit_app.py
```

**Opens:** http://localhost:8501

---

## 🔍 Analyze Logs

### **Step 1: Search for Logs**
```
Enter one or more identifiers:
• user_data1: e.g., "12345"
• user_data2: e.g., "ORD-67890"  
• user_data3: e.g., "CUST-ABC"

Click [🔍 Search]
```

### **Step 2: Ask Questions**
```
Type in chat:
• "What happened with this order?"
• "Why did the install type change?"
• "What errors occurred?"
• "Compare expected vs actual flow"
```

### **Step 3: Get AI Analysis**
```
AI analyzes:
✅ Detected flows in chronological order
✅ Expected vs actual behavior
✅ Root cause identification
✅ Actionable recommendations
```

---

## ⚙️ Configuration

### **Enable Vector Search (Optional)**

**Edit `.env` file:**
```bash
# Enable semantic document search (~$0.0001/query)
ENABLE_VECTOR_SEARCH=true
```

**Benefits:**
- ✅ Richer cross-document context
- ✅ Handles terminology variations
- ✅ Better error correlation

**Cost:** ~$0.0001 per query (negligible)

---

### **Enable GitLab Integration (Optional)**

**Edit `.env` file:**
```bash
# Enable code documentation generation
ENABLE_GITLAB=true
GITLAB_URL=https://gitlab.ftr.com
GITLAB_TOKEN=your_token_here
GITLAB_PROJECT_ID=396
```

**Allows:** Regenerating documentation from latest code

---

## 🔄 Regenerate Documentation

### **Option 1: UI Button**
```
1. Click "🔄 Regen" in header
2. Confirmation popup appears
3. Click "✅ Yes, Regenerate"
4. Wait ~10-15 minutes
```

### **Option 2: CLI**
```powershell
cd C:\Code\log-ai\eoc-log-analyzer
venv\Scripts\activate

# Full regeneration (docs + embeddings)
python tools\knowledge_server\regenerate_embeddings.py

# Docs only (no embeddings, free)
python tools\knowledge_server\regenerate_embeddings.py --skip-embeddings

# Embeddings only (skip doc generation)
python tools\knowledge_server\regenerate_embeddings.py --skip-docs
```

**Cost:** ~$0.01 (only for embedding generation)

---

## 📊 Status Indicators

```
🔍 EOC Log Analyzer  │ 📚 8 KB sections  │ 🔍 Vector ✅  │ 💻 GitLab ✅
```

- **📚 X KB sections** - Knowledge base loaded (8 files = good)
- **🔍 Vector ✅** - Vector search enabled in config
- **🔍 Vector ⚠️** - Vector search disabled (using file-based)
- **💻 GitLab ✅** - GitLab credentials configured
- **💻 GitLab ⚠️** - GitLab not configured (can't regenerate docs)

---

## 💰 Cost Per Analysis

| What | Cost | Notes |
|------|------|-------|
| **Search logs** | $0.00 | Database queries are free |
| **Ask question** | ~$0.02 | Single LLM call to Claude |
| **Vector search** | +$0.0003 | Only if enabled (~3 queries/analysis) |
| **Total per question** | **~$0.0203** | Very affordable! |

---

## 🎯 Common Use Cases

### **1. Order Troubleshooting**
```
Search: user_data1 = order ID
Ask: "Why did this order fail?"
Result: Flow-by-flow analysis with root cause
```

### **2. Install Type Issues**
```
Search: user_data2 = order number
Ask: "Why did install type change from FTTP to FTTN?"
Result: Detailed explanation with recalculation logic
```

### **3. Error Investigation**
```
Search: user_data3 = customer ID
Ask: "What errors occurred and why?"
Result: Error correlation across all flows
```

### **4. Flow Validation**
```
Search: Any identifier
Ask: "Did the order follow expected process?"
Result: Expected vs actual comparison
```

---

## 🐛 Troubleshooting

### **Q: No logs found?**
**A:** Check search criteria:
- Try different user_data fields
- Verify identifier exists in database
- Check Database API is running

### **Q: Vector search not working?**
**A:** Check config:
```bash
# In .env
ENABLE_VECTOR_SEARCH=true  # Must be true

# Check terminal for:
# ✅ "🔍 Vector ✅" in UI header
# ⚠️  "🔍 Vector ⚠️" means disabled
```

### **Q: "GitLab ⚠️" shown?**
**A:** GitLab not configured (optional):
- Only needed for regenerating docs
- Analysis still works with existing docs
- To fix: Add GitLab credentials to `.env`

### **Q: Analysis is slow?**
**A:** Expected times:
- Planning: ~100ms (very fast)
- Data fetching: ~1-2 seconds
- LLM analysis: ~3-5 seconds
- **Total: ~5-7 seconds per question**

---

## 📚 Documentation

- **System Flow:** `SYSTEM_FLOW_SUMMARY.md` - Complete flow explanation
- **Vector Search:** `tools/knowledge_server/VECTOR_SEARCH_SETUP.md` - Detailed setup
- **Implementation:** `VECTOR_SEARCH_IMPLEMENTATION.md` - Technical details

---

## 🎉 Quick Tips

1. **Start simple:** Just search + ask basic questions
2. **Enable vector search:** Only if you want richer context (+minimal cost)
3. **Regenerate monthly:** Keep docs fresh with latest code
4. **Use Windows Task Scheduler:** Automate weekly regeneration
5. **Check terminal:** See detailed progress logs

---

## ✅ You're Ready!

```powershell
# Start the app
cd C:\Code\log-ai\eoc-log-analyzer
python -m streamlit run streamlit_app.py

# Open browser: http://localhost:8501
# Search for logs → Ask questions → Get AI analysis!
```

**Questions?** Check `SYSTEM_FLOW_SUMMARY.md` for complete details.

