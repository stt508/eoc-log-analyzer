# 🔧 EOC Log Analyzer - Tools Reference

## Overview

This document lists **all available tools** after cleanup (removed 11 unused methods).

---

## 📊 **Tools Summary Table**

| Category | Tool Name | Purpose | Input Parameters | Used By |
|----------|-----------|---------|------------------|---------|
| **Knowledge Server** | `query_services` | Search service catalog | `search_term` (optional) | Agents (if using LangChain tools) |
| **Knowledge Server** | `get_api_contract` | Get API contract details | `service_name` | Agents (if using LangChain tools) |
| **Knowledge Server** | `get_process_flow` | Get business process flow | `process_name` | **Planning Agent (direct call)** |
| **Knowledge Server** | `search_documentation` | Natural language doc search | `query` | Agents (if using LangChain tools) |
| **Knowledge Server** | `get_system_overview` | Get system architecture | None | Agents (if using LangChain tools) |
| **Knowledge Server** | `get_error_handling_info` | Get error handling patterns | None | Agents (if using LangChain tools) |
| **Database API** | `search_message_logs` | Search CWMESSAGELOG | Multiple criteria | **Planning & Execution Agents** |
| **Database API** | `search_orders` | Search ORDER_ORDER_HEADER | Multiple criteria | **Execution Agent** |
| **Database API** | `search_order_tracking` | Search ORDER_TRACKING_INFO | Multiple criteria | **Execution Agent** |
| **Database API** | `search_order_instances` | Search CWORDERINSTANCE | Multiple criteria | **Execution Agent** |

---

## 📚 **Knowledge Server Tools (6 total)**

### **1. `query_services`**

**Purpose:** Search the service catalog for services

**Function:** `query_services_tool(search_term: str = "") -> str`

**Parameters:**
- `search_term` (optional): Service name or description
  - Example: `"ManageOrder"`, `"customer order services"`

**Returns:** JSON with matching services

**Tech:** Vector search (if enabled) → File-based fallback

**Usage Status:** ⚠️ Defined but not actively used (direct calls preferred)

---

### **2. `get_api_contract`**

**Purpose:** Get API contract details for a service

**Function:** `get_api_contract_tool(service_name: str = "") -> str`

**Parameters:**
- `service_name`: Service name
  - Example: `"ManageOrder"`, `"order submission API"`

**Returns:** Request/response structures, parameters, error codes

**Tech:** Vector search → File-based fallback

**Usage Status:** ⚠️ Defined but not actively used

---

### **3. `get_process_flow`**

**Purpose:** Get business process flow details

**Function:** `get_process_flow_tool(process_name: str = "") -> str`

**Parameters:**
- `process_name`: Process/flow name
  - Example: `"InstallOptions"`, `"OM.quoteToOrder"`, `"CustomerOrderManagement:CustomerOrderManagement/CommitCustomerOrder"`

**Returns:** Expected steps, behavior, timing, common errors

**Tech:** Vector search → File-based fallback

**Usage Status:** ✅ **ACTIVELY USED by Planning Agent**

**Note:** This is the most important Knowledge Server tool!

---

### **4. `search_documentation`**

**Purpose:** Natural language search across all documentation

**Function:** `search_documentation_tool(query: str) -> str`

**Parameters:**
- `query`: Natural language question
  - Example: `"How does install type recalculation work?"`, `"validation errors"`

**Returns:** Relevant documentation sections

**Tech:** Vector search → File-based fallback

**Usage Status:** ⚠️ Defined but not actively used

---

### **5. `get_system_overview`**

**Purpose:** Get high-level system architecture

**Function:** `get_system_overview_tool(_: str = "") -> str`

**Parameters:** None (empty string placeholder)

**Returns:** System overview documentation

**Tech:** Vector search → File-based fallback

**Usage Status:** ⚠️ Defined but not actively used

---

### **6. `get_error_handling_info`**

**Purpose:** Get error handling patterns

**Function:** `get_error_handling_info_tool(_: str = "") -> str`

**Parameters:** None (empty string placeholder)

**Returns:** Common errors, error codes, resolution steps

**Tech:** Vector search → File-based fallback

**Usage Status:** ⚠️ Defined but not actively used

---

## 🗄️ **Database API Client Methods (4 core search methods)**

### **1. `search_message_logs`**

**Purpose:** Search CWMESSAGELOG table for message logs

**Function:** `api_client.search_message_logs(...) -> List[Dict[str, Any]]`

**Parameters:**
```python
user_data1: Optional[str] = None          # Primary identifier
user_data2: Optional[str] = None          # Secondary identifier
user_data3: Optional[str] = None          # Tertiary identifier
order_id: Optional[str] = None            # Order ID
customer_id: Optional[str] = None         # Customer ID
operation: Optional[str] = None           # Operation name
start_date: Optional[str] = None          # Start date (ISO)
end_date: Optional[str] = None            # End date (ISO)
limit: int = 50                           # Max results
include_blob_data: bool = False           # Include SEND_DATA/RECEIVE_DATA
```

**Returns:** List of message log dictionaries

**Usage Status:** ✅ **ACTIVELY USED by Planning & Execution Agents**

**Example:**
```python
logs = api_client.search_message_logs(
    user_data1="12345",
    user_data2="ORD-67890",
    limit=50,
    include_blob_data=True
)
```

---

### **2. `search_orders`**

**Purpose:** Search ORDER_ORDER_HEADER table for order headers

**Function:** `api_client.search_orders(...) -> List[Dict[str, Any]]`

**Parameters:**
```python
cworderid: Optional[str] = None           # CW Order ID
omorderid: Optional[str] = None           # OM Order ID
quoteid: Optional[str] = None             # Quote ID
telephonenumber: Optional[str] = None     # Phone number
universalserviceid: Optional[str] = None  # Service ID
ordertype: Optional[str] = None           # Order type
stagecode: Optional[str] = None           # Stage code
start_date: Optional[str] = None          # Start date (ISO)
end_date: Optional[str] = None            # End date (ISO)
limit: int = 50                           # Max results
include_blob_data: bool = False           # Include NCLOBs
```

**Returns:** List of order header dictionaries

**Usage Status:** ✅ **ACTIVELY USED by Execution Agent**

**Example:**
```python
orders = api_client.search_orders(
    cworderid="ORD-12345",
    limit=5,
    include_blob_data=False
)
```

---

### **3. `search_order_tracking`**

**Purpose:** Search ORDER_TRACKING_INFO table for tracking records

**Function:** `api_client.search_order_tracking(...) -> List[Dict[str, Any]]`

**Parameters:**
```python
cworderid: Optional[str] = None           # CW Order ID
orderid: Optional[str] = None             # Order ID
workid: Optional[str] = None              # Work ID
scaseid: Optional[str] = None             # SCASE ID
icaseid: Optional[str] = None             # ICASE ID
orderstatus: Optional[str] = None         # Order status
casestatus: Optional[str] = None          # Case status
flowstatus: Optional[str] = None          # Flow status
has_errors: Optional[bool] = None         # Filter by errors (13+ fields)
start_date: Optional[str] = None          # Start date (ISO)
end_date: Optional[str] = None            # End date (ISO)
limit: int = 50                           # Max results
include_blob_data: bool = False           # Include error messages
```

**Returns:** List of tracking record dictionaries

**Usage Status:** ✅ **ACTIVELY USED by Execution Agent**

**Example:**
```python
tracking = api_client.search_order_tracking(
    cworderid="ORD-12345",
    limit=5,
    include_blob_data=True
)
```

---

### **4. `search_order_instances`**

**Purpose:** Search CWORDERINSTANCE table for order instances

**Function:** `api_client.search_order_instances(...) -> List[Dict[str, Any]]`

**Parameters:**
```python
cwdocid: Optional[str] = None             # Document ID
customerid: Optional[str] = None          # Customer ID
accountid: Optional[str] = None           # Account ID
ordertype: Optional[str] = None           # Order type
ordersubtype: Optional[str] = None        # Order subtype
status: Optional[str] = None              # Status (single char)
state: Optional[str] = None               # Order state
quoteid: Optional[str] = None             # Quote ID
externalorderid: Optional[str] = None     # External Order ID
productcode: Optional[str] = None         # Product code
parentorder: Optional[str] = None         # Parent order ID
start_date: Optional[str] = None          # Start date (ISO)
end_date: Optional[str] = None            # End date (ISO)
limit: int = 50                           # Max results
include_blob_data: bool = False           # Include NCLOBs
```

**Returns:** List of order instance dictionaries

**Usage Status:** ✅ **ACTIVELY USED by Execution Agent**

**Example:**
```python
instances = api_client.search_order_instances(
    cwdocid="DOC-12345",
    limit=5,
    include_blob_data=False
)
```

---

## 🎯 **Tool Usage by Agent**

### **Planning Agent**
```python
# Direct calls (not using LangChain tools)

# 1. Search message logs
logs = api_client.search_message_logs(
    user_data1=user_data1,
    user_data2=user_data2,
    user_data3=user_data3,
    limit=50
)

# 2. Get expected documentation for detected flows
docs = get_process_flow_tool(flow_type)  # e.g., "InstallOptions"
```

**Why direct calls?**
- ✅ Faster (no LangChain overhead)
- ✅ Lower LLM token usage
- ✅ Full control over data flow

---

### **Execution Agent**
```python
# Direct calls (not using LangChain tools)

# 1. Get message logs
message_logs = api_client.search_message_logs(
    user_data1=user_data1,
    user_data2=user_data2,
    user_data3=user_data3,
    limit=50,
    include_blob_data=True
)

# 2. Get order tracking
order_tracking = api_client.search_order_tracking(
    cworderid=extracted_cworderid,
    limit=5,
    include_blob_data=True
)

# 3. Get order header
order_header = api_client.search_orders(
    cworderid=extracted_cworderid,
    limit=5,
    include_blob_data=False
)

# 4. Get order instances
order_instances = api_client.search_order_instances(
    cwdocid=extracted_cworderid,
    limit=5,
    include_blob_data=False
)

# 5. Optional: Vector search for semantic context
if config.app.enable_vector_search:
    semantic_docs = search_knowledge_base(query)
```

---

## ⚠️ **Important Notes**

### **1. LangChain Tools vs Direct Calls**

**LangChain Tools (Defined but unused):**
- 6 Knowledge Server tools in `KNOWLEDGE_TOOLS` array
- Wrapper functions exist but agents don't use them

**Direct Calls (Actively used):**
- 4 Database API methods
- 1 Knowledge Server function (`get_process_flow_tool`)
- 1 Optional vector search (`search_knowledge_base`)

**Why?**
- ✅ Direct calls = faster execution
- ✅ No agent iteration overhead
- ✅ Lower LLM costs (fewer tokens)
- ✅ Full control over when/how data is fetched

---

### **2. Vector Search Behavior**

**If `ENABLE_VECTOR_SEARCH=true`:**
```python
1. Try vector search first (semantic similarity)
2. If no matches → Fall back to file-based search
3. If file-based fails → Return "Context not available"
```

**If `ENABLE_VECTOR_SEARCH=false`:**
```python
1. Use file-based search directly
2. If fails → Return "Context not available"
```

**Result:** Analysis never fails due to missing context!

---

### **3. BLOB/NCLOB Data**

**What is it?**
- `SEND_DATA` / `RECEIVE_DATA` in CWMESSAGELOG
- Error messages in ORDER_TRACKING_INFO
- Various NCLOBs in other tables

**When to include?**
- `include_blob_data=True` → Retrieves and base64 decodes
- `include_blob_data=False` → Skips for faster queries

**LLM Usage:**
- LLM decodes base64 to understand request/response payloads
- Looks for keywords: "install_type", "orderstatus", "error", "failure"

---

## 🔗 **Tool Wrapper Functions (Optional)**

**Location:** Bottom of `database_api_client.py`

These exist for potential future use with LangChain agents:

```python
# Message logs
search_message_logs_tool(search_criteria: str) -> str

# Orders
search_orders_tool(search_criteria: str) -> str

# Order tracking
search_order_tracking_tool(search_criteria: str) -> str

# Order instances
search_order_instances_tool(search_criteria: str) -> str
```

**Status:** ⚠️ Defined but not actively used

---

## 📋 **Quick Reference Card**

| **Need to...** | **Use this tool** | **Agent** |
|----------------|-------------------|-----------|
| Find message logs | `api_client.search_message_logs()` | Planning, Execution |
| Detect flows | Rule-based matching (no tool) | Planning |
| Get expected docs | `get_process_flow_tool()` | Planning |
| Get order tracking | `api_client.search_order_tracking()` | Execution |
| Get order header | `api_client.search_orders()` | Execution |
| Get order instances | `api_client.search_order_instances()` | Execution |
| Semantic search | `search_knowledge_base()` (optional) | Execution |
| Analyze with LLM | `llm.invoke()` (single call) | Execution |

---

## ✅ **Summary**

**Total Tools:**
- 6 Knowledge Server tools (LangChain format, mostly unused)
- 4 Database API search methods (actively used)
- 4 Optional tool wrappers (for future LangChain use)

**Actively Used:**
- ✅ `search_message_logs` (Planning + Execution)
- ✅ `search_orders` (Execution)
- ✅ `search_order_tracking` (Execution)
- ✅ `search_order_instances` (Execution)
- ✅ `get_process_flow_tool` (Planning)
- ✅ `search_knowledge_base` (Execution, if enabled)

**Design Philosophy:**
- Direct calls for speed and control
- Tools defined for future flexibility
- Graceful fallback at every step
- No failures due to missing context

**Cost per analysis:** ~$0.02 (LLM) + ~$0.0003 (vector search if enabled)

