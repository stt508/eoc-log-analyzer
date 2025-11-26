"""
Database API Client for EOC Log Analyzer

Client for calling the eoc-database-api service to access:
- CWMESSAGELOG (message logs)
- ORDER_ORDER_HEADER (order headers)
- ORDER_TRACKING_INFO (order tracking with error detection)

All database operations go through HTTP API calls - no direct Oracle connections.
"""

import httpx
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

from config import config

class DatabaseAPIClient:
    """Client for the EOC Database API Service"""
    
    def __init__(self):
        # Get API configuration from environment
        self.api_base_url = getattr(config.app, 'database_api_url', 'http://localhost:8001')
        self.api_key = getattr(config.app, 'database_api_key', None)
        self.timeout = getattr(config.app, 'api_timeout', 30)
        
        # Set up headers
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "EOC-Log-Analyzer-AI-Agent/1.0"
        }
        
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"
        
        logger.info(f"Database API client initialized - URL: {self.api_base_url}")
    
    def _make_sync_request(self, endpoint: str, method: str = "GET", **kwargs) -> Dict[str, Any]:
        """Make synchronous HTTP request to the database API"""
        
        url = f"{self.api_base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        with httpx.Client(timeout=self.timeout) as client:
            try:
                response = client.request(
                    method=method,
                    url=url,
                    headers=self.headers,
                    **kwargs
                )
                
                response.raise_for_status()
                return response.json()
                
            except httpx.TimeoutException:
                logger.error(f"Database API request timed out: {url}")
                raise
            except httpx.HTTPStatusError as e:
                logger.error(f"Database API HTTP error {e.response.status_code}: {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"Database API request failed: {e}")
                raise
    
    # ========================================================================
    # CWMESSAGELOG Methods
    # ========================================================================
    
    def search_message_logs(self, 
                           user_data1: Optional[str] = None,
                           user_data2: Optional[str] = None, 
                           user_data3: Optional[str] = None,
                           order_id: Optional[str] = None,
                           customer_id: Optional[str] = None,
                           operation: Optional[str] = None,
                           start_date: Optional[str] = None,
                           end_date: Optional[str] = None,
                           limit: int = 50,
                           include_blob_data: bool = False) -> List[Dict[str, Any]]:
        """
        Search message logs from CWMESSAGELOG table by various criteria
        
        Args:
            user_data1: Primary identifier (e.g., phone number, account)
            user_data2: Secondary identifier
            user_data3: Tertiary identifier
            order_id: Order ID
            customer_id: Customer ID
            operation: Operation name
            start_date: Start date for filtering (ISO format)
            end_date: End date for filtering (ISO format)
            limit: Maximum number of results (default 50)
            include_blob_data: Include BLOB data (SEND_DATA, RECEIVE_DATA) - default False
        
        Returns:
            List of message log entries
        """
        
        try:
            criteria = {
                "limit": limit,
                "include_blob_data": include_blob_data
            }
            
            if user_data1:
                criteria["user_data1"] = user_data1
            if user_data2:
                criteria["user_data2"] = user_data2
            if user_data3:
                criteria["user_data3"] = user_data3
            if order_id:
                criteria["order_id"] = order_id
            if customer_id:
                criteria["customer_id"] = customer_id
            if operation:
                criteria["operation"] = operation
            if start_date:
                criteria["start_date"] = start_date
            if end_date:
                criteria["end_date"] = end_date
            
            result = self._make_sync_request("message-logs/search", method="POST", json=criteria)
            
            if isinstance(result, dict) and result.get("messages"):
                return result["messages"]
            return []
            
        except Exception as e:
            logger.error(f"Failed to search message logs: {e}")
            return []
    
    # ========================================================================
    # ORDER_ORDER_HEADER Methods
    # ========================================================================
    
    def search_orders(self,
                     cworderid: Optional[str] = None,
                     omorderid: Optional[str] = None,
                     quoteid: Optional[str] = None,
                     telephonenumber: Optional[str] = None,
                     universalserviceid: Optional[str] = None,
                     ordertype: Optional[str] = None,
                     stagecode: Optional[str] = None,
                     start_date: Optional[str] = None,
                     end_date: Optional[str] = None,
                     limit: int = 50,
                     include_blob_data: bool = False) -> List[Dict[str, Any]]:
        """
        Search order headers from ORDER_ORDER_HEADER table
        
        Args:
            cworderid: CW Order ID
            omorderid: OM Order ID
            quoteid: Quote ID
            telephonenumber: Telephone number
            universalserviceid: Universal Service ID
            ordertype: Order type
            stagecode: Stage code
            start_date: Start date (ISO format)
            end_date: End date (ISO format)
            limit: Maximum results (default 50)
            include_blob_data: Include NCLOB fields (default False)
        
        Returns:
            List of order header entries
        """
        
        try:
            criteria = {
                "limit": limit,
                "include_blob_data": include_blob_data
            }
            
            if cworderid:
                criteria["cworderid"] = cworderid
            if omorderid:
                criteria["omorderid"] = omorderid
            if quoteid:
                criteria["quoteid"] = quoteid
            if telephonenumber:
                criteria["telephonenumber"] = telephonenumber
            if universalserviceid:
                criteria["universalserviceid"] = universalserviceid
            if ordertype:
                criteria["ordertype"] = ordertype
            if stagecode:
                criteria["stagecode"] = stagecode
            if start_date:
                criteria["start_date"] = start_date
            if end_date:
                criteria["end_date"] = end_date
            
            result = self._make_sync_request("orders/search", method="POST", json=criteria)
            
            if isinstance(result, dict) and result.get("orders"):
                return result["orders"]
            return []
            
        except Exception as e:
            logger.error(f"Failed to search orders: {e}")
            return []
    
    # ========================================================================
    # ORDER_TRACKING_INFO Methods
    # ========================================================================
    
    def search_order_tracking(self,
                             cworderid: Optional[str] = None,
                             orderid: Optional[str] = None,
                             workid: Optional[str] = None,
                             scaseid: Optional[str] = None,
                             icaseid: Optional[str] = None,
                             orderstatus: Optional[str] = None,
                             casestatus: Optional[str] = None,
                             flowstatus: Optional[str] = None,
                             has_errors: Optional[bool] = None,
                             start_date: Optional[str] = None,
                             end_date: Optional[str] = None,
                             limit: int = 50,
                             include_blob_data: bool = False) -> List[Dict[str, Any]]:
        """
        Search order tracking from ORDER_TRACKING_INFO table with smart error detection
        
        Args:
            cworderid: CW Order ID
            orderid: Order ID
            workid: Work ID
            scaseid: SCASE ID
            icaseid: ICASE ID
            orderstatus: Order status
            casestatus: Case status
            flowstatus: Flow status
            has_errors: Filter for orders with/without errors (checks 13+ error fields)
            start_date: Start date (ISO format)
            end_date: End date (ISO format)
            limit: Maximum results (default 50)
            include_blob_data: Include NCLOB error messages (default False)
        
        Returns:
            List of order tracking entries
        """
        
        try:
            criteria = {
                "limit": limit,
                "include_blob_data": include_blob_data
            }
            
            if cworderid:
                criteria["cworderid"] = cworderid
            if orderid:
                criteria["orderid"] = orderid
            if workid:
                criteria["workid"] = workid
            if scaseid:
                criteria["scaseid"] = scaseid
            if icaseid:
                criteria["icaseid"] = icaseid
            if orderstatus:
                criteria["orderstatus"] = orderstatus
            if casestatus:
                criteria["casestatus"] = casestatus
            if flowstatus:
                criteria["flowstatus"] = flowstatus
            if has_errors is not None:
                criteria["has_errors"] = has_errors
            if start_date:
                criteria["start_date"] = start_date
            if end_date:
                criteria["end_date"] = end_date
            
            result = self._make_sync_request("order-tracking/search", method="POST", json=criteria)
            
            if isinstance(result, dict) and result.get("tracking_records"):
                return result["tracking_records"]
            return []
            
        except Exception as e:
            logger.error(f"Failed to search order tracking: {e}")
            return []
    
    # ========================================================================
    # CWORDERINSTANCE Methods
    # ========================================================================
    
    def search_order_instances(self,
                              cwdocid: Optional[str] = None,
                              customerid: Optional[str] = None,
                              accountid: Optional[str] = None,
                              ordertype: Optional[str] = None,
                              ordersubtype: Optional[str] = None,
                              status: Optional[str] = None,
                              state: Optional[str] = None,
                              quoteid: Optional[str] = None,
                              externalorderid: Optional[str] = None,
                              productcode: Optional[str] = None,
                              parentorder: Optional[str] = None,
                              start_date: Optional[str] = None,
                              end_date: Optional[str] = None,
                              limit: int = 50,
                              include_blob_data: bool = False) -> List[Dict[str, Any]]:
        """
        Search order instances from CWORDERINSTANCE table
        
        Args:
            cwdocid: CW Document ID
            customerid: Customer ID
            accountid: Account ID
            ordertype: Order type
            ordersubtype: Order subtype
            status: Status (single character)
            state: Order state
            quoteid: Quote ID
            externalorderid: External Order ID
            productcode: Product code
            parentorder: Parent order ID
            start_date: Start date (ISO format)
            end_date: End date (ISO format)
            limit: Maximum results (default 50)
            include_blob_data: Include NCLOB fields (default False)
        
        Returns:
            List of order instance entries
        """
        
        try:
            criteria = {
                "limit": limit,
                "include_blob_data": include_blob_data
            }
            
            if cwdocid:
                criteria["cwdocid"] = cwdocid
            if customerid:
                criteria["customerid"] = customerid
            if accountid:
                criteria["accountid"] = accountid
            if ordertype:
                criteria["ordertype"] = ordertype
            if ordersubtype:
                criteria["ordersubtype"] = ordersubtype
            if status:
                criteria["status"] = status
            if state:
                criteria["state"] = state
            if quoteid:
                criteria["quoteid"] = quoteid
            if externalorderid:
                criteria["externalorderid"] = externalorderid
            if productcode:
                criteria["productcode"] = productcode
            if parentorder:
                criteria["parentorder"] = parentorder
            if start_date:
                criteria["start_date"] = start_date
            if end_date:
                criteria["end_date"] = end_date
            
            result = self._make_sync_request("order-instances/search", method="POST", json=criteria)
            
            if isinstance(result, dict) and result.get("order_instances"):
                return result["order_instances"]
            return []
            
        except Exception as e:
            logger.error(f"Failed to search order instances: {e}")
            return []
    


# ============================================================================
# Global API Client Instance
# ============================================================================

api_client = DatabaseAPIClient()


# ============================================================================
# LangChain Tool Functions - CWMESSAGELOG
# ============================================================================

def search_message_logs_tool(search_criteria: str) -> str:
    """
    Search message logs from CWMESSAGELOG table by various criteria
    
    Input: JSON string with criteria such as user_data1, user_data2, user_data3,
    order_id, operation, start_date, end_date, limit, include_blob_data
    """
    
    try:
        criteria = json.loads(search_criteria) if isinstance(search_criteria, str) else search_criteria
        result = api_client.search_message_logs(**criteria)
        
        if result:
            return json.dumps({
                "success": True,
                "total_found": len(result),
                "messages": result
            }, indent=2, default=str)
        else:
            return json.dumps({"success": True, "total_found": 0, "messages": []}, indent=2)
    except json.JSONDecodeError:
        return json.dumps({
            "success": False,
            "error": "Invalid search criteria format. Expected JSON string."
        }, indent=2)
    except Exception as e:
        logger.error(f"Message log search tool failed: {e}")
        return json.dumps({"success": False, "error": f"Error: {str(e)}"}, indent=2)


def get_message_log_by_id_tool(msgid: str) -> str:
    """Get a specific message log by MSGID from CWMESSAGELOG"""
    
    try:
        result = api_client.get_message_log_by_id(msgid)
        if result:
            return json.dumps({"success": True, "message": result}, indent=2, default=str)
        else:
            return json.dumps({"success": False, "error": f"Message log {msgid} not found"}, indent=2)
    except Exception as e:
        logger.error(f"Get message log tool failed: {e}")
        return json.dumps({"success": False, "error": f"Error: {str(e)}"}, indent=2)


# ============================================================================
# LangChain Tool Functions - ORDER_ORDER_HEADER
# ============================================================================

def search_orders_tool(search_criteria: str) -> str:
    """
    Search orders from ORDER_ORDER_HEADER table
    
    Input: JSON string with criteria such as cworderid, telephonenumber, ordertype,
    stagecode, quoteid, omorderid, start_date, end_date, limit, include_blob_data
    """
    
    try:
        criteria = json.loads(search_criteria) if isinstance(search_criteria, str) else search_criteria
        result = api_client.search_orders(**criteria)
        
        if result:
            return json.dumps({
                "success": True,
                "total_found": len(result),
                "orders": result
            }, indent=2, default=str)
        else:
            return json.dumps({"success": True, "total_found": 0, "orders": []}, indent=2)
    except json.JSONDecodeError:
        return json.dumps({
            "success": False,
            "error": "Invalid search criteria format. Expected JSON string."
        }, indent=2)
    except Exception as e:
        logger.error(f"Order search tool failed: {e}")
        return json.dumps({"success": False, "error": f"Error: {str(e)}"}, indent=2)


def get_order_by_cwdocid_tool(cwdocid: str) -> str:
    """Get a specific order by CWDOCID (primary key) from ORDER_ORDER_HEADER"""
    
    try:
        result = api_client.get_order_by_cwdocid(cwdocid)
        if result:
            return json.dumps({"success": True, "order": result}, indent=2, default=str)
        else:
            return json.dumps({"success": False, "error": f"Order {cwdocid} not found"}, indent=2)
    except Exception as e:
        logger.error(f"Get order tool failed: {e}")
        return json.dumps({"success": False, "error": f"Error: {str(e)}"}, indent=2)


def get_orders_by_cworderid_tool(cworderid: str) -> str:
    """Quick search for orders by CW Order ID from ORDER_ORDER_HEADER"""
    
    try:
        result = api_client.get_orders_by_cworderid(cworderid)
        return json.dumps({
            "success": True,
            "total_found": len(result),
            "cworderid": cworderid,
            "orders": result
        }, indent=2, default=str)
    except Exception as e:
        logger.error(f"Get orders by cworderid tool failed: {e}")
        return json.dumps({"success": False, "error": f"Error: {str(e)}"}, indent=2)


def get_orders_by_telephone_tool(telephonenumber: str) -> str:
    """Quick search for orders by telephone number from ORDER_ORDER_HEADER"""
    
    try:
        result = api_client.get_orders_by_telephone(telephonenumber)
        return json.dumps({
            "success": True,
            "total_found": len(result),
            "telephonenumber": telephonenumber,
            "orders": result
        }, indent=2, default=str)
    except Exception as e:
        logger.error(f"Get orders by telephone tool failed: {e}")
        return json.dumps({"success": False, "error": f"Error: {str(e)}"}, indent=2)


# ============================================================================
# LangChain Tool Functions - ORDER_TRACKING_INFO
# ============================================================================

def search_order_tracking_tool(search_criteria: str) -> str:
    """
    Search order tracking from ORDER_TRACKING_INFO table with smart error detection
    
    Input: JSON string with criteria such as cworderid, orderid, workid, orderstatus,
    flowstatus, casestatus, has_errors, start_date, end_date, limit, include_blob_data
    """
    
    try:
        criteria = json.loads(search_criteria) if isinstance(search_criteria, str) else search_criteria
        result = api_client.search_order_tracking(**criteria)
        
        if result:
            return json.dumps({
                "success": True,
                "total_found": len(result),
                "tracking_records": result
            }, indent=2, default=str)
        else:
            return json.dumps({"success": True, "total_found": 0, "tracking_records": []}, indent=2)
    except json.JSONDecodeError:
        return json.dumps({
            "success": False,
            "error": "Invalid search criteria format. Expected JSON string."
        }, indent=2)
    except Exception as e:
        logger.error(f"Order tracking search tool failed: {e}")
        return json.dumps({"success": False, "error": f"Error: {str(e)}"}, indent=2)




# ============================================================================
# LangChain Tool Functions - CWORDERINSTANCE
# ============================================================================

def search_order_instances_tool(search_criteria: str) -> str:
    """
    Search order instances from CWORDERINSTANCE table
    
    Input: JSON string with criteria such as cwdocid, customerid, accountid, ordertype,
    ordersubtype, status, state, quoteid, externalorderid, productcode, parentorder,
    start_date, end_date, limit, include_blob_data
    """
    
    try:
        criteria = json.loads(search_criteria) if isinstance(search_criteria, str) else search_criteria
        result = api_client.search_order_instances(**criteria)
        
        if result:
            return json.dumps({
                "success": True,
                "total_found": len(result),
                "order_instances": result
            }, indent=2, default=str)
        else:
            return json.dumps({"success": True, "total_found": 0, "order_instances": []}, indent=2)
    except json.JSONDecodeError:
        return json.dumps({
            "success": False,
            "error": "Invalid search criteria format. Expected JSON string."
        }, indent=2)
    except Exception as e:
        logger.error(f"Order instance search tool failed: {e}")
        return json.dumps({"success": False, "error": f"Error: {str(e)}"}, indent=2)




# ============================================================================
# PLAN MANAGEMENT TOOLS (for saving/retrieving troubleshooting plans)
# ============================================================================

def search_plans_tool(search_criteria: str) -> str:
    """Search troubleshooting plans by goal_type, order_type, success_rate"""
    
    try:
        criteria = json.loads(search_criteria)
        result = api_client._make_sync_request(
            endpoint="plans/search",
            method="POST",
            json=criteria
        )
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        logger.error(f"Search plans tool failed: {e}")
        return json.dumps({"success": False, "error": f"Error: {str(e)}"}, indent=2)

def get_plan_by_id_tool(plan_id: str) -> str:
    """Get a specific troubleshooting plan by ID"""
    
    try:
        result = api_client._make_sync_request(
            endpoint=f"plans/{plan_id}",
            method="GET"
        )
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        logger.error(f"Get plan by ID tool failed: {e}")
        return json.dumps({"success": False, "error": f"Error: {str(e)}"}, indent=2)

def save_new_plan_tool(plan_data: str) -> str:
    """Save a new troubleshooting plan to the database"""
    
    try:
        plan = json.loads(plan_data)
        result = api_client._make_sync_request(
            endpoint="plans",
            method="POST",
            json=plan
        )
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        logger.error(f"Save new plan tool failed: {e}")
        return json.dumps({"success": False, "error": f"Error: {str(e)}"}, indent=2)

def update_plan_usage_tool(plan_id: str, success: str) -> str:
    """Update plan usage statistics after execution (success must be 'true' or 'false')"""
    
    try:
        success_bool = success.lower() == 'true'
        result = api_client._make_sync_request(
            endpoint=f"plans/{plan_id}/usage",
            method="POST",
            json={"success": success_bool}
        )
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        logger.error(f"Update plan usage tool failed: {e}")
        return json.dumps({"success": False, "error": f"Error: {str(e)}"}, indent=2)


# ============================================================================
# API Tools List for LangChain Agents
# ============================================================================

API_TOOLS = [
    # CWMESSAGELOG Tools
    {
        "name": "search_message_logs",
        "function": search_message_logs_tool,
        "description": """Search message logs from CWMESSAGELOG table by various criteria. 
        Input: JSON string with search criteria. 
        
        Available fields:
        - user_data1: Primary identifier (phone number, account, etc.)
        - user_data2: Secondary identifier
        - user_data3: Tertiary identifier
        - order_id: Order ID
        - customer_id: Customer ID
        - operation: Operation name (e.g., "ProcessOrder", "SendNotification")
        - start_date: Start date (ISO format, e.g., 2024-01-01)
        - end_date: End date (ISO format)
        - limit: Max results (default 50, max 1000)
        - include_blob_data: Include SEND_DATA/RECEIVE_DATA (default false)"""
    },
    {
        "name": "get_message_log_by_id",
        "function": get_message_log_by_id_tool,
        "description": """Get a specific message log entry by MSGID from CWMESSAGELOG table. 
        Returns complete log entry including BLOB data (SEND_DATA, RECEIVE_DATA).
        Input: msgid (string, e.g., "123456")"""
    },
    
    # ORDER_ORDER_HEADER Tools
    {
        "name": "search_orders",
        "function": search_orders_tool,
        "description": """Search order headers from ORDER_ORDER_HEADER table by various criteria.
        Input: JSON string with search criteria.
        
        Available fields:
        - cworderid: CW Order ID
        - omorderid: OM Order ID
        - quoteid: Quote ID
        - telephonenumber: Telephone number
        - universalserviceid: Universal Service ID
        - ordertype: Order type
        - stagecode: Stage code (order stage)
        - start_date: Start date (ISO format)
        - end_date: End date (ISO format)
        - limit: Max results (default 50, max 1000)
        - include_blob_data: Include NCLOB fields (default false)"""
    },
    {
        "name": "get_order_by_cwdocid",
        "function": get_order_by_cwdocid_tool,
        "description": """Get a specific order by CWDOCID (primary key) from ORDER_ORDER_HEADER.
        Returns complete order header including NCLOB fields.
        Input: cwdocid (string)"""
    },
    {
        "name": "get_orders_by_cworderid",
        "function": get_orders_by_cworderid_tool,
        "description": """Quick search for orders by CW Order ID from ORDER_ORDER_HEADER.
        Returns up to 100 most recent orders matching the CW Order ID.
        Input: cworderid (string)"""
    },
    {
        "name": "get_orders_by_telephone",
        "function": get_orders_by_telephone_tool,
        "description": """Quick search for orders by telephone number from ORDER_ORDER_HEADER.
        Returns up to 100 most recent orders matching the telephone number.
        Input: telephonenumber (string, e.g., "5551234567")"""
    },
    
    # ORDER_TRACKING_INFO Tools
    {
        "name": "search_order_tracking",
        "function": search_order_tracking_tool,
        "description": """Search order tracking from ORDER_TRACKING_INFO table with smart error detection.
        Input: JSON string with search criteria.
        
        Available fields:
        - cworderid: CW Order ID
        - orderid: Order ID
        - workid: Work ID
        - scaseid: SCASE ID
        - icaseid: ICASE ID
        - orderstatus: Order status
        - casestatus: Case status
        - flowstatus: Flow status
        - has_errors: Boolean - filter for orders with/without errors (checks 13+ error fields)
        - start_date: Start date (ISO format)
        - end_date: End date (ISO format)
        - limit: Max results (default 50, max 1000)
        - include_blob_data: Include NCLOB error messages (default false)
        
        The has_errors field intelligently checks multiple error indicators:
        WFMERRORID, PREORDERERRORSYSTEMS, TRIADERRORID_IA, DPIERRORID_DISP, DPIERRORID_IA,
        DPIUMERRORID_IA, TCERRORID_IA, CUSTOMERNOTIFERRORID_IA, HASDPIEVERERRORED, etc."""
    },
    {
        "name": "get_order_tracking_with_errors",
        "function": get_order_tracking_with_errors_tool,
        "description": """Get all order tracking records that have ANY errors from ORDER_TRACKING_INFO.
        Automatically checks 13+ error fields and returns orders with problems, including full error messages.
        This is the BEST tool for troubleshooting failed orders.
        Input: limit (string, optional, default "50")"""
    },
    {
        "name": "get_order_tracking_by_cworderid",
        "function": get_order_tracking_by_cworderid_tool,
        "description": """Quick search for order tracking by CW Order ID from ORDER_TRACKING_INFO.
        Returns up to 100 most recent tracking records matching the CW Order ID.
        Input: cworderid (string)"""
    },
    
    # CWORDERINSTANCE Tools
    {
        "name": "search_order_instances",
        "function": search_order_instances_tool,
        "description": """Search order instances from CWORDERINSTANCE table (core order metadata).
        Input: JSON string with search criteria.
        
        Available fields:
        - cwdocid: CW Document ID
        - customerid: Customer ID
        - accountid: Account ID
        - ordertype: Order type
        - ordersubtype: Order subtype
        - status: Status (single character)
        - state: Order state (e.g., "COMPLETE", "PENDING")
        - quoteid: Quote ID
        - externalorderid: External Order ID
        - productcode: Product code
        - parentorder: Parent order ID
        - start_date: Start date (ISO format)
        - end_date: End date (ISO format)
        - limit: Max results (default 50, max 1000)
        - include_blob_data: Include NCLOB fields (attrs, notes, relatedentities, etc.)
        
        Use for: Order metadata, pricing, state/status, relationships, product codes"""
    },
    {
        "name": "get_order_instance_by_cwdocid",
        "function": get_order_instance_by_cwdocid_tool,
        "description": """Get a specific order instance by CWDOCID (primary key) from CWORDERINSTANCE.
        Returns complete order instance metadata including NCLOB fields (attrs, notes, etc.).
        Input: cwdocid (string)"""
    },
    {
        "name": "get_order_instances_by_customerid",
        "function": get_order_instances_by_customerid_tool,
        "description": """Quick search for order instances by Customer ID from CWORDERINSTANCE.
        Returns up to 100 most recent order instances for the customer.
        Input: customerid (string)"""
    },
    {
        "name": "get_order_instances_by_quoteid",
        "function": get_order_instances_by_quoteid_tool,
        "description": """Quick search for order instances by Quote ID from CWORDERINSTANCE.
        Returns up to 100 most recent order instances matching the quote.
        Input: quoteid (string)"""
    },
    
    # PLAN MANAGEMENT Tools
    {
        "name": "search_plans",
        "function": search_plans_tool,
        "description": """Search for existing troubleshooting plans by criteria.
        Use this to find existing plans before creating a new one.
        Input: JSON string with search criteria.
        
        Available fields:
        - goal_type: Type of goal (e.g., "order_analysis", "error_investigation")
        - order_type: Specific order type (e.g., fiber_installation, new_service)
        - is_active: 1 for active plans, 0 for archived
        - min_success_rate: Minimum success rate (0.0 to 1.0, e.g., 0.7 for 70%)
        - limit: Max results (default 50, max 500)
        
        Use this FIRST to check if a suitable plan already exists before creating a new one."""
    },
    {
        "name": "get_plan_by_id",
        "function": get_plan_by_id_tool,
        "description": """Get a specific troubleshooting plan by its ID.
        Returns the complete plan including steps, expected outcomes, and success statistics.
        Input: plan_id (string, e.g., "a1b2c3d4e5f6")"""
    },
    {
        "name": "save_new_plan",
        "function": save_new_plan_tool,
        "description": """Save a NEW troubleshooting plan to the database.
        Use this AFTER determining no suitable existing plan exists.
        Input: JSON string with plan data.
        
        Required fields:
        - goal_type: Type of goal (e.g., order_analysis)
        - title: Clear, descriptive title
        - steps: JSON string of troubleshooting steps array
        - confidence: Your confidence in this plan (0.0 to 1.0)
        
        Optional fields:
        - order_type: Specific order type if applicable
        - description: Detailed description of when to use this plan
        - expected_outcomes: JSON string of expected outcomes array
        
        IMPORTANT: Always search_plans FIRST before saving a new plan!"""
    },
    {
        "name": "update_plan_usage",
        "function": update_plan_usage_tool,
        "description": """Update plan usage statistics after executing a plan.
        This tracks how often plans are used and their success rate.
        Input: plan_id (string), success (string: 'true' or 'false')
        
        Call this AFTER executing a plan to track its effectiveness."""
    }
]
