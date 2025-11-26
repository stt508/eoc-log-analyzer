# 📚 EOC Order Care - Wiki Documentation

## 🎯 Quick Start

This folder contains **wiki-ready markdown files** generated from the EOC Order Care codebase.

---

## 📁 Files in This Directory

| File | Purpose | Upload As |
|------|---------|-----------|
| `00-Home.md` | Navigation hub | **Home** or **Index** page |
| `01-System-Overview.md` | Architecture | **System Overview** |
| `02-Service-Catalog.md` | Services + file paths | **Service Catalog** |
| `03-Expected-Flows.md` | Flows + file paths | **Expected Flows** |
| `04-API-Contracts.md` | API inputs/outputs | **API Contracts** |
| `05-Error-Handling.md` | Error patterns | **Error Handling** |
| `06-Component-Map.md` | Component interactions | **Component Map** |
| `07-Agent-Quick-Reference.md` | AI agent guide | **Agent Quick Reference** |

---

## 🚀 How to Upload

### **Step 1: Choose Your Wiki**

- **Confluence:** Upload as pages in a space
- **SharePoint:** Upload to Wiki Library
- **GitHub/GitLab Wiki:** Copy files to wiki repo
- **Other:** Import markdown files

---

### **Step 2: Upload All Files**

1. Create a new space/site: **"EOC Order Care Documentation"**
2. Upload each markdown file as a separate page
3. Maintain the numeric prefixes for ordering (00, 01, 02...)

---

### **Step 3: Set Up Navigation**

Create links between pages using wiki's navigation features:
- Make `00-Home.md` the landing page
- Link all other pages from Home
- Enable breadcrumbs if available

---

## 🤖 For AI Agents

These files are designed for **both human and AI consumption**:

### **What Agents Get:**

✅ **Expected System Behavior** - What SHOULD happen  
✅ **File Paths** - Where to find code  
✅ **Fetch Commands** - Ready-to-use `get_file_content()` calls  
✅ **Troubleshooting Workflow** - Step-by-step guidance  

### **Agent Workflow:**

```
1. Read wiki docs → Understand expected behavior
2. Query database → Get actual behavior
3. Compare → Find deviation
4. Fetch code (using file paths) → Verify implementation
5. Analyze → Provide root cause
```

---

## 🔍 Example: File Paths Included

Every service includes its file path:

```markdown
### OrderService

**Path:** `Trunk/FrontierOM/services/OrderService.java`

**To fetch code:**
```python
get_file_content("Trunk/FrontierOM/services/OrderService.java")
```
```

Every flow step includes file paths:

```markdown
| Step | Component | File |
|------|-----------|------|
| 4 | OrderOrchestrator | `src/OrderOrchestrator.java` |
```

**This is the key feature!** Agents know WHERE to fetch code when needed.

---

## 🔄 Regenerating

To update these files:

```bash
# Windows
..\generate_wiki.bat

# Linux/Mac
python ../generate_wiki_docs.py
```

**When to regenerate:**
- After major code changes
- Weekly (recommended)
- When flows change

---

## 📖 More Information

- **Upload Guide:** `../WIKI_UPLOAD_GUIDE.md`
- **Complete Summary:** `../WIKI_DOCUMENTATION_SUMMARY.md`
- **Hybrid Approach:** `../HYBRID_CODE_CONTEXT_GUIDE.md`

---

## ✅ Ready to Upload!

1. ✅ Review files in this folder
2. ✅ Upload to your wiki
3. ✅ Configure agent MCP access
4. ✅ Agents will use wiki + fetch code as needed

**All set!** 🚀

