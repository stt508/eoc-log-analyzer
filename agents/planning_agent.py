"""
Planning Agent for Oracle Log Analysis (Phase 1)

Responsible for building a static 8-step execution plan.
NO LLM, NO tool calls, NO execution - just plan generation.
"""

import json
from typing import Dict, Any
from datetime import datetime
from loguru import logger


class PlanningAgent:
    """Agent responsible for building static execution plans"""
    
    # Map dropdown selections to database field names
    FIELD_MAPPING = {
        "phone_number": "billingtelephonenumber",
        "order_number_om": "omorderid",
        "order_number_dpi": "dpiordernumber",
        "quote_id": "quoteid",
        "quote_uuid": "quoteguid"
    }
    
    def __init__(self):
        logger.info("✅ Planning Agent initialized (static plan builder)")
    
    def create_plan(self, search_type: str, search_value: str) -> Dict[str, Any]:
        """
        Create a static 8-step execution plan
        
        Args:
            search_type: Type of identifier (phone_number, order_number_dpi, etc.)
            search_value: The actual value to search for
        
        Returns:
            Dictionary with plan structure
        """
        
        try:
            logger.info(f"📋 Planning: Building static plan for {search_type}={search_value}")
            
            # Get database field name for search type
            db_field = self.FIELD_MAPPING.get(search_type)
            
            if not db_field:
                logger.error(f"❌ Invalid search type: {search_type}")
                return {
                    "success": False,
                    "error": f"Invalid search type: {search_type}",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Build static 8-step plan
            plan = {
                "search_input": {
                    "type": search_type,
                    "value": search_value,
                    "db_field": db_field
                },
                "steps": [
                    # Step 1: Retrieve Order Header
                    {
                        "sequence": 1,
                        "action": "retrieve_order_header",
                        "tool": "search_orders",
                        "parameters": {
                            db_field: search_value,
                            "limit": 50,
                            "include_blob_data": False
                        },
                        "status": "pending",
                        "description": f"Search ORDER_ORDER_HEADER by {db_field}"
                    },
                    
                    # Step 2: Retrieve Order Tracking
                    {
                        "sequence": 2,
                        "action": "retrieve_order_tracking",
                        "tool": "search_order_tracking",
                        "parameters": {
                            "cworderid": "${from_step_1}",  # Extracted by Execution Agent
                            "limit": 50,
                            "include_blob_data": True
                        },
                        "status": "pending",
                        "description": "Search ORDER_TRACKING_INFO by cworderid from Step 1"
                    },
                    
                    # Step 3: Retrieve Order Instances
                    {
                        "sequence": 3,
                        "action": "retrieve_order_instances",
                        "tool": "search_order_instances",
                        "parameters": {
                            "cwdocid": "${from_step_1}",  # Extracted by Execution Agent
                            "limit": 50,
                            "include_blob_data": False
                        },
                        "status": "pending",
                        "description": "Search CWORDERINSTANCE by cwdocid from Step 1"
                    },
                    
                    # Step 4: Retrieve Message Logs
                    {
                        "sequence": 4,
                        "action": "retrieve_message_logs",
                        "tool": "search_message_logs",
                        "parameters": {
                            "user_data1": search_value,  # Use original search value
                            "limit": 50,
                            "include_blob_data": True
                        },
                        "status": "pending",
                        "description": f"Search CWMESSAGELOG by user_data1={search_value}"
                    },
                    
                    # Step 5: Detect Execution Flow
                    {
                        "sequence": 5,
                        "action": "detect_execution_flow",
                        "tool": "detect_flow_from_logs",
                        "parameters": {
                            "message_logs": "${from_step_4}",
                            "install_type": "${from_step_1}"
                        },
                        "status": "pending",
                        "description": "Detect execution flows from message logs (rule-based)"
                    },
                    
                    # Step 6: Retrieve Expected Behavior
                    {
                        "sequence": 6,
                        "action": "retrieve_expected_behavior",
                        "tool": "get_process_flow",
                        "parameters": {
                            "flow_type": "${from_step_5}"
                        },
                        "status": "pending",
                        "description": "Get expected flow documentation from Knowledge Server"
                    },
                    
                    # Step 7: Analyze Expected vs Actual
                    {
                        "sequence": 7,
                        "action": "analyze_expected_vs_actual",
                        "tool": "llm_analyze",
                        "parameters": {
                            "all_collected_data": "${from_all_steps}",
                            "expected_behavior": "${from_step_6}",
                            "detected_flows": "${from_step_5}"
                        },
                        "status": "pending",
                        "description": "LLM analyzes expected vs actual behavior"
                    },
                    
                    # Step 8: Format Response
                    {
                        "sequence": 8,
                        "action": "format_response",
                        "tool": "format_output",
                        "parameters": {
                            "analysis": "${from_step_7}",
                            "search_input": "${search_input}"
                        },
                        "status": "pending",
                        "description": "Format final analysis response"
                    }
                ],
                "created_at": datetime.now().isoformat(),
                "plan_type": "static_v1"
            }
            
            logger.info(f"✅ Plan created with 8 steps")
            
            return {
                "success": True,
                "plan": plan,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Planning failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
