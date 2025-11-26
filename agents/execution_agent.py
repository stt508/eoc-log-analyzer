"""
Execution Agent for Oracle Log Analysis (Phase 1)

Simple "dumb worker" that executes individual steps.
The Coordinator tells it what to do, and it just does it.
No intelligence, no decision making - just execution.
"""

import json
from typing import Dict, Any
from datetime import datetime
from langchain_databricks import ChatDatabricks
from loguru import logger

from config import config
from tools.database_api_client import api_client
from tools.knowledge_server.knowledge_tools import get_process_flow_tool


class ExecutionAgent:
    """Dumb worker agent that executes individual steps"""
    
    def __init__(self):
        # Initialize LLM for steps 7-8
        endpoint_name = config.llm.databricks_base_url.split("/")[-1]
        host = config.llm.databricks_base_url.rsplit("/serving-endpoints/", 1)[0]
        
        self.llm = ChatDatabricks(
            endpoint=endpoint_name,
            host=host,
            api_token=config.llm.databricks_token,
            max_tokens=config.llm.max_tokens,
            temperature=config.llm.temperature
        )
        
        logger.info("✅ Execution Agent initialized (dumb worker mode)")
    
    def _match_flow_type(self, operation: str) -> str:
        """Rule-based flow detection (for step 5)"""
        if not operation:
            return "Unknown"
        
        op_lower = operation.lower()
        
        if 'dt.tmf622ext.service:ominterface/createorder' in op_lower:
            return "DT_SubmitOrder"
        elif 'cpq.services:confirmcustomerorder/confirmcustomerorder' in op_lower:
            return "Legacy_SubmitOrder"
        elif 'dt.tmf622ext.service:installationconfiguration/getinstalloption' in op_lower:
            return "DT_InstallOptions"
        elif 'ordercare:installationconfiguration/getinstalloption' in op_lower:
            return "Legacy_InstallOptions"
        else:
            return "Unknown"
    
    def execute_step(self, step: Dict[str, Any], params: Dict[str, Any], memory: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a single step (dumb worker - just follows instructions)
        
        Args:
            step: Step definition from plan
            params: Resolved parameters (placeholders already resolved by Coordinator)
            memory: Memory for this order (read-only for context)
        
        Returns:
            Result dictionary with standard format:
            {
                "action": "retrieve_order_header",
                "status": "completed" | "error",
                "result": [...],
                "count": N,
                "timestamp": "..."
            }
        """
        
        action = step['action']
        tool = step['tool']
        
        try:
            # ================================================================
            # STEP 1: Retrieve Order Header
            # ================================================================
            if action == "retrieve_order_header":
                result = api_client.search_orders(**params)
                return {
                    "action": action,
                    "status": "completed",
                    "result": result,
                    "count": len(result),
                    "timestamp": datetime.now().isoformat()
                }
            
            # ================================================================
            # STEP 2: Retrieve Order Tracking
            # ================================================================
            elif action == "retrieve_order_tracking":
                result = api_client.search_order_tracking(**params)
                return {
                    "action": action,
                    "status": "completed",
                    "result": result,
                    "count": len(result),
                    "timestamp": datetime.now().isoformat()
                }
            
            # ================================================================
            # STEP 3: Retrieve Order Instances
            # ================================================================
            elif action == "retrieve_order_instances":
                result = api_client.search_order_instances(**params)
                return {
                    "action": action,
                    "status": "completed",
                    "result": result,
                    "count": len(result),
                    "timestamp": datetime.now().isoformat()
                }
            
            # ================================================================
            # STEP 4: Retrieve Message Logs
            # ================================================================
            elif action == "retrieve_message_logs":
                result = api_client.search_message_logs(**params)
                return {
                    "action": action,
                    "status": "completed",
                    "result": result,
                    "count": len(result),
                    "timestamp": datetime.now().isoformat()
                }
            
            # ================================================================
            # STEP 5: Detect Execution Flow (Rule-based)
            # ================================================================
            elif action == "detect_execution_flow":
                message_logs = params.get('message_logs', [])
                install_type = params.get('install_type')
                
                # Detect flows from message logs
                detected_flows = []
                for log in message_logs:
                    flow_type = self._match_flow_type(log.get('operation', ''))
                    if flow_type != "Unknown":
                        detected_flows.append({
                            "flow_type": flow_type,
                            "operation": log.get('operation'),
                            "timestamp": log.get('creation_time'),
                            "msgid": log.get('msgid')
                        })
                
                return {
                    "action": action,
                    "status": "completed",
                    "result": {
                        "flows": detected_flows,
                        "install_type": install_type,
                        "total_flows": len(detected_flows)
                    },
                    "count": len(detected_flows),
                    "timestamp": datetime.now().isoformat()
                }
            
            # ================================================================
            # STEP 6: Retrieve Expected Behavior
            # ================================================================
            elif action == "retrieve_expected_behavior":
                flow_data = params.get('flow_type', {})
                flows = flow_data.get('flows', []) if isinstance(flow_data, dict) else []
                
                # Get expected docs for each detected flow
                expected_docs = []
                for flow in flows:
                    flow_type = flow.get('flow_type')
                    
                    # Map to Knowledge Server flow name
                    flow_mapping = {
                        "DT_SubmitOrder": "OM.quoteToOrder",
                        "Legacy_SubmitOrder": "CustomerOrderManagement:CustomerOrderManagement/CommitCustomerOrder",
                        "DT_InstallOptions": "InstallOptions",
                        "Legacy_InstallOptions": "InstallOptions"
                    }
                    
                    flow_name = flow_mapping.get(flow_type, "Unknown")
                    
                    try:
                        docs = get_process_flow_tool(flow_name)
                        expected_docs.append({
                            "flow_type": flow_type,
                            "documentation": docs
                        })
                    except Exception as e:
                        expected_docs.append({
                            "flow_type": flow_type,
                            "documentation": f"Documentation not available: {e}"
                        })
                
                return {
                    "action": action,
                    "status": "completed",
                    "result": expected_docs,
                    "count": len(expected_docs),
                    "timestamp": datetime.now().isoformat()
                }
            
            # ================================================================
            # STEP 7: Analyze Expected vs Actual (LLM)
            # ================================================================
            elif action == "analyze_expected_vs_actual":
                all_data = params.get('all_collected_data', memory)
                expected_behavior = params.get('expected_behavior', [])
                detected_flows = params.get('detected_flows', {})
                
                # Build comprehensive analysis prompt
                analysis_prompt = f"""
                Analyze this order troubleshooting data:
                
                ORDER INFO:
                {json.dumps(all_data.get('order_info', {}), indent=2, default=str)}
                
                DETECTED FLOWS:
                {json.dumps(detected_flows, indent=2, default=str)}
                
                EXPECTED BEHAVIOR:
                {json.dumps(expected_behavior, indent=2, default=str)[:5000]}
                
                COLLECTED DATA:
                - Message Logs: {all_data.get('step_4', {}).get('count', 0)} records
                - Order Tracking: {all_data.get('step_2', {}).get('count', 0)} records
                - Order Instances: {all_data.get('step_3', {}).get('count', 0)} records
                
                MESSAGE LOGS SAMPLE:
                {json.dumps(all_data.get('step_4', {}).get('result', [])[:10], indent=2, default=str)[:3000]}
                
                ORDER TRACKING SAMPLE:
                {json.dumps(all_data.get('step_2', {}).get('result', [])[:5], indent=2, default=str)[:2000]}
                
                PROVIDE A COMPREHENSIVE ANALYSIS:
                1. Flow Summary: What flows were detected and in what order?
                2. Expected vs Actual: Compare actual operations against expected flow documentation
                3. Issues Identified: Any errors, failures, or deviations?
                4. Root Cause: What is the most likely cause of any issues?
                5. Recommendations: Actionable next steps
                
                Be specific and reference actual data from the logs.
                """
                
                # Call LLM
                logger.info(f"   🤖 Calling LLM for analysis ({len(analysis_prompt)} chars)")
                llm_response = self.llm.invoke(analysis_prompt)
                analysis = llm_response.content if hasattr(llm_response, 'content') else str(llm_response)
                
                return {
                    "action": action,
                    "status": "completed",
                    "result": analysis,
                    "count": 1,
                    "timestamp": datetime.now().isoformat()
                }
            
            # ================================================================
            # STEP 8: Format Response
            # ================================================================
            elif action == "format_response":
                analysis = params.get('analysis', '')
                search_input = params.get('search_input', {})
                
                # Simple formatting (for now just return the analysis)
                formatted = f"""
                # Order Analysis Report
                
                **Search Criteria:** {search_input.get('type', 'N/A')} = {search_input.get('value', 'N/A')}
                **Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                
                ---
                
                {analysis}
                """
                
                return {
                    "action": action,
                    "status": "completed",
                    "result": formatted,
                    "count": 1,
                    "timestamp": datetime.now().isoformat()
                }
            
            # ================================================================
            # UNKNOWN ACTION
            # ================================================================
            else:
                logger.error(f"Unknown action: {action}")
                return {
                    "action": action,
                    "status": "error",
                    "error": f"Unknown action: {action}",
                    "result": None,
                    "count": 0,
                    "timestamp": datetime.now().isoformat()
                }
        
        except Exception as e:
            logger.error(f"❌ Step execution failed: {e}")
            return {
                "action": action,
                "status": "error",
                "error": str(e),
                "result": None,
                "count": 0,
                "timestamp": datetime.now().isoformat()
            }
