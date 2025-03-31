# -*- coding: utf-8 -*-
"""
Routing logic for the Visual AI Automation Workflow Builder
"""

import re
import streamlit as st
from src.models.state import WorkflowState
from src.config.constants import ROUTING_KEY_MARKER, DEFAULT_ROUTING_KEY

def generic_router(state: WorkflowState) -> str:
    """
    Determines the next route based on the routing key in state['last_response_content']
    
    Args:
        state (WorkflowState): The current workflow state
        
    Returns:
        str: The routing key to determine the next node
    """
    print("\n--- Routing Check ---")
    routing_key = DEFAULT_ROUTING_KEY  # Default if no key found
    last_content = state.get("last_response_content", "")

    if last_content:
        # Ensure last_content is treated as a string
        if isinstance(last_content, str):
             match = re.search(rf"{ROUTING_KEY_MARKER}\s*(\w+)\s*$", last_content)
             if match:
                 # Key found, use it
                 routing_key = match.group(1).strip()
                 print(f"  Extracted key: '{routing_key}'")
             else:
                 # String content, but no key found at the end
                 print(f"  No routing key found in last response: '...{last_content[-50:]}'")
                 print(f"  -> Using default routing ('{DEFAULT_ROUTING_KEY}').")
        else:
             # Content is not a string
             print(f"  Last response content type is {type(last_content)}, not string.")
             print(f"  -> Using default routing ('{DEFAULT_ROUTING_KEY}').")
    else:
        # No previous response content found in state
        print(f"  No previous response content found.")
        print(f"  -> Using default routing ('{DEFAULT_ROUTING_KEY}').")

    # Log and return the determined routing key
    log_decision_msg = f"🚦 Routing decision: '{routing_key}'"
    print(f"  -> {log_decision_msg}")
    if "execution_log" not in st.session_state: 
        st.session_state.execution_log = []
    st.session_state.execution_log.append(log_decision_msg)
    return routing_key