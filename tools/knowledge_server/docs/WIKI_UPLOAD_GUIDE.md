# Wiki Upload Guide

**Files Location:** `C:\Code\log-ai\eoc-log-analyzer\wiki_docs\`  
**Files to Upload:** 9 markdown files (8 documentation + 1 README)

---

## 📋 Quick Overview

You have 3 main options:

1. **Manual Upload** (via Web UI) - Easiest, 5-10 minutes
2. **Bulk Upload** (via API/CLI) - Fastest, 1-2 minutes if supported
3. **Git-based Upload** (if wiki is Git-backed) - Most automated

---

## 🌐 Option 1: Manual Upload via Web UI (RECOMMENDED)

### **Best For:** Confluence, MediaWiki, DokuWiki, GitLab Wiki, any wiki with web interface

### **Steps:**

#### 1. **Create Wiki Space/Project**
```
Space Name: "EOC OrderCare Documentation"
Space Key: EOCORDER (or similar)
Description: "Auto-generated technical documentation for EOC Order Care system"
```

#### 2. **Upload Files in Order:**

**Step-by-step:**

1. **Go to your wiki** → Create new space/project

2. **Create pages in this order:**
   - `00-Home.md` → Create as **"Home"** or **"Main Page"**
   - `01-System-Overview.md` → Create as **"System Overview"**
   - `02-Service-Catalog.md` → Create as **"Service Catalog"**
   - `03-Expected-Flows.md` → Create as **"Expected Flows"**
   - `04-API-Contracts.md` → Create as **"API Contracts"**
   - `05-Error-Handling.md` → Create as **"Error Handling"**
   - `06-Component-Map.md` → Create as **"Component Map"**
   - `07-Agent-Quick-Reference.md` → Create as **"Agent Quick Reference"**

3. **For each file:**
   - Open the `.md` file in Notepad
   - Copy all content (Ctrl+A, Ctrl+C)
   - Paste into wiki editor
   - Click **Save** or **Publish**

#### 3. **Update Internal Links** (if needed)

Most wikis will auto-convert markdown links like `[Service Catalog](./02-Service-Catalog.md)` to proper wiki links. If not, update them manually.

---

## ⚡ Option 2: Bulk Upload via Script

### **For Confluence (with API access):**

Create this PowerShell script: `upload_to_confluence.ps1`

```powershell
# Confluence API Upload Script

$CONFLUENCE_URL = "https://your-confluence-instance.com"
$SPACE_KEY = "EOCORDER"
$USERNAME = "your-email@company.com"
$API_TOKEN = "your-api-token"

# Base64 encode credentials
$base64AuthInfo = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${USERNAME}:${API_TOKEN}"))

$files = @(
    @{file="00-Home.md"; title="Home"; parent=$null},
    @{file="01-System-Overview.md"; title="System Overview"; parent="Home"},
    @{file="02-Service-Catalog.md"; title="Service Catalog"; parent="Home"},
    @{file="03-Expected-Flows.md"; title="Expected Flows"; parent="Home"},
    @{file="04-API-Contracts.md"; title="API Contracts"; parent="Home"},
    @{file="05-Error-Handling.md"; title="Error Handling"; parent="Home"},
    @{file="06-Component-Map.md"; title="Component Map"; parent="Home"},
    @{file="07-Agent-Quick-Reference.md"; title="Agent Quick Reference"; parent="Home"}
)

foreach ($item in $files) {
    Write-Host "Uploading $($item.title)..."
    
    $content = Get-Content "wiki_docs\$($item.file)" -Raw
    
    $body = @{
        type = "page"
        title = $item.title
        space = @{key = $SPACE_KEY}
        body = @{
            storage = @{
                value = $content
                representation = "markdown"
            }
        }
    } | ConvertTo-Json -Depth 10
    
    try {
        Invoke-RestMethod -Uri "$CONFLUENCE_URL/rest/api/content" `
            -Method Post `
            -Headers @{
                Authorization = "Basic $base64AuthInfo"
                "Content-Type" = "application/json"
            } `
            -Body $body
        
        Write-Host "✓ Uploaded $($item.title)" -ForegroundColor Green
    } catch {
        Write-Host "✗ Failed: $($item.title) - $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`nDone! Check your Confluence space."
```

**Run it:**
```powershell
cd C:\Code\log-ai\eoc-log-analyzer
.\upload_to_confluence.ps1
```

---

### **For GitLab Wiki:**

```powershell
# GitLab Wiki Upload Script

$GITLAB_URL = "https://gitlab.ftr.com"
$PROJECT_ID = "396"  # Your project ID
$GITLAB_TOKEN = "your-gitlab-token"

$files = @(
    "00-Home.md",
    "01-System-Overview.md",
    "02-Service-Catalog.md",
    "03-Expected-Flows.md",
    "04-API-Contracts.md",
    "05-Error-Handling.md",
    "06-Component-Map.md",
    "07-Agent-Quick-Reference.md"
)

foreach ($file in $files) {
    $slug = $file -replace '\.md$', '' -replace '^\d+-', '' -replace '-', '_'
    $title = $file -replace '\.md$', '' -replace '^\d+-', '' -replace '-', ' '
    $content = Get-Content "wiki_docs\$file" -Raw
    
    Write-Host "Uploading $title..."
    
    $body = @{
        content = $content
        title = $title
        format = "markdown"
    } | ConvertTo-Json
    
    try {
        Invoke-RestMethod -Uri "$GITLAB_URL/api/v4/projects/$PROJECT_ID/wikis" `
            -Method Post `
            -Headers @{
                "PRIVATE-TOKEN" = $GITLAB_TOKEN
                "Content-Type" = "application/json"
            } `
            -Body $body
        
        Write-Host "✓ Uploaded $title" -ForegroundColor Green
    } catch {
        Write-Host "✗ Failed: $title - $($_.Exception.Message)" -ForegroundColor Red
    }
}
```

---

## 📁 Option 3: Git-Based Upload (for Git-backed wikis)

### **If your wiki is backed by Git (GitLab, GitHub, Bitbucket):**

```powershell
# Navigate to your project
cd C:\path\to\your-project

# Clone the wiki repository
git clone https://gitlab.ftr.com/EOC/ordercare.wiki.git
cd ordercare.wiki

# Copy all markdown files
Copy-Item C:\Code\log-ai\eoc-log-analyzer\wiki_docs\*.md .

# Commit and push
git add *.md
git commit -m "Add EOC OrderCare system documentation

- System overview and architecture
- Complete service catalog
- Business process flows
- API contracts
- Error handling patterns
- Component relationships
- Agent quick reference

Generated from Trunk/FrontierOM codebase"

git push origin master
```

**The wiki will automatically render the markdown files!**

---

## 🎨 Option 4: Export to Other Formats (if needed)

### **Convert to HTML:**

```powershell
# Install pandoc if needed: choco install pandoc

cd C:\Code\log-ai\eoc-log-analyzer\wiki_docs

# Convert each file
Get-ChildItem *.md | ForEach-Object {
    $htmlFile = $_.Name -replace '\.md$', '.html'
    pandoc $_.Name -f markdown -t html -s -o $htmlFile
    Write-Host "Created $htmlFile"
}
```

### **Convert to PDF:**

```powershell
# Convert to PDF with pandoc
Get-ChildItem *.md | ForEach-Object {
    $pdfFile = $_.Name -replace '\.md$', '.pdf'
    pandoc $_.Name -f markdown -t pdf -o $pdfFile
    Write-Host "Created $pdfFile"
}
```

---

## 📊 Recommended Approach by Wiki Type

| Wiki Platform | Best Method | Time Required |
|--------------|-------------|---------------|
| **Confluence** | API Script (Option 2) | 2 min |
| **GitLab Wiki** | Git Clone (Option 3) | 3 min |
| **GitHub Wiki** | Git Clone (Option 3) | 3 min |
| **MediaWiki** | Manual Upload (Option 1) | 10 min |
| **DokuWiki** | Manual Upload (Option 1) | 10 min |
| **Notion** | Manual Upload (Option 1) | 10 min |
| **SharePoint** | Manual Upload (Option 1) | 10 min |

---

## ✅ Post-Upload Checklist

After uploading, verify:

- [ ] All 8 pages are created
- [ ] Internal links work (click through navigation)
- [ ] Code blocks render correctly
- [ ] Tables display properly
- [ ] File paths are readable
- [ ] Search functionality finds your pages

---

## 🔄 Future Updates

**To regenerate and re-upload:**

```powershell
# 1. Regenerate documentation
cd C:\Code\log-ai\eoc-log-analyzer
.\venv\Scripts\python.exe generate_wiki_docs.py --branch master --base-path Trunk/FrontierOM

# 2. Re-upload using your chosen method above
# (The files will overwrite the old ones)
```

**Frequency recommendation:** Regenerate monthly or after major code changes

---

## 🆘 Troubleshooting

### **Issue: Links don't work**

**Solution:** Update relative links to match your wiki structure
```
Before: [Service Catalog](./02-Service-Catalog.md)
After:  [Service Catalog](/eocorder/Service-Catalog)  # Adjust to your wiki
```

### **Issue: Code blocks look weird**

**Solution:** Ensure your wiki supports markdown code fences:
- Confluence: Use markdown macro
- MediaWiki: Use `<syntaxhighlight>` tags
- GitLab: Native support ✓

### **Issue: Permission denied**

**Solution:** 
- Verify API token has write permissions
- Check space/project permissions
- Try manual upload instead

---

## 📞 Need Help?

**Your files are ready at:**
```
C:\Code\log-ai\eoc-log-analyzer\wiki_docs\
```

**Quick test:** Open any `.md` file in VS Code or Notepad to verify content before uploading.

---

**🎯 Recommended for you:** If your wiki is on **GitLab** → Use **Option 3 (Git-based)**  
**Otherwise:** Use **Option 1 (Manual)** - it's fool-proof and takes 10 minutes.

