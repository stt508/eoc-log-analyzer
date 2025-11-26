"""
Coordinator Agent for Oracle Log Analysis (Phase 1)

Orchestrates planning and execution:
1. Calls Planning Agent to get static 8-step plan
2. Logs plan to terminal
3. Executes Step 1 to get orders
4. For each order found, executes steps 2-8
5. Manages memory and placeholder resolution
6. Returns final results

The Coordinator is SMART - it manages the flow.
The Execution Agent is DUMB - it just executes what it's told.
"""

import json
from typing import Dict, Any, Optional, List
from datetime import datetime
from loguru import logger

from agents.planning_agent import PlanningAgent
from agents.execution_agent import ExecutionAgent


class CoordinatorAgent:
    """Smart coordinator that manages planning and execution"""
    
    def __init__(self):
        self.planning_agent = PlanningAgent()
        self.execution_agent = ExecutionAgent()
        logger.info("✅ Coordinator Agent initialized")
    
    def _log_plan(self, plan: Dict[str, Any]):
        """Log the plan to terminal"""
        logger.info("=" * 70)
        logger.info("📋 EXECUTION PLAN")
        logger.info("=" * 70)
        logger.info(f"Search: {plan['search_input']['type']} = {plan['search_input']['value']}")
        logger.info(f"Total Steps: {len(plan['steps'])}")
        logger.info("")
        for step in plan['steps']:
            logger.info(f"  Step {step['sequence']}: {step['action']}")
            logger.info(f"    Tool: {step['tool']}")
            logger.info(f"    Description: {step['description']}")
        logger.info("=" * 70)
        logger.info("")
    
    def _resolve_placeholder(self, value: str, order_memory: Dict[str, Any]) -> Any:
        """
        Resolve placeholder like ${from_step_1} to actual value
        
        Args:
            value: Placeholder string or actual value
            order_memory: Memory for this specific order
        
        Returns:
            Resolved value
        """
        if not isinstance(value, str) or not value.startswith("${"):
            return value  # Not a placeholder
        
        # Extract step reference: ${from_step_1} -> step_1
        if value == "${from_step_1}":
            # Extract cworderid or cwdocid from step 1
            step_1_result = order_memory.get("step_1", {}).get("result", [])
            if step_1_result and len(step_1_result) > 0:
                order = step_1_result[0]
                # Return cworderid (used by step 2 and others)
                return order.get("cworderid")
        
        elif value == "${from_step_4}":
            # Return message logs from step 4
            return order_memory.get("step_4", {}).get("result", [])
        
        elif value == "${from_step_5}":
            # Return detected flows from step 5
            return order_memory.get("step_5", {}).get("result", {})
        
        elif value == "${from_step_6}":
            # Return expected behavior from step 6
            return order_memory.get("step_6", {}).get("result", "")
        
        elif value == "${from_all_steps}":
            # Return all collected data
            return order_memory
        
        elif value == "${search_input}":
            # Return original search input
            return order_memory.get("order_info", {})
        
        # Default: return as-is
        return value
    
    def _resolve_parameters(self, parameters: Dict[str, Any], order_memory: Dict[str, Any]) -> Dict[str, Any]:
        """
        Resolve all placeholders in step parameters
        
        Args:
            parameters: Step parameters (may contain placeholders)
            order_memory: Memory for this specific order
        
        Returns:
            Parameters with resolved values
        """
        resolved = {}
        for key, value in parameters.items():
            resolved[key] = self._resolve_placeholder(value, order_memory)
        return resolved
    
    def analyze_order(self, search_type: str, search_value: str, goal: str = None) -> Dict[str, Any]:
        """
        Main entry point for order analysis
        
        Args:
            search_type: Type of search (phone_number, order_number_dpi, etc.)
            search_value: Value to search for
            goal: Optional analysis goal
        
        Returns:
            Dictionary with analysis results
        """
        start_time = datetime.now()
        
        logger.info("=" * 70)
        logger.info(f"🎯 COORDINATOR: Starting analysis")
        logger.info(f"   Search: {search_type} = {search_value}")
        logger.info(f"   Goal: {goal or 'General troubleshooting'}")
        logger.info("=" * 70)
        logger.info("")
        
        try:
            # ================================================================
            # PHASE 1: GET PLAN FROM PLANNING AGENT
            # ================================================================
            logger.info("📞 Calling Planning Agent...")
            plan_result = self.planning_agent.create_plan(search_type, search_value)
            
            if not plan_result["success"]:
                logger.error(f"❌ Planning failed: {plan_result.get('error')}")
                return {
                    "success": False,
                    "stage": "planning",
                    "error": plan_result.get("error", "Planning failed"),
                    "timestamp": datetime.now().isoformat()
                }
            
            plan = plan_result["plan"]
            logger.info("✅ Plan received from Planning Agent")
            logger.info("")
            
            # Log the plan
            self._log_plan(plan)
            
            # ================================================================
            # PHASE 2: EXECUTE STEP 1 (Get Orders)
            # ================================================================
            logger.info("▶️  EXECUTING STEP 1: Retrieve Order Header")
            logger.info("-" * 70)
            
            step_1 = plan['steps'][0]
            step_1_result = self.execution_agent.execute_step(
                step=step_1,
                params=step_1['parameters'],
                memory={}
            )
            
            # Check if any orders found
            if step_1_result['count'] == 0:
                logger.error(f"❌ No orders found for {search_type}={search_value}")
                return {
                    "success": False,
                    "stage": "execution",
                    "error": f"No orders found for {search_type}={search_value}",
                    "stopped_at_step": 1,
                    "timestamp": datetime.now().isoformat()
                }
            
            orders = step_1_result['result']
            logger.info(f"✅ Step 1 complete: Found {len(orders)} order(s)")
            logger.info("")
            
            # ================================================================
            # PHASE 3: EXECUTE STEPS 2-8 FOR EACH ORDER
            # ================================================================
            memory = {}
            
            for order_idx, order in enumerate(orders):
                logger.info("=" * 70)
                logger.info(f"🔄 PROCESSING ORDER {order_idx + 1} of {len(orders)}")
                logger.info(f"   Order ID: {order.get('cworderid', 'N/A')}")
                logger.info(f"   DPI Order: {order.get('dpiordernumber', 'N/A')}")
                logger.info("=" * 70)
                logger.info("")
                
                # Create memory for this order
                order_memory = {
                    "order_info": {
                        "cworderid": order.get('cworderid'),
                        "dpiordernumber": order.get('dpiordernumber'),
                        "omorderid": order.get('omorderid'),
                        "billingtelephonenumber": order.get('billingtelephonenumber'),
                        "installtype": order.get('installtype')
                    },
                    "step_1": {
                        "action": "retrieve_order_header",
                        "status": "completed",
                        "result": [order],
                        "count": 1,
                        "timestamp": step_1_result['timestamp']
                    }
                }
                
                # Execute steps 2-8 for this order
                for step in plan['steps'][1:]:  # Skip step 1 (already done)
                    step_num = step['sequence']
                    logger.info(f"▶️  EXECUTING STEP {step_num}: {step['action']}")
                    logger.info(f"   Tool: {step['tool']}")
                    
                    # Resolve placeholders in parameters
                    resolved_params = self._resolve_parameters(step['parameters'], order_memory)
                    
                    # Execute step
                    result = self.execution_agent.execute_step(
                        step=step,
                        params=resolved_params,
                        memory=order_memory
                    )
                    
                    # Store result in memory
                    order_memory[f"step_{step_num}"] = result
                    
                    logger.info(f"✅ Step {step_num} complete")
                    if result.get('count') is not None:
                        logger.info(f"   Records: {result['count']}")
                    logger.info("")
                
                # Store this order's memory
                memory[f"order_{order_idx}"] = order_memory
                
                logger.info(f"✅ Order {order_idx + 1} processing complete")
                logger.info("")
            
            # ================================================================
            # PHASE 4: RETURN RESULTS
            # ================================================================
            elapsed_time = (datetime.now() - start_time).total_seconds() * 1000
            
            logger.info("=" * 70)
            logger.info("✅ COORDINATOR: Analysis completed successfully")
            logger.info(f"   Orders processed: {len(orders)}")
            logger.info(f"   Execution time: {elapsed_time:.0f}ms")
            logger.info("=" * 70)
            logger.info("")
            
            return {
                "success": True,
                "search_input": plan['search_input'],
                "total_orders": len(orders),
                "memory": memory,
                "execution_time_ms": elapsed_time,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Coordinator failed: {e}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "stage": "coordination",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }


# Global coordinator instance
coordinator = CoordinatorAgent()
