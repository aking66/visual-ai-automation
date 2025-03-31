# -*- coding: utf-8 -*-
"""
Router module for the Visual AI Automation Workflow Builder

This module handles the routing logic between nodes in the workflow.
It determines which node should be executed next based on the current state
and routing rules defined in the workflow.
"""

import streamlit as st
from src.models.state import WorkflowState
from src.core.graph_compiler import get_node_display_name

def route_next_node(state: WorkflowState) -> WorkflowState:
    """
    Determine the next node to execute in the workflow
    
    This function is used as the router node in the LangGraph workflow.
    It inspects the current state (specifically the current_node_id),
    logs the routing decision, and returns the state unchanged so that
    LangGraph can route execution to the appropriate node.
    
    Args:
        state (WorkflowState): The current workflow state
        
    Returns:
        WorkflowState: The unchanged workflow state (routing is handled by LangGraph)
    """
    # The current_node_id is set by the previous node processor and contains
    # either a specific routing key or the default routing key
    next_node_id = state.current_node_id
    
    # Get a human-readable name for the next node
    next_node_name = get_node_display_name(next_node_id)
    
    # Log the routing decision
    if next_node_id == "END":
        st.session_state.execution_log.append("⏹️ **Routing to: End**")
    else:
        st.session_state.execution_log.append(f"➡️ **Routing to: {next_node_name}** (`{next_node_id}`)")
    
    # Return state unchanged - LangGraph uses current_node_id for routing
    return state