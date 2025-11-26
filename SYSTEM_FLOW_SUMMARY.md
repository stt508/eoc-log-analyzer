# EOC Log Analyzer - System Flow Summary

## 🎯 Overview

The EOC Log Analyzer uses a **multi-agent system** with **optional vector search** for semantic document retrieval. The system is designed to be:
- ✅ **Cost-aware**: No operations without user consent
- ✅ **Config-driven**: Vector search enabled/disabled via `.env`
- ✅ **Graceful degradation**: Falls back to file-based search if vector DB unavailable
- ✅ **Performance-focused**: Rule-based flow detection + semantic context retrieval

---

## 📊 System Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                     Streamlit UI (Web Interface)               │
├────────────────────────────────────────────────────────────────┤
│  • Search by user_data1/2/3                                    │
│  • Chat with AI                                                │
│  • "🔄 Regen" button (with confirmation popup)                 │
│  • Status indicators (Vector ✅/⚠️, GitLab ✅/⚠️)              │
└────────────────────────────────────────────────────────────────┘
                              ▼
┌────────────────────────────────────────────────────────────────┐
│                   Coordinator Agent (Orchestrator)             │
├────────────────────────────────────────────────────────────────┤
│  analyze_order(user_data1, user_data2, user_data3, goal)      │
│    1. Call Planning Agent → Get flow-based plan               │
│    2. Call Execution Agent → Execute plan with LLM analysis   │
│    3. Return comprehensive analysis                            │
└────────────────────────────────────────────────────────────────┘
         ▼                                            ▼
┌───────────────────────────┐         ┌──────────────────────────────┐
│   Planning Agent          │         │   Execution Agent            │
│   (Rule-Based)            │         │   (LLM-Powered)              │
├───────────────────────────┤         ├──────────────────────────────┤
│ • Query message logs      │         │ • Process flow plan          │
│ • Detect flow types       │         │ • Fetch all data             │
│   - DT_SubmitOrder        │         │   - Message logs             │
│   - Legacy_SubmitOrder    │         │   - Order tracking           │
│   - DT_InstallOptions     │         │   - Order header             │
│   - Legacy_InstallOptions │         │   - Order instances          │
│ • Match with known flows  │         │ • Query vector DB (optional) │
│ • Get expected docs       │         │ • Single LLM call            │
│ • Return ordered plan     │         │ • Return analysis            │
└───────────────────────────┘         └──────────────────────────────┘
         ▼                                            ▼
┌───────────────────────────┐         ┌──────────────────────────────┐
│  Knowledge Server         │         │  Database API Client         │
│  (File-Based Fallback)    │         │  (FastAPI Service)           │
├───────────────────────────┤         ├──────────────────────────────┤
│ • Static markdown docs    │         │ • CWMESSAGELOG               │
│ • Pre-generated content   │         │ • ORDER_TRACKING_INFO        │
│ • No LLM, no cost         │         │ • ORDER_ORDER_HEADER         │
│ • Fast lookup             │         │ • CWORDERINSTANCE            │
└───────────────────────────┘         └──────────────────────────────┘
                                                     ▼
                              ┌──────────────────────────────┐
                              │   Oracle Database (EOC)      │
                              ├──────────────────────────────┤
                              │ • CW schema tables           │
                              │ • ORDER schema tables        │
                              │ • Read-only access           │
                              └──────────────────────────────┘

         ┌────────────────────────────────────────────┐
         │  Vector Search (Optional - Config-Driven)  │
         ├────────────────────────────────────────────┤
         │ • Databricks Vector Search                 │
         │ • ~500 document chunks                     │
         │ • BGE-Large-EN embeddings                  │
         │ • Semantic similarity search               │
         │ • Cost: ~$0.0001/query                     │
         │ • Enabled via: ENABLE_VECTOR_SEARCH=true   │
         └────────────────────────────────────────────┘
```

---

## 🔄 Analysis Flow (User Asks Question)

### **Step 1: User Input**
```
User enters search criteria:
- user_data1 = "12345"
- user_data2 = "ORD-67890"
- user_data3 = "CUST-ABC"

User asks: "Why did the install type change?"
```

### **Step 2: Planning Phase (Rule-Based, ~100ms)**
```python
Planning Agent:
1. Query message logs via Database API
   GET /message_logs?user_data1=12345&user_data2=ORD-67890&limit=50
   → Returns 47 message logs, sorted by timestamp

2. Iterate through logs, detect known flow types:
   Log #1: operation="DT.TMF622Ext.Service:OMInterface/createOrder"
           → flow_type = "DT_SubmitOrder"
   
   Log #15: operation="OrderCare:InstallationConfiguration/getInstallOption"
            → flow_type = "Legacy_InstallOptions"
   
   Log #28: operation="CPQ.Services:confirmCustomerOrder/confirmCustomerOrder"
            → flow_type = "Legacy_SubmitOrder"

3. For each detected flow, get expected documentation:
   flow_type = "Legacy_InstallOptions"
   → Query Knowledge Server: get_process_flow_tool("InstallOptions")
   → Returns markdown documentation (file-based, no cost)

4. Build flow-based plan:
   {
     "order_context": {...},
     "flows": [
       {
         "sequence": 1,
         "flow_type": "DT_SubmitOrder",
         "operation": "DT.TMF622Ext.Service:OMInterface/createOrder",
         "timestamp": "2024-11-26 10:15:23",
         "msgid": "MSG-12345",
         "expected_flow_docs": "... detailed documentation ..."
       },
       {
         "sequence": 2,
         "flow_type": "Legacy_InstallOptions",
         ...
       }
     ]
   }

✅ Output: Structured plan with 3 detected flows
⏱️ Time: ~100ms
💰 Cost: $0 (no LLM, no vector DB yet)
```

### **Step 3: Execution Phase (Data Collection + LLM, ~3-5 seconds)**
```python
Execution Agent:
1. Extract search criteria from plan
   user_data1 = "12345"
   user_data2 = "ORD-67890"
   user_data3 = "CUST-ABC"

2. Fetch data from Database API:
   • Message logs (47 records) - includes SEND_DATA/RECEIVE_DATA BLOBs
   • Order tracking (2 records)
   • Order header (1 record)
   • Order instances (1 record)

3. For each flow, check if vector search is enabled:
   
   if config.app.enable_vector_search == true:
     # Semantic query (optional, ~$0.0001)
     query = "Legacy_InstallOptions workflow: expected steps, errors, timing"
     semantic_docs = vector_manager.search(query, num_results=5)
     
     if semantic_docs:
       ✅ Use rich cross-document context
     else:
       ⚠️  Fall back to expected_flow_docs from plan
   
   else:
     # Use file-based docs from plan (free)
     docs = flow['expected_flow_docs']

4. Build comprehensive analysis prompt:
   - Order context
   - Each flow with expected documentation
   - All collected data
   - Instructions for LLM

5. Single LLM call to Databricks Claude:
   prompt_size = ~15,000 chars
   response = llm.invoke(analysis_prompt)
   
✅ Output: Detailed analysis with root cause and recommendations
⏱️ Time: ~3-5 seconds
💰 Cost: ~$0.02 (LLM) + ~$0.0003 (3 vector queries if enabled)
```

### **Step 4: Response to User**
```
AI: **📊 Auto-Generated Analysis**

**Overall Flow Summary:**
The order went through 3 flows: DT_SubmitOrder → Legacy_InstallOptions → Legacy_SubmitOrder

**Flow-by-Flow Analysis:**

1. DT_SubmitOrder (2024-11-26 10:15:23)
   - Expected: Create order in DT system, return order ID
   - Actual: SUCCESS, order created with ID "ORD-67890"
   - Send data shows: install_type="FTTP"
   - Receive data shows: orderstatus="CREATED"

2. Legacy_InstallOptions (2024-11-26 10:16:45)
   - Expected: Calculate install options based on address
   - Actual: SUCCESS, but install_type CHANGED to "FTTN"
   - ⚠️ DEVIATION: Install type recalculation occurred
   - Reason: Address qualification returned different technology

3. Legacy_SubmitOrder (2024-11-26 10:17:12)
   - Expected: Commit order with final install type
   - Actual: SUCCESS with install_type="FTTN"
   - Order tracking shows: INSTALL_TYPE_CHANGE event logged

**Root Cause:**
The install type changed because the Legacy_InstallOptions flow performed
a recalculation based on address serviceability. The original DT_SubmitOrder
specified FTTP, but the address qualification engine returned FTTN as the
only available technology.

**Recommendations:**
1. Check address qualification database for this location
2. Verify if DT system should have caught this earlier
3. Consider pre-validating install types before DT order creation
```

---

## 💰 Cost Breakdown

### **Per Analysis (Single Question):**

| Operation | Time | Cost | Notes |
|-----------|------|------|-------|
| Planning (rule-based) | ~100ms | $0.00 | No LLM, no vector DB |
| Vector queries (optional, 3 flows) | ~300ms | $0.0003 | Only if enabled |
| LLM analysis (single call) | ~3s | $0.02 | Claude Sonnet 4 |
| **TOTAL** | **~3.4s** | **~$0.0203** | **Per question** |

### **Embedding Generation (User Clicks "🔄 Regen"):**

| Operation | Time | Cost | Notes |
|-----------|------|------|-------|
| Doc generation (GitLab → Markdown) | ~8-10 min | $0.00 | Local, no cloud |
| Embedding generation (~500 chunks) | ~2-3 min | $0.01 | Databricks BGE (free or minimal) |
| Vector index update | ~30s | $0.001 | One-time sync |
| **TOTAL** | **~10-15 min** | **~$0.01** | **User approval required** |

---

## 🎛️ Configuration

### **`.env` File:**

```bash
# ============================================================================
# VECTOR SEARCH CONFIGURATION (Optional)
# ============================================================================

# Enable/Disable vector search for semantic document retrieval
# ⚠️  This only controls QUERYING the vector DB (~$0.0001/query)
# ⚠️  Generating embeddings (~$0.01) always requires user approval via UI
# Set to false to always use file-based search (free, no costs)
ENABLE_VECTOR_SEARCH=false

# ============================================================================
# DATABRICKS CONFIGURATION (Required for LLM + Optional for Vector Search)
# ============================================================================

DATABRICKS_TOKEN=dapi-your-token-here
DATABRICKS_BASE_URL=https://dbc-4ee5e339-1e79.cloud.databricks.com/serving-endpoints/databricks-claude-sonnet-4
```

### **UI Status Indicators:**

```
┌─────────────────────────────────────────────────────────────┐
│ 🔍 EOC Log Analyzer  │ 📚 8 KB sections  │ 🔍 Vector ✅   │
│                      │                   │ 💻 GitLab ✅   │
│                      │                   │ v1.0.0         │
│                      │                   │ [🔄 Regen]     │
└─────────────────────────────────────────────────────────────┘
```

- **🔍 Vector ✅** = `ENABLE_VECTOR_SEARCH=true` in `.env`
- **🔍 Vector ⚠️** = `ENABLE_VECTOR_SEARCH=false` (file-based fallback)
- **💻 GitLab ✅** = `ENABLE_GITLAB=true` and credentials configured

---

## 🔄 Regeneration Flow (User Clicks "🔄 Regen")

### **Step 1: Confirmation Popup**
```
⚠️ Regenerate Documentation & Embeddings

This will:
1. 📚 Generate markdown documentation from GitLab code (free)
2. 🔢 Create vector embeddings (~$0.01 cost)
3. 📤 Update Databricks Vector Search index

Current Status:
- Existing docs: 8 files (230.5 KB)
- Vector search: ✅ Enabled (or ⚠️ Disabled)
- Estimated time: ~10 minutes

Note: This is a time-intensive process and incurs a small cost (~$0.01).
Querying the vector DB during analysis is separate (controlled by config).

[✅ Yes, Regenerate]  [❌ Cancel]
```

### **Step 2: User Clicks "✅ Yes, Regenerate"**
```python
# Runs in background subprocess
python tools\knowledge_server\regenerate_embeddings.py

# What happens:
1. Doc Generation (8-10 min):
   - Fetch XML files from GitLab
   - Parse Cordys metadata
   - Generate 8 markdown files with LLM
   - Save to tools/knowledge_server/docs/

2. Embedding Generation (2-3 min):
   - Load markdown files
   - Chunk into ~500 pieces (1000 chars, 200 overlap)
   - Generate embeddings (Databricks BGE-Large-EN)

3. Index Update (30 sec):
   - Connect to Databricks Vector Search
   - Upsert all chunks to index
   - Wait for sync

✅ Total: ~10-15 minutes, ~$0.01 cost
```

### **Step 3: Result**
```
✅ Documentation & embeddings regenerated successfully!
[Balloons animation]

Knowledge Server reloaded with fresh content.
```

---

## 🚦 Flow Decision Logic

### **When Vector Search is Used:**

```python
# In knowledge_tools.py

def search_knowledge_base(query: str) -> Optional[str]:
    # Check config flag
    if not config.app.enable_vector_search:
        logger.debug("Vector search disabled, using file-based fallback")
        return None  # → Falls back to file-based
    
    # Try vector search
    vector_mgr = get_vector_manager()  # Lazy init, only if needed
    
    if vector_mgr:
        results = vector_mgr.search(query, num_results=5, score_threshold=0.5)
        
        if results:
            logger.debug(f"✅ Vector search returned {len(results)} results")
            return combined_content  # → Use vector search results
        else:
            logger.debug("⚠️ No vector matches")
            return None  # → Falls back to file-based
    
    return None  # → Falls back to file-based
```

### **Fallback Hierarchy:**

```
1st Choice: Vector Search (if enabled + available)
            ↓ (if disabled, unavailable, or no matches)
2nd Choice: File-Based Search (knowledge_server.mcp_server)
            ↓ (if docs not generated)
3rd Choice: "Context not available" message
            → Analysis continues with available data only
```

---

## 📋 Key Features

### ✅ **Cost-Aware Design**

1. **No operations on app startup** - Zero cost until user acts
2. **Config-driven vector search** - Can be disabled to avoid query costs
3. **User approval for embeddings** - Popup confirmation before expensive operation
4. **Single LLM call** - Minimizes LLM costs per analysis

### ✅ **Performance Optimized**

1. **Rule-based flow detection** - No LLM needed, <100ms
2. **Lazy initialization** - Vector manager only created when needed
3. **Graceful degradation** - Always falls back to file-based
4. **Parallel data fetching** - All DB queries at once

### ✅ **Clean Logging**

```
🔍 Planning: Detecting flows from message logs...
📦 Found 47 message logs
✅ Detected 3 flows: DT_SubmitOrder → Legacy_InstallOptions → Legacy_SubmitOrder

▶️  Execution: Analyzing 3 detected flows
📊 Fetching message logs (47 found)
📊 Fetching order tracking (2 found)
🤖 Sending LLM request (15234 chars)
✅ LLM analysis complete (2456 chars)

✅ Coordinator: Analysis completed successfully
```

**No more:**
- ❌ Verbose agent iterations
- ❌ Tool call JSON dumps
- ❌ LangChain debugging output

---

## 🎯 Summary

**The system uses:**

1. **Rule-based flow detection** (Planning Agent)
   - Fast, deterministic, zero-cost
   - Detects 4 known flow types
   - Returns structured plan with expected docs

2. **Optional vector search** (Execution Agent)
   - Config flag: `ENABLE_VECTOR_SEARCH`
   - Only if enabled: semantic context retrieval
   - Falls back to file-based if disabled/unavailable

3. **Single LLM call** (Execution Agent)
   - Comprehensive prompt with all data
   - One analysis per question (~$0.02)
   - Rich cross-document context (if vector enabled)

4. **User-controlled embedding generation**
   - Only via "🔄 Regen" button
   - Requires explicit confirmation
   - ~$0.01 cost, ~10-15 minutes

**Result:** Fast, cost-effective, semantically-aware log analysis! 🚀

