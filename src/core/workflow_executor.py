# -*- coding: utf-8 -*-
"""
Workflow execution logic for the Visual AI Automation Workflow Builder

This module provides the functionality to execute compiled workflow graphs.
It handles the initializing of workflow state, executing the workflow,
managing errors, and extracting the final output.
"""

import re
import traceback
import streamlit as st

from src.models.state import WorkflowState
from src.config.constants import ROUTING_KEY_MARKER

def execute_workflow(initial_message: str) -> bool:
    """
    Execute the compiled workflow with the provided initial message
    
    This function:
    1. Resets any previous execution state
    2. Initializes the workflow with the given message
    3. Executes the workflow graph
    4. Handles and reports any errors during execution
    5. Updates the UI with execution status
    
    Args:
        initial_message (str): The initial input message for the workflow
        
    Returns:
        bool: True if execution was successful, False otherwise
    """
    # Reset execution state
    st.session_state.execution_log = ["**🚀 Starting Workflow...**"]
    st.session_state.final_state = None
    
    # Initialize workflow state
    initial_state = WorkflowState(
        input=initial_message,
        node_outputs={},
        last_response_content="",
        current_node_id=""
    )
    
    st.session_state.execution_log.append(
        f"📥 Input: {initial_message[:150]}{'...' if len(initial_message)>150 else ''}"
    )
    
    log_placeholder = st.empty()
    log_placeholder.info("⏳ Running workflow...")
    
    with st.spinner("Executing workflow..."):
        try:
            # Get the recursion limit
            rec_limit = st.session_state.get('recursion_limit', 25)
            print(f"Invoking graph with limit: {rec_limit}")
            
            # Execute the workflow graph
            final_state_result = st.session_state.compiled_graph.invoke(
                initial_state, 
                config={"recursion_limit": rec_limit}
            )
            
            st.session_state.final_state = final_state_result
            st.session_state.execution_log.append("**🏁 Workflow Finished**")
            st.toast("Finished!", icon="🏁")
            log_placeholder.empty()
            return True
            
        except Exception as e:
            err_msg = f"{e}"
            
            if "must be followed by tool messages" in str(e):
                err_msg = f"LLM generated 'tool_calls' which graph cannot handle. Error: {e}."
                st.error(f"{err_msg}", icon="🔥")
            elif isinstance(e, RecursionError) or "recursion limit" in str(e).lower():
                err_msg = f"Recursion limit ({rec_limit}) reached. Error: {e}"
                st.error(f"{err_msg}", icon="🔥")
            else:
                st.error(f"Exec failed: {err_msg}", icon="🔥")
                
            st.session_state.execution_log.append(f"**💥 WORKFLOW ERROR:** {err_msg}")
            print(f"Exec Error: {e}")
            traceback.print_exc()
            st.toast("Failed!", icon="❌")
            log_placeholder.empty()
            return False

def get_final_message_content():
    """
    Extract the final message content from the workflow execution state,
    removing any routing markers
    
    This function parses the final response content and removes any routing
    key markers to present a clean output to the user.
    
    Returns:
        str or None: The final message content if available, otherwise None
    """
    final_message_content = None
    
    if st.session_state.final_state and isinstance(st.session_state.final_state, dict):
        final_content_raw = st.session_state.final_state.get('last_response_content', '')
        
        if final_content_raw and isinstance(final_content_raw, str):
            final_message_content = re.sub(
                rf"\s*{ROUTING_KEY_MARKER}\s*\w+\s*$", 
                "", 
                final_content_raw
            ).strip()
    
    return final_message_content