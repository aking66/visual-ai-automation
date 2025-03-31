# -*- coding: utf-8 -*-
"""
Visual AI Automation Workflow Builder - Main Entry Point

This is the main entry point for the Visual AI Automation Workflow Builder application.
It initializes the Streamlit UI and renders the main components of the application.

The application allows users to:
1. Create and configure visual workflows using LLM-powered nodes
2. Define conditional routing between nodes
3. Execute workflows with custom inputs
4. Visualize workflow execution results
"""

import streamlit as st
from src.ui.main_ui import (
    render_sidebar,
    render_graph_section,
    render_node_config_section,
    render_execution_section,
    render_results_section
)

def main():
    """
    Main application entry point
    
    Initializes the Streamlit UI, renders the main components, and
    handles the application flow.
    """
    # Configure page settings
    st.set_page_config(
        page_title="Visual AI Workflow Builder",
        page_icon="🔄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Set application title
    st.title("Visual AI Automation Workflow Builder")
    
    # Initialize session state variables if needed
    if 'nodes' not in st.session_state:
        st.session_state.nodes = []
        
    if 'selected_node_id' not in st.session_state:
        st.session_state.selected_node_id = None
        
    if 'execution_log' not in st.session_state:
        st.session_state.execution_log = []
        
    if 'compiled_graph' not in st.session_state:
        st.session_state.compiled_graph = None
        
    if 'compile_timestamp' not in st.session_state:
        st.session_state.compile_timestamp = None
        
    if 'final_state' not in st.session_state:
        st.session_state.final_state = None
        
    if 'recursion_limit' not in st.session_state:
        st.session_state.recursion_limit = 25
    
    # Render sidebar and get LLM initialization status
    llm_ready = render_sidebar()
    
    # Create main layout using columns
    col1, col2 = st.columns([3, 2])
    
    # Render graph visualization in first column
    with col1:
        render_graph_section()
        
    # Render node configuration in second column
    with col2:
        render_node_config_section()
    
    # Horizontal separator
    st.divider()
    
    # Render execution and results sections
    render_execution_section(llm_ready)
    st.divider()
    render_results_section()

# Run the application when script is executed directly
if __name__ == "__main__":
    main()