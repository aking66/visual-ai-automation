# -*- coding: utf-8 -*-
"""
Helper utilities for the Visual AI Automation Workflow Builder
"""

import streamlit as st
import traceback
from typing import Callable

def load_workflow(workflow_func: Callable):
    """
    Load a workflow template into the session state
    
    Args:
        workflow_func (Callable): Function that returns a workflow configuration
    """
    try:
        # Load the nodes from the workflow function
        st.session_state.nodes = workflow_func()
        
        # Reset any existing compiled graph
        st.session_state.compiled_graph = None
        
        # Select the first node by default
        st.session_state.selected_node_id = st.session_state.nodes[0]['id'] if st.session_state.nodes else None
        
        # Clear any execution logs and state
        st.session_state.execution_log = []
        st.session_state.final_state = None
        st.session_state.recursion_limit = None
        
        # Generate a display name for the workflow by transforming the function name
        wf_name = workflow_func.__name__.replace('get_', '').replace('_workflow', '').replace('_', ' ').title()
        
        # Notify the user
        st.toast(f"{wf_name} loaded!", icon="📄")
        
        # Refresh the UI
        st.rerun()
        
    except Exception as e:
        st.error(f"Load Error: {e}")
        print(f"Load Error: {e}")
        traceback.print_exc()

def initialize_session_state():
    """
    Initialize the session state with default values
    """
    default_values = {
        "compiled_graph": None,
        "execution_log": [],
        "final_state": None,
        "selected_node_id": None,
        "recursion_limit": None,
        "google_api_key_provided": False
    }
    
    # Set defaults if values don't exist
    for key, value in default_values.items():
        st.session_state.setdefault(key, value)
    
    # Load default workflow if nodes don't exist
    if "nodes" not in st.session_state or not st.session_state.nodes:
        try:
            from src.workflows.example_workflows import get_enhanced_hedge_fund_workflow
            
            print("Loading default workflow")
            st.session_state.nodes = get_enhanced_hedge_fund_workflow()
            
            if st.session_state.nodes and isinstance(st.session_state.nodes, list):
                st.session_state.selected_node_id = st.session_state.nodes[0].get('id')
        except Exception as e:
            print(f"Default load error: {e}")
            st.session_state.nodes = []