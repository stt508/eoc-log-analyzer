"""
Code Documentation Generator
Generates LLM-friendly documentation from codebase for troubleshooting context
"""

import json
import re
import sys
from typing import Dict, List, Any, Optional
from datetime import datetime
from collections import defaultdict
from pathlib import Path
from loguru import logger

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tools.gitlab_integration import gitlab_client
from tools.knowledge_server.cordys_xml_parser import cordys_parser

class CodeDocumentationGenerator:
    """Generate structured documentation from codebase for LLM context"""
    
    def __init__(self):
        self.documentation: Dict[str, Any] = {}
        self.last_generated: Optional[datetime] = None
        
    def generate_documentation(self, branch: str = "master", base_path: str = "Trunk/FrontierOM") -> Dict[str, Any]:
        """
        Generate comprehensive documentation from Cordys/OpenText BPM codebase
        
        Parses XML metadata files to extract:
        - Services and interfaces
        - Business processes and workflows
        - Data entities and database mappings
        - Integration points
        - Business logic scripts
        """
        
        try:
            logger.info(f"Generating documentation from {branch}/{base_path}...")
            
            # Get all XML files from GitLab
            all_files = gitlab_client.list_repository_files(path=base_path, ref=branch)
            
            if not all_files:
                return {"error": "No files found"}
            
            xml_files = [f for f in all_files if f.get('path', '').endswith('.xml')]
            
            logger.info(f"Found {len(xml_files)} XML files. Parsing metadata...")
            
            # Parse ALL XML files - NO SAMPLING - comprehensive documentation
            logger.info(f"📖 COMPREHENSIVE MODE: Parsing ALL {len(xml_files)} XML files...")
            logger.info("⏰ This will take time, but will provide complete documentation for AI analysis")
            parsed_data = self._parse_xml_files(xml_files, branch, max_files=999999)  # No limit
            
            # Organize parsed data by type and module
            organized_data = self._organize_parsed_data(parsed_data)
            
            # Generate documentation sections
            self.documentation = {
                "generated_at": datetime.now().isoformat(),
                "branch": branch,
                "base_path": base_path,
                "total_files": len(xml_files),
                "parsed_files": len(parsed_data),
                "system_overview": self._generate_cordys_system_overview(organized_data),
                "service_catalog": self._generate_cordys_service_catalog(organized_data),
                "api_contracts": self._generate_cordys_api_contracts(organized_data),
                "expected_flows": self._generate_cordys_expected_flows(organized_data),
                "error_handling": self._generate_cordys_error_handling(organized_data),
                "component_map": self._generate_cordys_component_map(organized_data),
                "data_entities": self._generate_cordys_data_entities(organized_data),
                "integration_points": self._generate_cordys_integration_points(organized_data)
            }
            
            self.last_generated = datetime.now()
            
            logger.info("✅ Documentation generated successfully")
            
            return self.documentation
            
        except Exception as e:
            logger.error(f"Failed to generate documentation: {e}")
            return {"error": str(e)}
    
    def get_documentation_summary(self) -> str:
        """Get a concise summary of documentation for LLM context"""
        
        if not self.documentation:
            return "No documentation available. Code context not loaded."
        
        summary_parts = [
            "=== EOC ORDER CARE SYSTEM DOCUMENTATION ===",
            f"Generated: {self.documentation.get('generated_at', 'Unknown')}",
            f"Branch: {self.documentation.get('branch', 'Unknown')}",
            "",
            "=== SYSTEM OVERVIEW ===",
            self.documentation.get('system_overview', 'Not available'),
            "",
            "=== SERVICE CATALOG ===",
            json.dumps(self.documentation.get('service_catalog', {}), indent=2),
            "",
            "=== EXPECTED ORDER FLOWS ===",
            self._format_flows(self.documentation.get('expected_flows', {})),
            "",
            "=== API CONTRACTS ===",
            self._format_api_contracts(self.documentation.get('api_contracts', {})),
            "",
            "=== ERROR HANDLING PATTERNS ===",
            self.documentation.get('error_handling', 'Not available'),
            "",
            "=== COMPONENT MAP ===",
            json.dumps(self.documentation.get('component_map', {}), indent=2),
            "",
            "==================================================",
            "Use GitLab tools to fetch specific file contents when detailed code analysis is needed.",
            "==================================================",
        ]
        
        return "\n".join(summary_parts)
    
    def _generate_system_overview(self, java_files: List[Dict]) -> str:
        """Generate high-level system overview"""
        
        services = []
        controllers = []
        models = []
        
        for file_info in java_files:
            path = file_info.get('path', '')
            name = file_info.get('name', '')
            
            if 'Service' in name:
                services.append(name.replace('.java', ''))
            elif 'Controller' in name or 'Handler' in name:
                controllers.append(name.replace('.java', ''))
            elif 'Model' in name or 'Entity' in name or 'DTO' in name:
                models.append(name.replace('.java', ''))
        
        overview = f"""
EOC Order Care System Architecture:

**Services ({len(services)}):**
{self._format_list(services[:10])}

**Controllers/Handlers ({len(controllers)}):**
{self._format_list(controllers[:10])}

**Data Models ({len(models)}):**
{self._format_list(models[:10])}

**System Purpose:**
Order Care (EOC) is responsible for order lifecycle management including:
- Order creation and validation
- Order orchestration across systems (DPI, Triad, TC, SOAPO)
- Message processing and logging
- Error handling and recovery
- Order tracking and status updates
"""
        return overview
    
    def _generate_service_catalog(self, java_files: List[Dict]) -> Dict[str, Any]:
        """Generate catalog of services and their responsibilities"""
        
        catalog = {}
        
        for file_info in java_files:
            name = file_info.get('name', '')
            path = file_info.get('path', '')
            
            if 'Service' in name:
                service_name = name.replace('.java', '')
                
                # Infer responsibility from name
                responsibility = self._infer_service_responsibility(service_name)
                
                catalog[service_name] = {
                    "file_path": path,  # Full path for GitLab fetching
                    "file_name": name,
                    "responsibility": responsibility,
                    "type": "Service",
                    "layer": self._determine_layer(path),
                    "gitlab_fetch_command": f'get_file_content("{path}")'
                }
        
        return catalog
    
    def _generate_api_contracts(self, java_files: List[Dict]) -> Dict[str, Any]:
        """Generate API contracts (expected inputs/outputs)"""
        
        contracts = {
            "order_creation": {
                "endpoint": "POST /orders",
                "input": "Order details, customer info, service type",
                "output": "cwdocid, cworderid, status",
                "expected_http_codes": [200, 201, 400, 500]
            },
            "order_tracking": {
                "endpoint": "GET /orders/{cworderid}/status",
                "input": "cworderid",
                "output": "Order status, tracking info, error details",
                "expected_http_codes": [200, 404, 500]
            },
            "message_processing": {
                "service": "MessageProcessingService",
                "input": "Message payload, operation type, user_data",
                "output": "MSGID, status, send/receive data",
                "expected_outcomes": ["SUCCESS", "FAILED", "RETRY"]
            }
        }
        
        return contracts
    
    def _generate_expected_flows(self, java_files: List[Dict]) -> Dict[str, Any]:
        """Generate expected system flows with file references"""
        
        # Find relevant files for each component
        file_map = {}
        for file_info in java_files:
            name = file_info.get('name', '').replace('.java', '')
            path = file_info.get('path', '')
            file_map[name] = path
        
        flows = {
            "new_order_flow": {
                "description": "Standard flow for creating a new order",
                "related_files": self._find_related_files(file_map, ["Order", "Controller", "Service"]),
                "steps": [
                    {"step": 1, "component": "OrderController", "action": "Receive order request", "expected": "Validation passes", 
                     "file": file_map.get("OrderController", "OrderController.java")},
                    {"step": 2, "component": "OrderService", "action": "Create ORDER_ORDER_HEADER entry", "expected": "cwdocid generated",
                     "file": file_map.get("OrderService", "OrderService.java")},
                    {"step": 3, "component": "OrderInstanceService", "action": "Create CWORDERINSTANCE", "expected": "Order instance created",
                     "file": file_map.get("OrderInstanceService", "OrderInstanceService.java")},
                    {"step": 4, "component": "OrderOrchestrator", "action": "Route to provisioning systems", "expected": "Messages sent to DPI/Triad",
                     "file": file_map.get("OrderOrchestrator", "OrderOrchestrator.java")},
                    {"step": 5, "component": "MessageLogger", "action": "Log messages to CWMESSAGELOG", "expected": "MSGID created",
                     "file": file_map.get("MessageLogger", "MessageLogger.java")},
                    {"step": 6, "component": "OrderTracking", "action": "Update ORDER_TRACKING_INFO", "expected": "Status = PROCESSING",
                     "file": file_map.get("OrderTrackingService", "OrderTrackingService.java")}
                ],
                "success_criteria": "Order reaches COMPLETE status",
                "failure_points": ["Validation", "DPI call", "Triad call", "DB write"]
            },
            "order_modification_flow": {
                "description": "Flow for modifying an existing order",
                "steps": [
                    {"step": 1, "component": "OrderService", "action": "Fetch existing order", "expected": "Order found in DB"},
                    {"step": 2, "component": "ValidationService", "action": "Validate modification", "expected": "Change allowed"},
                    {"step": 3, "component": "ChangeOrderService", "action": "Create change order", "expected": "New cwdocid for change"},
                    {"step": 4, "component": "OrderOrchestrator", "action": "Send modification messages", "expected": "Systems updated"}
                ],
                "success_criteria": "Order modification reflected in all systems",
                "failure_points": ["Order not found", "Validation failed", "System update failed"]
            },
            "error_recovery_flow": {
                "description": "Flow when an order encounters an error",
                "steps": [
                    {"step": 1, "component": "ErrorDetector", "action": "Detect error in ORDER_TRACKING_INFO", "expected": "Error fields populated"},
                    {"step": 2, "component": "ErrorHandler", "action": "Categorize error", "expected": "Error type identified"},
                    {"step": 3, "component": "RetryManager", "action": "Determine retry strategy", "expected": "Retry or escalate"},
                    {"step": 4, "component": "NotificationService", "action": "Notify if needed", "expected": "Alerts sent"}
                ],
                "success_criteria": "Error resolved or escalated appropriately",
                "failure_points": ["Error not detected", "Retry loop", "Notification failed"]
            }
        }
        
        return flows
    
    def _generate_error_handling_guide(self, java_files: List[Dict]) -> str:
        """Generate error handling patterns guide"""
        
        guide = """
ERROR HANDLING PATTERNS IN EOC:

**1. Database-Level Errors (ORDER_TRACKING_INFO):**
   - WFMERRORID: Workflow Manager errors
   - DPIERRORID_IA / DPIERRORID_DISP: DPI system errors
   - TRIADERRORID_IA / TRIADERRORID_DISP: Triad system errors
   - TCERRORID_IA / TCERRORID_DISP: TC system errors
   - HASDPIEVERERRORED: Flag if DPI ever errored

**2. Message-Level Errors (CWMESSAGELOG):**
   - FAILURE field: Indicates message processing failure
   - ATTEMPTCOUNT: Number of retry attempts
   - RECEIVE_DATA: May contain error response from external system

**3. Expected Error Codes:**
   - 200: Success
   - 400: Bad Request (validation failed)
   - 402: Payment Required
   - 404: Not Found
   - 500: Internal Server Error
   - 503: Service Unavailable (external system down)

**4. Retry Logic:**
   - Automatic retry for 500, 503 errors
   - No retry for 400, 404 errors
   - Max 3 retry attempts (check ATTEMPTCOUNT)

**5. Error Recovery:**
   - Check ORDER_TRACKING_INFO error fields first
   - Review CWMESSAGELOG for message failures
   - Correlate using cworderid across tables
"""
        return guide
    
    def _generate_component_map(self, java_files: List[Dict]) -> Dict[str, Any]:
        """Generate component interaction map"""
        
        component_map = {
            "order_layer": {
                "components": ["OrderService", "OrderController", "OrderValidator"],
                "responsibility": "Order lifecycle management",
                "interacts_with": ["database_layer", "orchestration_layer"]
            },
            "orchestration_layer": {
                "components": ["OrderOrchestrator", "MessageRouter", "SystemIntegrator"],
                "responsibility": "Route orders to external systems",
                "interacts_with": ["external_systems", "message_layer"]
            },
            "message_layer": {
                "components": ["MessageProcessor", "MessageLogger", "QueueManager"],
                "responsibility": "Message processing and logging",
                "interacts_with": ["database_layer", "external_systems"]
            },
            "database_layer": {
                "components": ["OrderRepository", "TrackingRepository", "MessageRepository"],
                "responsibility": "Data persistence",
                "tables": ["ORDER_ORDER_HEADER", "CWORDERINSTANCE", "ORDER_TRACKING_INFO", "CWMESSAGELOG"]
            },
            "external_systems": {
                "systems": ["DPI", "Triad", "TC", "SOAPO", "ServiceMan", "HSI"],
                "integration_type": "REST/SOAP APIs",
                "error_handling": "Captured in ORDER_TRACKING_INFO error fields"
            }
        }
        
        return component_map
    
    def _infer_service_responsibility(self, service_name: str) -> str:
        """Infer service responsibility from name"""
        
        if "Order" in service_name:
            return "Order management and lifecycle"
        elif "Payment" in service_name:
            return "Payment processing and validation"
        elif "Message" in service_name:
            return "Message processing and routing"
        elif "Notification" in service_name:
            return "Customer and system notifications"
        elif "Validation" in service_name:
            return "Data validation and business rules"
        elif "Integration" in service_name:
            return "External system integration"
        else:
            return "Supporting service"
    
    def _determine_layer(self, path: str) -> str:
        """Determine architectural layer from path"""
        
        if "controller" in path.lower() or "handler" in path.lower():
            return "Presentation Layer"
        elif "service" in path.lower():
            return "Business Logic Layer"
        elif "repository" in path.lower() or "dao" in path.lower():
            return "Data Access Layer"
        elif "model" in path.lower() or "entity" in path.lower():
            return "Data Model"
        else:
            return "Utility/Support"
    
    def _format_list(self, items: List[str]) -> str:
        """Format list for display"""
        if not items:
            return "  (none found)"
        return "\n".join([f"  - {item}" for item in items])
    
    def _format_flows(self, flows: Dict[str, Any]) -> str:
        """Format flows for display"""
        formatted = []
        for flow_name, flow_data in flows.items():
            formatted.append(f"\n**{flow_name}:**")
            formatted.append(f"  Description: {flow_data.get('description', 'N/A')}")
            formatted.append(f"  Steps:")
            for step in flow_data.get('steps', []):
                formatted.append(f"    {step['step']}. {step['component']}: {step['action']}")
                formatted.append(f"       Expected: {step['expected']}")
            formatted.append(f"  Success: {flow_data.get('success_criteria', 'N/A')}")
            formatted.append(f"  Failure Points: {', '.join(flow_data.get('failure_points', []))}")
        
        return "\n".join(formatted)
    
    def _format_api_contracts(self, contracts: Dict[str, Any]) -> str:
        """Format API contracts for display"""
        formatted = []
        for contract_name, contract_data in contracts.items():
            formatted.append(f"\n**{contract_name}:**")
            for key, value in contract_data.items():
                formatted.append(f"  {key}: {value}")
        
        return "\n".join(formatted)
    
    def _find_related_files(self, file_map: Dict[str, str], keywords: List[str]) -> List[Dict[str, str]]:
        """Find files related to keywords"""
        related = []
        for name, path in file_map.items():
            if any(keyword in name for keyword in keywords):
                related.append({
                    "file_name": f"{name}.java",
                    "file_path": path,
                    "fetch_command": f'get_file_content("{path}")'
                })
        return related[:10]  # Limit to 10 files


    def _parse_xml_files(self, xml_files: List[Dict], branch: str, max_files: int = 500) -> List[Dict[str, Any]]:
        """
        Parse XML metadata files using Cordys parser
        Samples files intelligently across modules for broad coverage
        """
        parsed_data = []

        # Organize files by module and type
        by_module = defaultdict(lambda: defaultdict(list))

        for file_info in xml_files:
            path = file_info['path']
            name = file_info['name']

            # Extract module from path
            path_parts = path.split('/')
            module = path_parts[2] if len(path_parts) > 2 else 'root'

            # Determine file type prefix
            if '_' in name:
                file_type = name.split('_')[0]
            else:
                file_type = 'other'

            by_module[module][file_type].append(file_info)

        # PARSE ALL FILES - NO SAMPLING
        files_to_parse = []
        for module, types in by_module.items():
            for file_type, files in types.items():
                # Take ALL files - comprehensive documentation
                files_to_parse.extend(files)

        # Apply max_files limit (set to 999999 for comprehensive mode)
        files_to_parse = files_to_parse[:max_files]
        
        logger.info(f"📊 Files by module:")
        for module, types in by_module.items():
            total = sum(len(files) for files in types.values())
            logger.info(f"  {module}: {total} files")

        logger.info(f"🔍 Parsing {len(files_to_parse)} XML files in COMPREHENSIVE mode...")
        logger.info("📖 Reading every line of code for deep understanding...")

        for i, file_info in enumerate(files_to_parse):
            # More frequent progress updates for visibility
            if i % 25 == 0:
                pct = (i / len(files_to_parse)) * 100 if files_to_parse else 0
                logger.info(f"  Progress: {i}/{len(files_to_parse)} ({pct:.1f}%) - Current: {file_info.get('name', 'Unknown')}")

            try:
                file_data = gitlab_client.get_file_content(file_info['path'], branch)

                if 'decoded_content' in file_data:
                    parsed = cordys_parser.parse_file(file_data['decoded_content'], file_info['path'])

                    if parsed:
                        parsed_data.append(parsed)
                        
                        # Log what we found for transparency
                        parsed_type = parsed.get('type', 'unknown')
                        if i % 100 == 0:  # Every 100 files
                            logger.info(f"    Found: {parsed_type} - {parsed.get('name', 'unnamed')}")

            except Exception as e:
                logger.warning(f"⚠️  Failed to fetch/parse {file_info['path']}: {e}")
                continue

        logger.info(f"✅ Successfully parsed {len(parsed_data)} files out of {len(files_to_parse)} total")
        logger.info(f"📊 Success rate: {(len(parsed_data)/len(files_to_parse)*100):.1f}%")

        return parsed_data


    def _organize_parsed_data(self, parsed_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Organize parsed data by type and module for easy reference"""

        organized = {
            "scripts": [],
            "interfaces": [],
            "processes": [],
            "documents": [],
            "datatypes": [],
            "services": [],
            "bindings": [],
            "namespaces": [],
            "by_module": defaultdict(lambda: defaultdict(list))
        }

        for item in parsed_data:
            item_type = item.get('type', 'unknown')

            # Add to type-specific list
            if item_type == 'script':
                organized['scripts'].append(item)
            elif item_type == 'interface':
                organized['interfaces'].append(item)
            elif item_type == 'process':
                organized['processes'].append(item)
            elif item_type == 'document':
                organized['documents'].append(item)
            elif item_type == 'datatype':
                organized['datatypes'].append(item)
            elif item_type == 'service':
                organized['services'].append(item)
            elif item_type == 'binding':
                organized['bindings'].append(item)
            elif item_type == 'namespace':
                organized['namespaces'].append(item)

            # Also organize by module
            file_path = item.get('file_path', '')
            path_parts = file_path.split('/')
            module = path_parts[2] if len(path_parts) > 2 else 'root'

            organized['by_module'][module][item_type].append(item)

        return organized


    def _generate_cordys_system_overview(self, organized_data: Dict[str, Any]) -> str:
        """Generate system overview from Cordys metadata"""

        modules = list(organized_data['by_module'].keys())

        overview = f"""
    **EOC Order Care - Cordys/OpenText BPM System**

    **Architecture:**
    - Platform: Cordys/OpenText BPM
    - Modules: {len(modules)}
    - Services: {len(organized_data['interfaces'])}
    - Business Processes: {len(organized_data['processes'])}
    - Data Entities: {len(organized_data['documents'])}
    - Business Logic Scripts: {len(organized_data['scripts'])}

    **Key Modules:**
    {self._format_module_list(modules[:15])}

    **System Purpose:**
    Order Care (EOC) manages the complete order lifecycle including:
    - Order capture and validation
    - Order orchestration across multiple systems (DPI, Triad, TC, Pega)
    - Message processing and transformation
    - Provisioning coordination
    - Error handling and recovery
    - Order status tracking and notifications

    **Integration Landscape:**
    - DPI (Digital Platform Integration) - Order submission
    - Triad - Network provisioning
    - TeamConnect (TC) - Dispatch and scheduling
    - Pega - Order management workflow
    - SOAPO - Service activation
    - ESB - Enterprise service bus integration
    """

        return overview


    def _generate_cordys_service_catalog(self, organized_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive service catalog"""

        catalog = {}

        for iface in organized_data['interfaces']:
            service_name = iface.get('name', 'Unknown')

            operations = []
            for op in iface.get('operations', []):
                operations.append({
                    "name": op.get('name'),
                    "type": op.get('type'),
                    "description": op.get('description'),
                    "input": op.get('input'),
                    "output": op.get('output')
                })

            catalog[service_name] = {
                "description": iface.get('description'),
                "label": iface.get('label'),
                "file_path": iface.get('file_path'),
                "operations": operations
            }

        return catalog


    def _generate_cordys_api_contracts(self, organized_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate API contract details"""

        contracts = {}

        for iface in organized_data['interfaces']:
            for op in iface.get('operations', []):
                contract_name = f"{iface.get('name')}.{op.get('name')}"

                contracts[contract_name] = {
                    "service": iface.get('label'),
                    "operation": op.get('name'),
                    "type": op.get('type'),
                    "request_structure": op.get('input'),
                    "response_structure": op.get('output'),
                    "description": op.get('description'),
                    "file_path": iface.get('file_path')
                }

        return contracts


    def _generate_cordys_expected_flows(self, organized_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate expected business process flows with crystal clear details"""

        flows = {}
        
        # =======================================================================================
        # KEY BUSINESS FLOWS - EXPLICITLY DOCUMENTED
        # =======================================================================================
        
        # 1. InstallOptions Flow
        flows["InstallOptions"] = {
            "flow_type": "Determine Install Options",
            "description": "Determines available installation types based on customer location, product, and network serviceability",
            "trigger": "Operation: installOptions or InstallOptions",
            "file_path": "Trunk/FrontierOM/metadata/InstallOptions/",
            "steps": [
                {
                    "step": 1,
                    "action": "Validate customer address",
                    "expected_result": "Address validation complete",
                    "systems": ["DPI", "Serviceability API"]
                },
                {
                    "step": 2,
                    "action": "Check network serviceability",
                    "expected_result": "Available services identified",
                    "systems": ["Network API", "DPI"]
                },
                {
                    "step": 3,
                    "action": "Determine install types",
                    "expected_result": "List of install options: SELF_INSTALL, FULL_INSTALL, NO_INSTALL, INSTANT_ACTIVATION",
                    "systems": ["EOC Business Logic"]
                },
                {
                    "step": 4,
                    "action": "Return install options to caller",
                    "expected_result": "Install options response",
                    "systems": ["EOC"]
                }
            ],
            "install_types": {
                "SELF_INSTALL": "Customer installs equipment themselves - EOC orchestrates",
                "FULL_INSTALL": "Technician visit required - FORWARDED TO DPI",
                "NO_INSTALL": "No equipment/installation needed - EOC orchestrates",
                "INSTANT_ACTIVATION": "Immediate activation, no physical install - EOC orchestrates"
            },
            "orchestration_owner": {
                "EOC_handles": ["SELF_INSTALL", "NO_INSTALL", "INSTANT_ACTIVATION"],
                "DPI_handles": ["FULL_INSTALL"]
            },
            "total_activities": 4
        }
        
        # 2. Legacy Submit Order (CustomerOrderManagement/CommitCustomerOrder)
        flows["Legacy_SubmitOrder_CommitCustomerOrder"] = {
            "flow_type": "Legacy Submit Order",
            "description": "Legacy submit order flow via CommitCustomerOrder. Recalculates InstallOptions and determines orchestration path.",
            "trigger": "Operation: confirmcustomerorder",
            "file_path": "Trunk/FrontierOM/metadata/CustomerOrderManagement/CommitCustomerOrder",
            "steps": [
                {
                    "step": 1,
                    "action": "Receive customer order",
                    "expected_result": "Order validated and accepted",
                    "systems": ["Pega", "EOC"]
                },
                {
                    "step": 2,
                    "action": "Call InstallOptions flow",
                    "expected_result": "Install type determined (SELF/FULL/NO/INSTANT)",
                    "systems": ["EOC InstallOptions"]
                },
                {
                    "step": 3,
                    "action": "Decision: Check install_type",
                    "expected_result": "Routing decision made",
                    "systems": ["EOC Business Logic"],
                    "decision_logic": {
                        "SELF_INSTALL": "EOC orchestrates → Proceed to Step 4",
                        "NO_INSTALL": "EOC orchestrates → Proceed to Step 4",
                        "INSTANT_ACTIVATION": "EOC orchestrates → Proceed to Step 4",
                        "FULL_INSTALL": "Forward to DPI → Proceed to Step 10"
                    }
                },
                {
                    "step": 4,
                    "action": "[EOC Path] Validate order data",
                    "expected_result": "Order data validated",
                    "systems": ["EOC", "DPI API"],
                    "applies_to": ["SELF_INSTALL", "NO_INSTALL", "INSTANT_ACTIVATION"]
                },
                {
                    "step": 5,
                    "action": "[EOC Path] Create order in EOC",
                    "expected_result": "Order created in ORDER_ORDER_HEADER",
                    "systems": ["EOC Database"],
                    "applies_to": ["SELF_INSTALL", "NO_INSTALL", "INSTANT_ACTIVATION"]
                },
                {
                    "step": 6,
                    "action": "[EOC Path] Orchestrate provisioning",
                    "expected_result": "Provisioning tasks initiated",
                    "systems": ["TC", "TRIAD", "SOAPO"],
                    "applies_to": ["SELF_INSTALL", "NO_INSTALL", "INSTANT_ACTIVATION"],
                    "parallel_processing": ["TC Activation", "TRIAD Provisioning"]
                },
                {
                    "step": 7,
                    "action": "[EOC Path] Wait for provisioning completion",
                    "expected_result": "All provisioning tasks complete",
                    "systems": ["TC", "TRIAD"],
                    "applies_to": ["SELF_INSTALL", "NO_INSTALL", "INSTANT_ACTIVATION"]
                },
                {
                    "step": 8,
                    "action": "[EOC Path] Update order status",
                    "expected_result": "Order status updated to COMPLETE",
                    "systems": ["EOC Database", "DPI"],
                    "applies_to": ["SELF_INSTALL", "NO_INSTALL", "INSTANT_ACTIVATION"]
                },
                {
                    "step": 9,
                    "action": "[EOC Path] Send customer notification",
                    "expected_result": "Customer notified of completion",
                    "systems": ["Marketo", "Customer Notification API"],
                    "applies_to": ["SELF_INSTALL", "NO_INSTALL", "INSTANT_ACTIVATION"]
                },
                {
                    "step": 10,
                    "action": "[DPI Path] Forward order to DPI",
                    "expected_result": "Order handed off to DPI for FULL_INSTALL orchestration",
                    "systems": ["DPI"],
                    "applies_to": ["FULL_INSTALL"],
                    "note": "DPI handles all FULL_INSTALL orchestration (scheduling, dispatch, provisioning)"
                },
                {
                    "step": 11,
                    "action": "[DPI Path] Receive DPI completion notification",
                    "expected_result": "DPI notifies EOC of order completion",
                    "systems": ["DPI", "EOC"],
                    "applies_to": ["FULL_INSTALL"]
                }
            ],
            "orchestration_owner": {
                "EOC_handles": ["SELF_INSTALL", "NO_INSTALL", "INSTANT_ACTIVATION"],
                "DPI_handles": ["FULL_INSTALL"],
                "critical_note": "EOC only orchestrates SELF/NO/INSTANT. FULL_INSTALL is forwarded to DPI."
            },
            "expected_systems": ["Pega", "EOC", "DPI", "TC", "TRIAD", "SOAPO", "Marketo"],
            "total_activities": 11
        }
        
        # 3. DT Submit Order (OM.quoteToOrder)
        flows["DT_SubmitOrder_quoteToOrder"] = {
            "flow_type": "DT Submit Order",
            "description": "Digital Transformation submit order flow via OM.quoteToOrder",
            "trigger": "Operation: OM.quoteToOrder or OM.qouteToOrder",
            "file_path": "Trunk/FrontierOM/metadata/OM/",
            "steps": [
                {
                    "step": 1,
                    "action": "Receive order from Digital Transformation layer",
                    "expected_result": "Order validated and accepted",
                    "systems": ["Digital API", "EOC"]
                },
                {
                    "step": 2,
                    "action": "Transform order data",
                    "expected_result": "Order transformed to EOC format",
                    "systems": ["EOC Transformation"]
                },
                {
                    "step": 3,
                    "action": "Call InstallOptions (if needed)",
                    "expected_result": "Install type confirmed",
                    "systems": ["EOC InstallOptions"]
                },
                {
                    "step": 4,
                    "action": "Route order based on install_type",
                    "expected_result": "Order routed to appropriate orchestrator",
                    "systems": ["EOC Business Logic"],
                    "decision_logic": {
                        "SELF_INSTALL": "EOC orchestrates",
                        "NO_INSTALL": "EOC orchestrates",
                        "INSTANT_ACTIVATION": "EOC orchestrates",
                        "FULL_INSTALL": "Forward to DPI"
                    }
                },
                {
                    "step": 5,
                    "action": "Execute orchestration (EOC or DPI)",
                    "expected_result": "Order processing complete",
                    "systems": ["EOC", "DPI", "TC", "TRIAD"]
                }
            ],
            "orchestration_owner": {
                "EOC_handles": ["SELF_INSTALL", "NO_INSTALL", "INSTANT_ACTIVATION"],
                "DPI_handles": ["FULL_INSTALL"]
            },
            "total_activities": 5
        }
        
        # 4. Retrieve Customer Order Details
        flows["RetrieveCustomerOrderDetails"] = {
            "flow_type": "Retrieve Order Details",
            "description": "Retrieve existing customer order details",
            "trigger": "Operation: retrievecustomerorderdetails",
            "file_path": "Trunk/FrontierOM/metadata/",
            "steps": [
                {
                    "step": 1,
                    "action": "Query ORDER_ORDER_HEADER by order identifiers",
                    "expected_result": "Order header data retrieved",
                    "systems": ["EOC Database"]
                },
                {
                    "step": 2,
                    "action": "Query ORDER_TRACKING_INFO for status",
                    "expected_result": "Order tracking status retrieved",
                    "systems": ["EOC Database"]
                },
                {
                    "step": 3,
                    "action": "Query CWORDERINSTANCE for metadata",
                    "expected_result": "Order instance details retrieved",
                    "systems": ["EOC Database"]
                },
                {
                    "step": 4,
                    "action": "Return consolidated order details",
                    "expected_result": "Complete order data returned",
                    "systems": ["EOC"]
                }
            ],
            "total_activities": 4
        }
        
        # 5. Activation Flow (Of.Activation)
        flows["Of_Activation"] = {
            "flow_type": "Activation",
            "description": "Parallel activation to TC and TRIAD, followed by DPI billing update and customer notification",
            "trigger": "Operation: SubmitOrder (activation phase)",
            "file_path": "Trunk/FrontierOM/metadata/OF/",
            "steps": [
                {
                    "step": 1,
                    "action": "Initiate parallel activation",
                    "expected_result": "TC and TRIAD activation started",
                    "systems": ["EOC"]
                },
                {
                    "step": 2,
                    "action": "[Parallel] TC Activation",
                    "expected_result": "TC activation complete",
                    "systems": ["TeamConnect"],
                    "parallel": True
                },
                {
                    "step": 3,
                    "action": "[Parallel] TRIAD Provisioning",
                    "expected_result": "TRIAD provisioning complete",
                    "systems": ["TRIAD"],
                    "parallel": True
                },
                {
                    "step": 4,
                    "action": "Wait for both TC and TRIAD completion",
                    "expected_result": "All activation complete",
                    "systems": ["EOC"]
                },
                {
                    "step": 5,
                    "action": "[Parallel] DPI SubmitOrder - Billing Update",
                    "expected_result": "Billing updated in DPI",
                    "systems": ["DPI"],
                    "parallel": True
                },
                {
                    "step": 6,
                    "action": "[Parallel] Customer Notification",
                    "expected_result": "Customer notified",
                    "systems": ["Marketo"],
                    "parallel": True
                }
            ],
            "total_activities": 6
        }
        
        # 6. Customer Notification Flow
        flows["Of_CustomerNotification"] = {
            "flow_type": "Customer Notification",
            "description": "Send notification to Marketo to update customer. Errors redirect to WFM.",
            "trigger": "Operation: customerNotification",
            "file_path": "Trunk/FrontierOM/metadata/OF/",
            "steps": [
                {
                    "step": 1,
                    "action": "Prepare notification payload",
                    "expected_result": "Notification data ready",
                    "systems": ["EOC"]
                },
                {
                    "step": 2,
                    "action": "Send to Marketo",
                    "expected_result": "Notification sent successfully",
                    "systems": ["Marketo API"]
                },
                {
                    "step": 3,
                    "action": "[OnException] Log error to WFM",
                    "expected_result": "WFM notified of failure",
                    "systems": ["WFM"],
                    "error_handling": True
                },
                {
                    "step": 4,
                    "action": "[OnException] Wait for WFM resolution",
                    "expected_result": "Error resolved or order cancelled",
                    "systems": ["WFM"],
                    "error_handling": True
                }
            ],
            "error_handling": {
                "on_error": "Redirect to WFM",
                "resolution_options": ["Continue where left off", "Cancel order", "Stop and require supplemental pass"]
            },
            "total_activities": 4
        }
        
        # 7. Cancellation Flow
        flows["Of_Cancellation"] = {
            "flow_type": "Cancellation",
            "description": "Cancel order and revert any provisioning",
            "trigger": "Operation: Cancel",
            "file_path": "Trunk/FrontierOM/metadata/OF/",
            "steps": [
                {
                    "step": 1,
                    "action": "Receive cancellation request",
                    "expected_result": "Cancellation validated",
                    "systems": ["EOC"]
                },
                {
                    "step": 2,
                    "action": "Check order status",
                    "expected_result": "Determine cancellation path",
                    "systems": ["EOC Database"]
                },
                {
                    "step": 3,
                    "action": "Cancel provisioning (if started)",
                    "expected_result": "Provisioning cancelled",
                    "systems": ["TC", "TRIAD", "DPI"]
                },
                {
                    "step": 4,
                    "action": "Update order status to CANCELLED",
                    "expected_result": "Order cancelled",
                    "systems": ["EOC Database"]
                },
                {
                    "step": 5,
                    "action": "Notify customer of cancellation",
                    "expected_result": "Customer notified",
                    "systems": ["Marketo"]
                }
            ],
            "total_activities": 5
        }
        
        # =======================================================================================
        # AUTO-DISCOVERED FLOWS FROM CORDYS METADATA
        # =======================================================================================
        
        for proc in organized_data['processes']:
            flow_name = proc.get('name', 'Unknown')

            # Skip if we already documented it above
            if flow_name in flows:
                continue

            # Extract activity sequence
            steps = []
            self._extract_process_steps(proc.get('activities', []), steps)

            flows[flow_name] = {
                "description": proc.get('description'),
                "label": proc.get('label'),
                "file_path": proc.get('file_path'),
                "steps": steps,
                "total_activities": len(steps)
            }

        return flows


    def _generate_cordys_error_handling(self, organized_data: Dict[str, Any]) -> str:
        """Generate error handling patterns documentation"""

        error_handlers = []

        # Find error handling processes and scripts
        for proc in organized_data['processes']:
            if 'error' in proc.get('name', '').lower() or 'exception' in proc.get('name', '').lower():
                error_handlers.append({
                    "type": "process",
                    "name": proc.get('name'),
                    "file_path": proc.get('file_path')
                })

        for script in organized_data['scripts']:
            if 'error' in script.get('name', '').lower() or 'exception' in script.get('name', '').lower():
                error_handlers.append({
                    "type": "script",
                    "name": script.get('name'),
                    "file_path": script.get('file_path')
                })

        doc = f"""
    **Error Handling Patterns:**

    **Error Handling Components ({len(error_handlers)}):**
    {self._format_component_list(error_handlers[:10])}

    **Common Patterns:**
    1. **Retry Logic**: Services configured with retry policies
    2. **Error Logging**: Message logs (CWMESSAGELOG) capture all errors
    3. **Compensation Flows**: Rollback processes for failed transactions
    4. **Error Notifications**: Customer and internal team notifications
    5. **Manual Intervention**: Orders moved to error queues for manual handling

    **Key Error Tables:**
    - CWMESSAGELOG: All message exchanges with FAILURE flag
    - ORDER_TRACKING_INFO: Error messages and status codes
    - ORDER_ORDER_HEADER: Order-level error tracking
    """

        return doc


    def _generate_cordys_component_map(self, organized_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate component relationship map"""

        component_map = {}

        # Map services to their bindings
        for service in organized_data['services']:
            service_name = service.get('name', '')
            ports = service.get('ports', [])

            bindings = []
            for port in ports:
                binding_ref = port.get('binding', '')
                # Find the actual binding
                for bind in organized_data['bindings']:
                    if binding_ref in bind.get('name', ''):
                        bindings.append({
                            "binding_name": bind.get('name'),
                            "interface": bind.get('interface'),
                            "file_path": bind.get('file_path')
                        })

            component_map[service_name] = {
                "type": "external_service",
                "description": service.get('description'),
                "file_path": service.get('file_path'),
                "bindings": bindings
            }

        return component_map


    def _generate_cordys_data_entities(self, organized_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate data entity catalog with DB mappings"""

        entities = {}

        for doc in organized_data['documents']:
            entity_name = doc.get('name', 'Unknown')

            fields = []
            for field in doc.get('fields', []):
                fields.append({
                    "name": field.get('name'),
                    "column": field.get('column'),
                    "table": field.get('table'),
                    "type": field.get('value_type'),
                    "is_key": field.get('is_key', False)
                })

            entities[entity_name] = {
                "description": doc.get('description'),
                "db_schema": doc.get('db_schema'),
                "extends": doc.get('extends'),
                "file_path": doc.get('file_path'),
                "fields": fields
            }

        return entities


    def _generate_cordys_integration_points(self, organized_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate external system integration catalog"""

        integrations = {}

        # External services are the integration points
        for service in organized_data['services']:
            service_name = service.get('name', '')

            # Try to determine external system from name
            external_system = "Unknown"
            if 'dpi' in service_name.lower():
                external_system = "DPI (Digital Platform)"
            elif 'triad' in service_name.lower():
                external_system = "Triad (Network Provisioning)"
            elif 'tc' in service_name.lower() or 'teamconnect' in service_name.lower():
                external_system = "TeamConnect (Dispatch)"
            elif 'pega' in service_name.lower():
                external_system = "Pega (Order Management)"
            elif 'esb' in service_name.lower():
                external_system = "ESB (Enterprise Service Bus)"

            integrations[service_name] = {
                "external_system": external_system,
                "description": service.get('description'),
                "file_path": service.get('file_path'),
                "ports": service.get('ports', [])
            }

        return integrations


    # Helper methods

    def _format_module_list(self, modules: List[str]) -> str:
        """Format module list"""
        if not modules:
            return "  (none found)"
        return "\n".join([f"  - {m}" for m in modules])


    def _format_component_list(self, components: List[Dict]) -> str:
        """Format component list"""
        if not components:
            return "  (none found)"

        formatted = []
        for comp in components:
            name = comp.get('name', 'Unknown')
            comp_type = comp.get('type', '')
            file_path = comp.get('file_path', '')
            formatted.append(f"  - [{comp_type}] {name} (`{file_path}`)")

        return "\n".join(formatted)


    def _extract_process_steps(self, activities: List[Dict], steps: List[Dict], depth: int = 0):
        """Recursively extract process steps"""
        if depth > 5:  # Prevent deep recursion
            return

        for activity in activities:
            step = {
                "name": activity.get('name'),
                "type": activity.get('type'),
                "label": activity.get('label'),
                "element": activity.get('element'),
                "depth": depth
            }
            steps.append(step)

            # Recurse into children
            if 'children' in activity:
                self._extract_process_steps(activity['children'], steps, depth + 1)



# Global singleton
doc_generator = CodeDocumentationGenerator()



