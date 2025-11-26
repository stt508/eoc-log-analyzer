---
**Auto-Generated Documentation**  
Generated: 2025-11-25T15:41:11.325404  
Branch: master  
Path: Trunk/FrontierOM  
**⚠️ Do not edit directly - regenerate from code**
---


# AI Agent Quick Reference

Quick guide for AI agents using this documentation.

---

## 🎯 Troubleshooting Workflow

```
1. User Question → Identify order issue
2. Expected Flow → What SHOULD happen? (see Expected Flows)
3. Database Query → What DID happen? (query ORDER_*, CWMESSAGELOG)
4. Compare → Where did they differ?
5. Fetch Code → Get implementation (use file paths)
6. Analyze → Why did it differ?
7. Report → Root cause and recommendation
```

---

## 📂 Documentation Structure

| Document | Purpose | When to Use |
|----------|---------|-------------|
| **System Overview** | High-level architecture | Understanding system structure |
| **Service Catalog** | All services with paths | Finding code to fetch |
| **Expected Flows** | What SHOULD happen | Comparing expected vs actual |
| **API Contracts** | Inputs/outputs | Understanding API behavior |
| **Error Handling** | Error patterns | Interpreting error codes |
| **Component Map** | System layers | Understanding interactions |

---

## 🔧 Available Tools

### Database Query Tools

- `search_message_logs(criteria)` - Query CWMESSAGELOG
- `search_orders(criteria)` - Query ORDER_ORDER_HEADER  
- `search_order_tracking(criteria)` - Query ORDER_TRACKING_INFO
- `search_order_instances(criteria)` - Query CWORDERINSTANCE

### Code Fetch Tools

- `get_file_content(path)` - Fetch specific file from GitLab
- `search_code(query)` - Search for code patterns
- `search_by_filename(name)` - Find file by name

---

## 💡 Best Practices

1. **Start with Expected Flow** → Know what should happen
2. **Query Database** → See what actually happened
3. **Compare** → Find the deviation point
4. **Only fetch code if needed** → Don't fetch unless unclear
5. **Use file paths from docs** → Exact paths provided

---

## 📝 Example Analysis

```
User: "Why did order 12345 fail?"

Step 1: Check Expected Flow
→ new_order_flow: Step 4 = "OrderOrchestrator routes to DPI"

Step 2: Query Database
→ dpierrorid_ia = 'E503' (Service Unavailable)

Step 3: Compare
→ Expected: DPI returns 200 OK
→ Actual: DPI returned 503

Step 4: Check Error Handling
→ E503 = Should retry 3 times

Step 5: Verify Retry
→ Query: SELECT attemptcount WHERE operation='SendToDPI'
→ Result: attemptcount = 3 ✓

Step 6: Conclusion
→ Root Cause: DPI service was down
→ System Behavior: Correct (retried as expected)
→ Recommendation: Check DPI service status

Step 7: Optional Code Fetch (if needed)
→ get_file_content("path/to/DPIIntegrationService.java")
→ Verify: max_retries = 3 ✓
```

---

**Generated:** 2025-11-25T15:41:11.325404
