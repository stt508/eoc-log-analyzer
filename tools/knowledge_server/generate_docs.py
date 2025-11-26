#!/usr/bin/env python3
"""
Generate Wiki Documentation for EOC Order Care System
Outputs separate markdown files ready for wiki upload
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
from loguru import logger
import sys

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tools.knowledge_server.code_documentation_generator import doc_generator
from config import config

def generate_wiki_markdown_files(output_dir: Path, docs: dict):
    """Generate separate markdown files for wiki upload"""
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    generated_files = []
    generation_time = docs.get('generated_at', datetime.now().isoformat())
    branch = docs.get('branch', 'master')
    base_path = docs.get('base_path', 'Trunk/FrontierOM')
    
    # Common header for all pages
    common_header = f"""---
**Auto-Generated Documentation**  
Generated: {generation_time}  
Branch: {branch}  
Path: {base_path}  
**⚠️ Do not edit directly - regenerate from code**
---

"""
    
    # 1. Home Page / Index
    home_content = f"""{common_header}
# EOC Order Care - System Documentation

## 📚 Documentation Index

This documentation is automatically generated from the EOC Order Care codebase to help developers and AI agents understand the system's expected behavior.

### 📖 Available Documentation

1. **[System Overview](./01-System-Overview.md)** - High-level architecture and components
2. **[Service Catalog](./02-Service-Catalog.md)** - All services with file paths
3. **[Expected Flows](./03-Expected-Flows.md)** - Step-by-step order processing flows
4. **[API Contracts](./04-API-Contracts.md)** - Expected inputs/outputs for APIs
5. **[Error Handling](./05-Error-Handling.md)** - Error patterns and recovery
6. **[Component Map](./06-Component-Map.md)** - Component interactions and relationships

---

## 🤖 For AI Agents

When troubleshooting an order issue:

1. **Check Expected Flow** → What SHOULD have happened?
2. **Query Database** → What ACTUALLY happened?
3. **Compare** → Where did they differ?
4. **Fetch Code** → Use file paths to get specific implementation details

### GitLab Code Access

All documentation includes file paths. To fetch code:

```python
# Use the file path from documentation
get_file_content("path/to/Service.java")
```

---

## 🔄 Last Updated

{generation_time}

**Regeneration:** This documentation is regenerated automatically when code changes.
"""
    
    home_file = output_dir / "00-Home.md"
    home_file.write_text(home_content, encoding='utf-8')
    generated_files.append(home_file)
    logger.info(f"✅ Generated: {home_file.name}")
    
    # 2. System Overview
    overview_content = f"""{common_header}
# System Overview

{docs.get('system_overview', 'Not available')}

---

## 🔗 Related Documentation

- [Service Catalog](./02-Service-Catalog.md) - Detailed service information
- [Component Map](./06-Component-Map.md) - Component relationships

---

## 📂 Key Directories

Based on the codebase structure, the main directories are:

```
{base_path}/
├── controllers/    - REST endpoints and request handlers
├── services/       - Business logic and orchestration
├── models/         - Data models and DTOs
├── repositories/   - Data access layer
└── integration/    - External system integrations
```

---

**Need implementation details?** Use `get_file_content(path)` with paths from [Service Catalog](./02-Service-Catalog.md).
"""
    
    overview_file = output_dir / "01-System-Overview.md"
    overview_file.write_text(overview_content, encoding='utf-8')
    generated_files.append(overview_file)
    logger.info(f"✅ Generated: {overview_file.name}")
    
    # 3. Service Catalog with File Paths
    service_catalog = docs.get('service_catalog', {})
    
    catalog_content = f"""{common_header}
# Service Catalog

Complete catalog of services with file paths for code access.

---

## 📋 All Services

"""
    
    for service_name, service_data in sorted(service_catalog.items()):
        file_path = service_data.get('file_path', 'N/A')
        file_name = service_data.get('file_name', 'N/A')
        responsibility = service_data.get('responsibility', 'N/A')
        layer = service_data.get('layer', 'N/A')
        
        catalog_content += f"""
### {service_name}

**Responsibility:** {responsibility}  
**Layer:** {layer}  
**File:** `{file_name}`  
**Path:** `{file_path}`  

**To fetch code:**
```python
get_file_content("{file_path}")
```

---

"""
    
    catalog_content += """
## 🤖 Agent Usage

When you need to see implementation details:

1. Find the service in this catalog
2. Copy the file path
3. Use `get_file_content(path)` to fetch the code
4. Analyze the implementation

**Example:**
```python
# Need to see OrderService implementation?
code = get_file_content("path/to/OrderService.java")
```
"""
    
    catalog_file = output_dir / "02-Service-Catalog.md"
    catalog_file.write_text(catalog_content, encoding='utf-8')
    generated_files.append(catalog_file)
    logger.info(f"✅ Generated: {catalog_file.name}")
    
    # 4. Expected Flows with File References
    flows = docs.get('expected_flows', {})
    
    flows_content = f"""{common_header}
# Expected Order Flows

Step-by-step flows showing what SHOULD happen in the system.

**For Troubleshooting:**
- Compare actual behavior (from logs/database) to expected flow
- Identify where deviation occurred
- Use file paths to investigate specific step implementations

---

"""
    
    for flow_name, flow_data in flows.items():
        description = flow_data.get('description', 'No description')
        steps = flow_data.get('steps', [])
        success_criteria = flow_data.get('success_criteria', 'Not specified')
        failure_points = flow_data.get('failure_points', [])
        related_files = flow_data.get('related_files', [])
        
        flows_content += f"""
## {flow_name.replace('_', ' ').title()}

**Description:** {description}

### Flow Steps

| Step | Component | Action | Expected Result | File |
|------|-----------|--------|----------------|------|
"""
        
        for step in steps:
            step_num = step.get('step', '?')
            component = step.get('component', 'Unknown')
            action = step.get('action', 'N/A')
            expected = step.get('expected', 'N/A')
            file_path = step.get('file', 'N/A')
            
            flows_content += f"| {step_num} | **{component}** | {action} | {expected} | `{file_path}` |\n"
        
        flows_content += f"""

**Success Criteria:** {success_criteria}

**Known Failure Points:** {', '.join(failure_points)}

### Related Code Files

"""
        if related_files:
            for file_info in related_files:
                file_name = file_info.get('file_name', 'N/A')
                file_path = file_info.get('file_path', 'N/A')
                flows_content += f"- `{file_name}` → `get_file_content(\"{file_path}\")`\n"
        else:
            flows_content += "_No related files identified_\n"
        
        flows_content += "\n---\n"
    
    flows_content += """
## 🤖 Troubleshooting Guide

When analyzing an order issue:

1. **Identify the relevant flow** (e.g., new_order_flow, order_modification_flow)
2. **Check what step failed** (from ORDER_TRACKING_INFO or CWMESSAGELOG)
3. **Compare to expected behavior** (from table above)
4. **Fetch the code** for that step (use file path from table)
5. **Analyze the implementation** to understand why it deviated

**Example:**
```
Issue: Order failed at step 4
Expected: OrderOrchestrator → DPI → Success
Actual: OrderOrchestrator → DPI → Error 503
Action: Fetch OrderOrchestrator.java to see retry logic
```
"""
    
    flows_file = output_dir / "03-Expected-Flows.md"
    flows_file.write_text(flows_content, encoding='utf-8')
    generated_files.append(flows_file)
    logger.info(f"✅ Generated: {flows_file.name}")
    
    # 5. API Contracts
    api_contracts = docs.get('api_contracts', {})
    
    api_content = f"""{common_header}
# API Contracts

Expected inputs, outputs, and status codes for system APIs.

---

"""
    
    for contract_name, contract_data in api_contracts.items():
        api_content += f"""
## {contract_name.replace('_', ' ').title()}

"""
        for key, value in contract_data.items():
            if isinstance(value, dict):
                api_content += f"**{key.title()}:**\n"
                for k, v in value.items():
                    api_content += f"- {k}: {v}\n"
            elif isinstance(value, list):
                api_content += f"**{key.title()}:** {', '.join(map(str, value))}\n"
            else:
                api_content += f"**{key.title()}:** {value}\n"
        
        api_content += "\n---\n"
    
    api_file = output_dir / "04-API-Contracts.md"
    api_file.write_text(api_content, encoding='utf-8')
    generated_files.append(api_file)
    logger.info(f"✅ Generated: {api_file.name}")
    
    # 6. Error Handling
    error_handling = docs.get('error_handling', 'Not available')
    
    error_content = f"""{common_header}
# Error Handling Patterns

Understanding error codes, retry logic, and recovery patterns.

---

{error_handling}

---

## 🔍 Troubleshooting with Error Codes

When you see an error code:

1. Find the error in the tables above
2. Understand what it means
3. Check if retry is expected
4. Verify actual behavior matches expected behavior
5. If implementation unclear, fetch the error handling code

**Example:**
```
Error: DPIERRORID_IA = "E503"
Expected: Service Unavailable → Retry 3 times
Verify: Check ATTEMPTCOUNT in CWMESSAGELOG
If wrong: Fetch DPIIntegrationService.java to see retry logic
```
"""
    
    error_file = output_dir / "05-Error-Handling.md"
    error_file.write_text(error_content, encoding='utf-8')
    generated_files.append(error_file)
    logger.info(f"✅ Generated: {error_file.name}")
    
    # 7. Component Map
    component_map = docs.get('component_map', {})
    
    component_content = f"""{common_header}
# Component Map

System architecture layers and component interactions.

---

"""
    
    for layer_name, layer_data in component_map.items():
        component_content += f"""
## {layer_name.replace('_', ' ').title()}

"""
        if 'components' in layer_data:
            component_content += "**Components:**\n"
            for comp in layer_data['components']:
                component_content += f"- {comp}\n"
        
        if 'responsibility' in layer_data:
            component_content += f"\n**Responsibility:** {layer_data['responsibility']}\n"
        
        if 'interacts_with' in layer_data:
            component_content += f"\n**Interacts With:** {', '.join(layer_data['interacts_with'])}\n"
        
        if 'tables' in layer_data:
            component_content += f"\n**Database Tables:**\n"
            for table in layer_data['tables']:
                component_content += f"- {table}\n"
        
        if 'systems' in layer_data:
            component_content += f"\n**External Systems:**\n"
            for system in layer_data['systems']:
                component_content += f"- {system}\n"
        
        if 'integration_type' in layer_data:
            component_content += f"\n**Integration Type:** {layer_data['integration_type']}\n"
        
        if 'error_handling' in layer_data:
            component_content += f"\n**Error Handling:** {layer_data['error_handling']}\n"
        
        component_content += "\n---\n"
    
    component_content += """
## 🤖 Understanding System Flow

Use this component map to understand:

1. **Which layer handles what** (presentation, business logic, data access)
2. **How components interact** (who calls who)
3. **Where to look for issues** (which layer likely has the problem)

When troubleshooting, identify which layer the issue is in, then fetch code from that layer's components.
"""
    
    component_file = output_dir / "06-Component-Map.md"
    component_file.write_text(component_content, encoding='utf-8')
    generated_files.append(component_file)
    logger.info(f"✅ Generated: {component_file.name}")
    
    # 8. Agent Quick Reference
    agent_ref_content = f"""{common_header}
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

**Generated:** {generation_time}
"""
    
    agent_ref_file = output_dir / "07-Agent-Quick-Reference.md"
    agent_ref_file.write_text(agent_ref_content, encoding='utf-8')
    generated_files.append(agent_ref_file)
    logger.info(f"✅ Generated: {agent_ref_file.name}")
    
    return generated_files


def main():
    parser = argparse.ArgumentParser(description="Generate wiki-ready markdown documentation")
    parser.add_argument("--branch", default="master", help="GitLab branch to analyze")
    parser.add_argument("--base-path", default="Trunk/FrontierOM", help="Base path in repository")
    parser.add_argument("--output", default="wiki_docs", help="Output directory for markdown files")
    parser.add_argument("--force", action="store_true", help="Force regeneration")
    
    args = parser.parse_args()
    
    # Check GitLab configuration
    if not config.has_gitlab():
        logger.error("❌ GitLab not configured!")
        logger.error("Set GITLAB_URL, GITLAB_TOKEN, GITLAB_PROJECT_ID in .env")
        logger.error("Set ENABLE_GITLAB=true in .env")
        return 1
    
    logger.info("🚀 Generating wiki documentation...")
    logger.info(f"   Branch: {args.branch}")
    logger.info(f"   Path: {args.base_path}")
    logger.info(f"   Output: {args.output}/")
    
    # Generate documentation
    try:
        docs = doc_generator.generate_documentation(
            branch=args.branch,
            base_path=args.base_path
        )
        
        if "error" in docs:
            logger.error(f"❌ Generation failed: {docs['error']}")
            return 1
        
        # Generate markdown files
        output_dir = Path(args.output)
        generated_files = generate_wiki_markdown_files(output_dir, docs)
        
        logger.info(f"✅ Generated {len(generated_files)} markdown files")
        logger.info(f"📁 Output directory: {output_dir.absolute()}")
        
        # Print file list
        print("\n" + "="*60)
        print("WIKI DOCUMENTATION FILES GENERATED")
        print("="*60)
        for file in generated_files:
            print(f"✅ {file.name}")
        print("="*60)
        print(f"\n📂 Location: {output_dir.absolute()}")
        print("\n🚀 Next Steps:")
        print("   1. Review the files in wiki_docs/")
        print("   2. Upload to your wiki server")
        print("   3. Agents will reference these docs + fetch code as needed")
        print("="*60)
        
        return 0
        
    except Exception as e:
        logger.error(f"❌ Failed to generate documentation: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())

