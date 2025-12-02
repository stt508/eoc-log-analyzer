"""
EOC Log Analyzer - Web UI

Streamlit-based web interface for analyzing message logs with AI assistance.
"""

import streamlit as st
from datetime import datetime
from loguru import logger
import sys

# Configure page
st.set_page_config(
    page_title="EOC Log Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"  # Minimize sidebar by default
)

# Configure logging
logger.remove()
logger.add(sys.stdout, level="INFO")

from config import config
from tools.database_api_client import api_client
from agents import coordinator
from tools.knowledge_server import knowledge_server
from tools.knowledge_server.chroma_vector_manager import get_chroma_manager
import subprocess
import os

# Custom CSS - Compact layout with toolbar space
st.markdown("""
<style>
    /* Ensure content is below Streamlit toolbar */
    .block-container {
        padding-top: 4rem !important;
        padding-bottom: 0rem !important;
        margin-top: 0 !important;
    }
    /* Make toolbar opaque to avoid overlap issues */
    header[data-testid="stHeader"] {
        background-color: white;
        z-index: 999;
    }
    /* Adjust main content area */
    .main .block-container {
        max-width: 100%;
    }
    .stForm {
        margin-bottom: 0.5rem !important;
    }
    /* Compact log entries */
    .log-entry {
        padding: 6px;
        margin: 3px 0;
        border-left: 2px solid #4CAF50;
        background-color: #f5f5f5;
        border-radius: 3px;
        font-size: 0.9em;
    }
    .log-time {
        color: #666;
        font-size: 0.85em;
    }
    .log-operation {
        font-weight: bold;
        color: #2196F3;
        font-size: 0.9em;
    }
    /* Compact chat messages */
    .chat-message {
        padding: 8px;
        margin: 5px 0;
        border-radius: 6px;
        font-size: 0.9em;
    }
    .user-message {
        background-color: #E3F2FD;
        margin-left: 15px;
    }
    .assistant-message {
        background-color: #F5F5F5;
        margin-right: 15px;
    }
    .stButton button {
        width: 100%;
    }
    /* Reduce metric padding */
    div[data-testid="stMetric"] {
        padding: 0 !important;
    }
    /* Reduce caption spacing */
    .stCaption {
        margin-bottom: 0.2rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'search_type' not in st.session_state:
    st.session_state.search_type = None
if 'search_value' not in st.session_state:
    st.session_state.search_value = None
if 'selected_log' not in st.session_state:
    st.session_state.selected_log = None
if 'show_log_popup' not in st.session_state:
    st.session_state.show_log_popup = False


# Skip auto-loading - AI will fetch files on-demand when needed
if 'code_loaded' not in st.session_state:
    st.session_state.code_loaded = False

# Ultra-compact header - single row
col1, col2, col3, col4, col5 = st.columns([2, 1.5, 1, 1, 1])
with col1:
    st.markdown("### 🔍 EOC Log Analyzer")
with col2:
    kb_stats = knowledge_server.get_stats()
    st.caption(f"📚 {kb_stats['total_sections']} KB sections" if kb_stats['total_sections'] > 0 else "📚 No KB")
with col3:
    # Show vector DB status with backend info
    if config.app.enable_vector_search:
        backend = config.app.vector_backend
        if backend == "chroma":
            try:
                chroma = get_chroma_manager()
                stats = chroma.get_collection_stats()
                doc_count = stats.get('total_documents', 0)
                st.caption(f"🔍 ChromaDB: {doc_count} docs")
            except:
                st.caption("🔍 ChromaDB ⚠️")
        else:
            st.caption(f"🔍 Databricks ✅")
    else:
        st.caption("🔍 Vector ⚠️")
with col4:
    if config.has_gitlab():
        st.caption("💻 GitLab ✅")
    else:
        st.caption("💻 GitLab ⚠️")
with col5:
    st.caption(f"v{config.app.app_version}")

# Sidebar for vector embeddings management
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    st.markdown("---")
    st.markdown("### 🔍 Vector Search")
    
    # Show current backend and status
    st.caption(f"**Backend:** {config.app.vector_backend.upper()}")
    st.caption(f"**Enabled:** {'✅' if config.app.enable_vector_search else '⚠️ Disabled'}")
    
    if config.app.vector_backend == "chroma":
        try:
            chroma = get_chroma_manager()
            stats = chroma.get_collection_stats()
            st.caption(f"**Documents:** {stats.get('total_documents', 0)}")
            st.caption(f"**Status:** {stats.get('status', 'unknown')}")
        except Exception as e:
            st.caption(f"**Status:** Error - {str(e)[:50]}")
    
    st.markdown("---")
    
    # Embedding generation
    st.markdown("### 📦 Generate Embeddings")
    
    if config.app.vector_backend == "chroma":
        st.caption("Generate vector embeddings from knowledge base files and store in ChromaDB.")
        
        # Warning about time
        st.warning("⚠️ This process can take several minutes. The app will be unresponsive during generation.")
        
        if st.button("🚀 Generate Embeddings", use_container_width=True, type="primary"):
            with st.spinner("🔄 Generating embeddings... Please wait..."):
                try:
                    # Run the embedding generation script
                    script_path = os.path.join(os.path.dirname(__file__), "generate_embeddings.py")
                    
                    # Run in subprocess with auto-confirm
                    result = subprocess.run(
                        [sys.executable, script_path],
                        input="yes\nyes\n",  # Auto-confirm prompts
                        capture_output=True,
                        text=True,
                        timeout=600  # 10 minute timeout
                    )
                    
                    if result.returncode == 0:
                        st.success("✅ Embeddings generated successfully!")
                        # Show output
                        if result.stdout:
                            with st.expander("📋 Generation Log"):
                                st.code(result.stdout)
                        st.rerun()
                    else:
                        st.error(f"❌ Generation failed: {result.stderr}")
                
                except subprocess.TimeoutExpired:
                    st.error("❌ Generation timed out (>10 minutes)")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    else:
        st.info("📍 Using Databricks Vector Search. Embeddings are managed in the `eoc-vector-embeddings` project.")
    
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.caption("• Regenerate embeddings after updating knowledge base files")
    st.caption("• Enable vector search in `.env` file")
    st.caption("• Switch backends via `VECTOR_BACKEND` config")

# New search form with dropdown + single text input
with st.form("search_form"):
    col1, col2, col3 = st.columns([2, 3, 1])
    
    with col1:
        search_type = st.selectbox(
            "Search Type",
            options=[
                "order_number_dpi",
                "phone_number",
                "order_number_om",
                "quote_id",
                "quote_uuid"
            ],
            format_func=lambda x: {
                "order_number_dpi": "Order Number (DPI)",
                "phone_number": "Phone Number",
                "order_number_om": "Order Number (OM)",
                "quote_id": "Quote ID",
                "quote_uuid": "Quote UUID"
            }[x],
            index=0,  # Default to Order Number (DPI)
            label_visibility="collapsed"
        )
    
    with col2:
        search_value = st.text_input(
            "Search Value",
            placeholder=f"Enter {search_type.replace('_', ' ')}...",
            label_visibility="collapsed",
            help="Enter the identifier to search for"
        )
    
    with col3:
        submit = st.form_submit_button("🔍 Analyze", use_container_width=True, type="primary")
    
    col_clear = st.columns([1])[0]
    with col_clear:
        clear = st.form_submit_button("🗑️ Clear", use_container_width=True, help="Clear all results")
    
    if submit:
        if not search_value:
            st.error("Please enter a search value")
        else:
            with st.spinner("🔄 Analyzing order... This may take 5-10 seconds"):
                # Call Coordinator Agent with new signature
                result = coordinator.analyze_order(
                    search_type=search_type,
                    search_value=search_value,
                    goal="Analyze order execution and identify any issues"
                )
                
                st.session_state.analysis_result = result
                st.session_state.search_type = search_type
                st.session_state.search_value = search_value
                
                if result.get('success'):
                    st.success(f"✅ Analysis complete! Found {result.get('total_orders', 0)} order(s)")
                else:
                    st.error(f"❌ {result.get('error', 'Analysis failed')}")
                
                st.rerun()
    
    if clear:
        st.session_state.analysis_result = None
        st.session_state.search_type = None
        st.session_state.search_value = None
        st.rerun()

# Main content area - split view (Message Logs LEFT + AI Analysis RIGHT)
if st.session_state.get('analysis_result'):
    result = st.session_state.analysis_result
    
    if result.get('success'):
        # Split view: 40% logs, 60% analysis
        col_logs, col_analysis = st.columns([4, 6])
        
        # ================================================================
        # LEFT COLUMN: MESSAGE LOGS TABLE
        # ================================================================
        with col_logs:
            st.markdown("### 📊 Message Logs")
            
            # Get message logs from memory
            memory = result.get('memory', {})
            total_orders = result.get('total_orders', 0)
            
            # Collect all message logs from all orders
            all_message_logs = []
            for order_idx in range(total_orders):
                order_memory = memory.get(f"order_{order_idx}", {})
                step_4_data = order_memory.get("step_4", {})
                message_logs = step_4_data.get("result", [])
                all_message_logs.extend(message_logs)
            
            if all_message_logs:
                st.caption(f"Total: {len(all_message_logs)} logs")
                
                # Display as table
                for idx, log in enumerate(all_message_logs):
                    with st.container():
                        col_time, col_op, col_btn = st.columns([2, 4, 1])
                        
                        with col_time:
                            timestamp = log.get('creation_time', 'N/A')
                            if isinstance(timestamp, str):
                                # Show only time if today
                                timestamp = timestamp.split('T')[-1][:8] if 'T' in timestamp else timestamp
                            st.caption(timestamp)
                        
                        with col_op:
                            operation = log.get('operation', 'Unknown')
                            # Shorten long operations
                            if len(operation) > 40:
                                operation = operation[:37] + "..."
                            st.text(operation)
                        
                        with col_btn:
                            if st.button("👁️", key=f"view_log_{idx}", help="View request/response"):
                                st.session_state.selected_log = log
                                st.session_state.show_log_popup = True
                                st.rerun()
            else:
                st.info("No message logs found")
        
        # ================================================================
        # RIGHT COLUMN: AI ANALYSIS
        # ================================================================
        with col_analysis:
            st.markdown("### 🤖 AI Analysis")
            
            # Show analysis for each order
            for order_idx in range(total_orders):
                order_memory = memory.get(f"order_{order_idx}", {})
                order_info = order_memory.get("order_info", {})
                
                if total_orders > 1:
                    st.markdown(f"#### Order {order_idx + 1} of {total_orders}")
                    st.caption(f"Order ID: {order_info.get('cworderid', 'N/A')} | DPI: {order_info.get('dpiordernumber', 'N/A')}")
                
                # Get analysis from step 8 (formatted response)
                step_8_data = order_memory.get("step_8", {})
                analysis = step_8_data.get("result", "No analysis available")
                
                st.markdown(analysis)
                
                if total_orders > 1 and order_idx < total_orders - 1:
                    st.markdown("---")
    
    else:
        # Show error
        st.error(f"❌ {result.get('error', 'Analysis failed')}")
        st.caption(f"Stopped at: {result.get('stopped_at_step', 'Unknown')}")

# ================================================================
# POPUP: Request/Response Viewer
# ================================================================
if st.session_state.get('show_log_popup', False):
    selected_log = st.session_state.get('selected_log', {})
    
    with st.container():
        st.markdown("---")
        st.markdown(f"### 📨 Message Details")
        st.caption(f"**MSGID:** {selected_log.get('msgid', 'N/A')} | **Operation:** {selected_log.get('operation', 'N/A')}")
        st.caption(f"**Time:** {selected_log.get('creation_time', 'N/A')}")
        
        # Split: Request LEFT, Response RIGHT
        col_request, col_response = st.columns(2)
        
        with col_request:
            st.markdown("#### 📤 REQUEST (SEND_DATA)")
            
            send_data = selected_log.get('send_data', '')
            if send_data:
                # Try to format as JSON/XML
                try:
                    # Try JSON first
                    parsed = json.loads(send_data)
                    formatted = json.dumps(parsed, indent=2)
                    st.code(formatted, language="json")
                except:
                    try:
                        # Try XML formatting
                        import xml.dom.minidom
                        dom = xml.dom.minidom.parseString(send_data)
                        formatted = dom.toprettyxml()
                        st.code(formatted, language="xml")
                    except:
                        # Show raw
                        st.code(send_data, language="text")
            else:
                st.info("No request data")
        
        with col_response:
            st.markdown("#### 📥 RESPONSE (RECEIVE_DATA)")
            
            receive_data = selected_log.get('receive_data', '')
            if receive_data:
                # Try to format as JSON/XML
                try:
                    # Try JSON first
                    parsed = json.loads(receive_data)
                    formatted = json.dumps(parsed, indent=2)
                    st.code(formatted, language="json")
                except:
                    try:
                        # Try XML formatting
                        import xml.dom.minidom
                        dom = xml.dom.minidom.parseString(receive_data)
                        formatted = dom.toprettyxml()
                        st.code(formatted, language="xml")
                    except:
                        # Show raw
                        st.code(receive_data, language="text")
            else:
                st.info("No response data")
        
        # Close button
        if st.button("❌ Close", use_container_width=True):
            st.session_state.show_log_popup = False
            st.rerun()
        
        st.markdown("---")

elif not st.session_state.get('analysis_result'):
    # Empty state
    st.info("👆 Enter search criteria and click Analyze to start")

