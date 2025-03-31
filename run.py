# -*- coding: utf-8 -*-
"""
N8N-Inspired AI Automation Workflow Builder using Streamlit and LangGraph
"""
# Subscribe to the Deep Charts YouTube Channel (https://www.youtube.com/@DeepCharts)

import streamlit as st
# Set page config must be the first Streamlit command
st.set_page_config(layout="wide", page_title="Visual AI Automation Builder ", page_icon="🤖")

import os
import re
import uuid
import sys
import traceback
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='automation_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('automation')

# Log startup information
logger.info("="*50)
logger.info("Starting Visual AI Automation Workflow Builder")
logger.info(f"Python version: {sys.version}")
logger.info(f"OS: {os.name}")
logger.info(f"Current Directory: {os.getcwd()}")
logger.info("Environment Variables:")
for key, value in os.environ.items():
    if key.startswith('GOOGLE') or key.startswith('ANTHROPIC') or key.startswith('COHERE'):
        # Mask API keys in logs
        logger.info(f"  {key}: {'*'*10}")
    else:
        logger.info(f"  {key}: {value}")
logger.info("="*50)

# Import modules from the project structure
try:
    logger.info("Importing project modules...")
    from src.config.constants import WEB_SEARCH_TOOL_DICT, ROUTING_KEY_MARKER, DEFAULT_ROUTING_KEY, END_NODE_ID
    from src.models.state import WorkflowState
    from src.core.llm import initialize_llm, get_llm_instances
    from src.core.graph_compiler import compile_graph, get_node_display_name
    from src.core.workflow_executor import execute_workflow, get_final_message_content
    from src.ui.graph_visualization import generate_agraph_data, get_graph_config
    from src.ui.node_management import (
        select_node, get_node_options_for_select, update_node_data_ui, delete_node_ui,
        move_node_ui, add_conditional_rule_ui, delete_conditional_rule_ui, add_new_node
    )
    from src.workflows.example_workflows import (
        get_simple_summarizer_workflow, get_sentiment_workflow, get_classification_workflow,
        get_deep_research_workflow, get_enhanced_hedge_fund_workflow
    )
    from src.utils.workflow_helpers import load_workflow, initialize_session_state
    logger.info("All modules imported successfully")
except ImportError as e:
    logger.error(f"Error importing modules: {e}")
    logger.error(traceback.format_exc())
    st.error(f"Error importing required modules: {e}")

# --- Check Required Packages ---
try:
    from streamlit_agraph import agraph
    AGRAPH_AVAILABLE = True
    logger.info("streamlit-agraph is available")
except ImportError:
    error_msg = "`streamlit-agraph` not found. Install: `pip install streamlit-agraph`"
    logger.error(error_msg)
    st.warning(error_msg)
    AGRAPH_AVAILABLE = False
    def agraph(*args, **kwargs): 
        logger.warning("Attempted to use agraph but it's not available")
        pass

# --- Initialize Session State ---
initialize_session_state()

# --- Streamlit App UI ---
st.title("🤖🧠 Visual AI Automation Builder")
now = datetime.now()
current_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
st.caption(f"Uses Dictionary State. LLM: `gemini-1.5-pro` (bound: `{WEB_SEARCH_TOOL_DICT}`). Refresh: {current_timestamp}")

# --- Sidebar UI ---
with st.sidebar:
    st.header("🔑 Google API Key")
    google_api_key_input = st.text_input(
        "API Key", 
        type="password", 
        value=os.environ.get("GOOGLE_API_KEY", ""), 
        help="Needed for LLM nodes.",
        key="api_key_input_sidebar"
    )
    
    api_key_in_env = os.environ.get("GOOGLE_API_KEY")
    api_key_changed = (google_api_key_input != api_key_in_env if api_key_in_env else bool(google_api_key_input))
    
    if api_key_changed:
        if google_api_key_input:
            os.environ["GOOGLE_API_KEY"] = google_api_key_input
        elif "GOOGLE_API_KEY" in os.environ:
            del os.environ["GOOGLE_API_KEY"]
            
        llm_ready = initialize_llm()
        st.session_state.google_api_key_provided = bool(google_api_key_input)
        
        if api_key_changed:
            st.session_state.compiled_graph = None
            st.rerun()
    else:
        llm_ready = initialize_llm()
        st.session_state.google_api_key_provided = bool(os.environ.get("GOOGLE_API_KEY"))
    
    if llm_ready:
        st.success("LLM Initialized.", icon="✅")
    elif st.session_state.get("google_api_key_provided"):
        st.error("LLM Init Failed.", icon="🔥")
    else:
        st.warning("LLM needs API Key.", icon="⚠️")
    
    st.caption(f"Tool binding: `{WEB_SEARCH_TOOL_DICT}`")
    st.divider()
    
    # --- Node Palette ---
    st.header("🧩 Node Palette")
    with st.form("add_node_form"):
        new_node_name_input = st.text_input(
            "New Node Name", 
            placeholder="e.g., 'Summarize Input'", 
            key="new_node_name_palette_main"
        )
        add_node_submitted = st.form_submit_button("➕ Add LLM Node", use_container_width=True)
        
        if add_node_submitted:
            add_new_node(new_node_name_input)
    
    # --- Example Workflows ---
    st.divider()
    st.header("📜 Example Workflows")
    ex_cols = st.columns(2)
    
    with ex_cols[0]:
        st.button(
            "📄 Summarizer", 
            use_container_width=True, 
            key="load_summarizer_btn", 
            on_click=load_workflow, 
            args=(get_simple_summarizer_workflow,)
        )
        
        st.button(
            "🎭 Sentiment", 
            use_container_width=True, 
            key="load_sentiment_btn", 
            on_click=load_workflow, 
            args=(get_sentiment_workflow,)
        )
        
        st.button(
            "🔬 Deep Research", 
            use_container_width=True, 
            key="load_deep_research_btn", 
            on_click=load_workflow, 
            args=(get_deep_research_workflow,)
        )
    
    with ex_cols[1]:
        st.button(
            "🏷️ Classify", 
            use_container_width=True, 
            key="load_classify_btn", 
            on_click=load_workflow, 
            args=(get_classification_workflow,)
        )
        
        st.button(
            "📈 Adv. Hedge Fund", 
            use_container_width=True, 
            key="load_adv_hedge_btn", 
            on_click=load_workflow, 
            args=(get_enhanced_hedge_fund_workflow,)
        )
    
    # --- Workflow Control ---
    st.divider()
    st.header("⚙️ Workflow Control")
    
    compile_disabled = not llm_ready or not st.session_state.nodes
    tooltip_compile = "Requires API Key & nodes." if compile_disabled else "Compile workflow."
    
    if st.button(
        "🔄 Compile Workflow", 
        type="primary", 
        use_container_width=True, 
        disabled=compile_disabled, 
        help=tooltip_compile, 
        key="compile_workflow_btn"
    ):
        if compile_graph():
            st.rerun()
    
    tooltip_reset = "Clear all nodes and reset."
    st.button(
        "🗑️ Reset Workflow", 
        use_container_width=True, 
        help=tooltip_reset, 
        key="reset_workflow_btn", 
        on_click=lambda: setattr(st.session_state, 'nodes', []) or st.rerun()
    )

# --- Main Content Area ---
top_cols = st.columns([0.6, 0.4])

# --- Graph Visualization ---
with top_cols[0]:
    st.subheader("📊 Workflow Graph")
    
    if not st.session_state.nodes:
        st.info("Add nodes or load an example.")
    elif not AGRAPH_AVAILABLE:
        st.warning("Install `streamlit-agraph` for visualization.")
    else:
        try:
            agraph_nodes, agraph_edges = generate_agraph_data(st.session_state.nodes)
            agraph_config = get_graph_config()
            
            clicked_node_id = agraph(
                nodes=agraph_nodes,
                edges=agraph_edges,
                config=agraph_config
            )
            
            valid_node_ids = {n['id'] for n in st.session_state.nodes if isinstance(n, dict)}
            if clicked_node_id and clicked_node_id in valid_node_ids and clicked_node_id != st.session_state.selected_node_id:
                select_node(clicked_node_id)
                st.rerun()
                
        except Exception as e:
            st.error(f"Graph Error: {e}", icon="🔥")
            print(f"Graph Error: {e}")
            import traceback
            traceback.print_exc()

# --- Node Configuration ---
with top_cols[1]:
    st.subheader("⚙️ Node Configuration")
    
    valid_node_ids = [n.get('id') for n in st.session_state.nodes if isinstance(n, dict)]
    
    if not st.session_state.selected_node_id or st.session_state.selected_node_id not in valid_node_ids:
        st.session_state.selected_node_id = valid_node_ids[0] if valid_node_ids else None
    
    if not st.session_state.nodes:
        st.info("Add nodes or load example.")
    else:
        node_options_display = get_node_options_for_select(include_end=False)
        node_ids_only = [opt[0] for opt in node_options_display]
        current_selection_index = 0
        
        try:
            current_selection_index = node_ids_only.index(st.session_state.selected_node_id) if st.session_state.selected_node_id in node_ids_only else 0
        except:
            pass
            
        if not node_ids_only:
            current_selection_index = 0
            
        selected_id_from_dropdown = st.selectbox(
            "Select Node:",
            options=node_options_display,
            index=current_selection_index,
            format_func=lambda x: x[1],
            key="node_selector_config",
            label_visibility="collapsed"
        )
        
        if selected_id_from_dropdown and selected_id_from_dropdown[0] != st.session_state.selected_node_id:
            select_node(selected_id_from_dropdown[0])
            st.rerun()
            
        st.divider()
    
    # --- Node Configuration UI ---
    selected_node_data = next(
        (n for n in st.session_state.nodes if isinstance(n, dict) and n.get("id") == st.session_state.selected_node_id),
        None
    )
    
    if selected_node_data:
        node_id = selected_node_data["id"]
        node_name = selected_node_data.get("name", "")
        node_prompt = selected_node_data.get("prompt", "")
        routing_rules = selected_node_data.get("routing_rules", {})
        default_target = routing_rules.get("default_target", END_NODE_ID)
        conditional_targets = routing_rules.get("conditional_targets", [])
        
        if not isinstance(routing_rules, dict):
            routing_rules = {"default_target": END_NODE_ID, "conditional_targets": []}
            
        if not isinstance(conditional_targets, list):
            conditional_targets = []
            
        with st.container(border=True):
            form_key = f"config_form_{node_id}"
            
            with st.form(key=form_key):
                st.markdown(f"**Editing: {node_name}** (`{node_id}`)")
                edited_name = st.text_input("Node Name", value=node_name, key=f"cfg_name_{node_id}")
                edited_prompt = st.text_area(
                    "LLM Prompt", 
                    value=node_prompt, 
                    height=150, 
                    key=f"cfg_prompt_{node_id}", 
                    help=f"Define task. Use '{{input_text}}' if needed. End response with '{ROUTING_KEY_MARKER} <key>'."
                )
                
                st.markdown("**🚦 Routing Rules**")
                node_options = get_node_options_for_select(include_end=True, exclude_node_id=node_id)
                current_default_idx = 0
                
                try:
                    current_default_idx = [i for i, (opt_id, _) in enumerate(node_options) if opt_id == default_target][0]
                except:
                    current_default_idx = next((i for i, (opt_id, _) in enumerate(node_options) if opt_id == END_NODE_ID), 0)
                
                selected_default_option = st.selectbox(
                    "Default Target", 
                    options=node_options, 
                    index=current_default_idx, 
                    format_func=lambda x: x[1], 
                    key=f"cfg_default_{node_id}"
                )
                edited_default_target_id = selected_default_option[0] if selected_default_option else END_NODE_ID
                
                st.markdown(f"**Conditional Targets (based on {ROUTING_KEY_MARKER} output):**")
                edited_conditional_targets = []
                current_conditional_targets = list(conditional_targets)
                
                # Create UI for each conditional rule
                for rule_idx, rule in enumerate(current_conditional_targets):
                    st.caption(f"Rule {rule_idx+1}")
                    rule_cols = st.columns([0.5, 0.5])
                    
                    with rule_cols[0]:
                        output_key = st.text_input(
                            f"If Key Is", 
                            value=rule.get("output_key", ""), 
                            placeholder="e.g., success", 
                            key=f"cfg_key_{node_id}_{rule_idx}", 
                            label_visibility="collapsed"
                        )
                        
                    with rule_cols[1]:
                        current_target_idx = 0
                        
                        try:
                            current_target_idx = [i for i, (opt_id, _) in enumerate(node_options) if opt_id == rule.get("target_node_id")][0]
                        except:
                            current_target_idx = next((i for i, (opt_id, _) in enumerate(node_options) if opt_id == END_NODE_ID), 0)
                            
                        selected_target_option = st.selectbox(
                            f"Then Go To", 
                            options=node_options, 
                            index=current_target_idx, 
                            format_func=lambda x: x[1], 
                            key=f"cfg_target_{node_id}_{rule_idx}", 
                            label_visibility="collapsed"
                        )
                        target_node_id = selected_target_option[0] if selected_target_option else END_NODE_ID
                        
                    edited_conditional_targets.append({
                        "output_key": output_key.strip(), 
                        "target_node_id": target_node_id
                    })
                
                st.divider()
                submitted = st.form_submit_button("💾 Save Changes", type="primary", use_container_width=True)
                
                if submitted:
                    final_conditional_targets = [r for r in edited_conditional_targets if r.get("output_key")]
                    new_data = {
                        "name": edited_name.strip(),
                        "prompt": edited_prompt,
                        "routing_rules": {
                            "default_target": edited_default_target_id,
                            "conditional_targets": final_conditional_targets
                        }
                    }
                    
                    if not edited_name.strip():
                        st.warning("Node Name cannot be empty.")
                    elif any(
                        isinstance(n, dict) and n.get('id') != node_id and n.get('name','').strip() == edited_name.strip() 
                        for n in st.session_state.nodes
                    ):
                        st.warning(f"Name exists.")
                    else:
                        update_node_data_ui(node_id, new_data)
                        st.rerun()
                        
            # Node management buttons
            st.markdown("**Manage Rules & Node:**")
            action_cols = st.columns([0.5, 0.5])
            
            with action_cols[0]:
                st.button(
                    "➕ Add Rule", 
                    key=f"add_rule_btn_{node_id}", 
                    on_click=add_conditional_rule_ui, 
                    args=(node_id,), 
                    use_container_width=True
                )
                
                if conditional_targets:
                    rule_opts = [(idx, f"Rule {idx+1}: '{rule.get('output_key', '')[:10]}...'") 
                                 for idx, rule in enumerate(conditional_targets)]
                    rule_opts.insert(0, (-1, "Delete Rule..."))
                    
                    selected_rule_idx_to_del = st.selectbox(
                        "Delete Rule", 
                        options=rule_opts, 
                        format_func=lambda x: x[1], 
                        label_visibility="collapsed", 
                        index=0, 
                        key=f"del_rule_sel_{node_id}"
                    )
                    
                    if 'selected_rule_idx_to_del' in locals() and selected_rule_idx_to_del and selected_rule_idx_to_del[0] != -1:
                        rule_idx_del = selected_rule_idx_to_del[0]
                        st.button(
                            f"🗑️ Confirm Del Rule {rule_idx_del+1}", 
                            key=f"del_rule_btn_{node_id}_{rule_idx_del}", 
                            on_click=delete_conditional_rule_ui, 
                            args=(node_id, rule_idx_del), 
                            use_container_width=True, 
                            type="secondary"
                        )
            
            with action_cols[1]:
                current_node_index = next((i for i, n in enumerate(st.session_state.nodes) 
                                           if isinstance(n, dict) and n.get("id") == node_id), -1)
                
                st.button(
                    "⬆️ Up", 
                    key=f"mv_up_{node_id}", 
                    on_click=move_node_ui, 
                    args=(node_id, -1), 
                    disabled=(current_node_index <= 0), 
                    use_container_width=True
                )
                
                st.button(
                    "⬇️ Down", 
                    key=f"mv_dn_{node_id}", 
                    on_click=move_node_ui, 
                    args=(node_id, 1), 
                    disabled=(current_node_index < 0 or current_node_index >= len(st.session_state.nodes) - 1), 
                    use_container_width=True
                )
                
                st.button(
                    "❌ Delete Node", 
                    key=f"del_nd_{node_id}", 
                    on_click=delete_node_ui, 
                    args=(node_id,), 
                    use_container_width=True, 
                    type="secondary", 
                    help="Delete this node."
                )
    elif st.session_state.nodes:
        st.info("Select node.")
    
    # Handle edge cases with node selection
    if (st.session_state.selected_node_id and st.session_state.nodes and 
        st.session_state.selected_node_id not in [n.get('id') for n in st.session_state.nodes if isinstance(n, dict)]):
        st.session_state.selected_node_id = st.session_state.nodes[0].get('id')
        st.rerun()
    elif not st.session_state.nodes:
        st.session_state.selected_node_id = None

# --- Execution Section ---
st.divider()
st.header("🚀 Execute Workflow")

run_tooltip = ""
run_disabled = True

if st.session_state.compiled_graph and llm_ready:
    st.success("Workflow compiled.", icon="✅")
    run_tooltip = "Run workflow."
    run_disabled = False
elif not llm_ready:
    st.warning("LLM not ready.", icon="⚠️")
    run_tooltip = "LLM needs API Key."
elif st.session_state.nodes:
    st.warning("Compile Workflow first.", icon="⚠️")
    run_tooltip = "Compile first."
else:
    st.info("Workflow empty.")
    run_tooltip = "Workflow empty/not compiled."

initial_message = st.text_area(
    "Enter initial message:",
    height=80,
    key="initial_input_exec",
    value="I want moderate capital appreciation over 5-7 years, willing to accept some market volatility but avoid highly speculative assets. Focus on tech and renewable energy sectors.",
    help="Input for the first node."
)

if not initial_message.strip():
    run_disabled = True
    run_tooltip += " Initial message required."

if st.button("▶️ Run Workflow", disabled=run_disabled, type="primary", help=run_tooltip):
    success = execute_workflow(initial_message)
    st.rerun()

# --- Results Display Section ---
st.subheader("📊 Execution Results")
results_cols = st.columns(2)

with results_cols[0]:
    st.markdown("**Execution Log**")
    
    if st.session_state.execution_log:
        log_text = "\n".join(st.session_state.execution_log)
        st.text_area("Log Details:", value=log_text, height=300, disabled=True, key="log_display_final_main")
    else:
        st.caption("Run workflow to see log.")

with results_cols[1]:
    st.markdown("**Final Output Message**")
    final_message_content = get_final_message_content()
    
    if final_message_content:
        message_container = st.container(height=300, border=False)
        avatar = "🏁"
        
        if any("WORKFLOW ERROR" in log for log in st.session_state.execution_log):
            avatar = "💥"
        elif "ERROR:" in final_message_content:
            avatar = "⚠️"
            
        message_container.chat_message("assistant", avatar=avatar).write(final_message_content)
        
    elif any("WORKFLOW ERROR" in log for log in st.session_state.execution_log):
        st.caption("Ended with error.")
    else:
        st.caption("Run workflow.")

# --- End of App ---