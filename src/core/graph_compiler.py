# -*- coding: utf-8 -*-
"""
Graph compiler module for the Visual AI Automation Workflow Builder

This module is responsible for compiling the workflow nodes defined by the user 
into a LangGraph execution graph that can be executed with conditional routing.
"""

import uuid
import streamlit as st
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional, Union, Callable
from langchain_core.language_models.base import BaseLanguageModel

from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage

from langgraph.graph import StateGraph, END

from src.models.state import WorkflowState
from src.core.node_processor import process_node
from src.core.router import route_next_node
from src.config.constants import DEFAULT_ROUTING_KEY, ROUTING_KEY_MARKER

def compile_graph() -> bool:
    """
    Compile the user-defined workflow nodes into a LangGraph execution graph
    
    This function:
    1. Validates that the nodes are properly configured
    2. Builds a LangGraph StateGraph with the defined nodes
    3. Configures routing between nodes based on rules
    4. Sets the compiled graph in session state for execution
    
    Returns:
        bool: True if compilation was successful, False otherwise
    """
    from src.core.llm import get_llm_instances
    
    if not st.session_state.nodes:
        st.warning("No nodes to compile.")
        return False
    
    try:
        nodes = st.session_state.nodes
        
        # Get a valid processor LLM
        processor_llm = get_llm_instances().get('processor_llm')
        if not processor_llm:
            st.error("Failed to initialize processor LLM.", icon="🔥")
            return False
            
        # Initialize the workflow state graph
        workflow = StateGraph(WorkflowState)
        
        st.session_state.execution_log = []
        now = datetime.now()
        
        # Add processing nodes to the graph
        for node in nodes:
            if isinstance(node, dict) and 'id' in node and 'name' in node:
                node_id = node['id']
                
                # Create node function with processor_llm
                node_fn = lambda state, node_data=node, llm=processor_llm: process_node(
                    state, node_data, llm
                )
                
                # Add node to graph
                workflow.add_node(node_id, node_fn)
        
        # Add router to determine the next node
        workflow.add_node("router", route_next_node)
        
        # Add edges between nodes
        for node in nodes:
            if isinstance(node, dict) and 'id' in node:
                # Connect node to router
                workflow.add_edge(node['id'], "router")
                
                # Get routing rules
                routing_rules = node.get('routing_rules', {})
                
                if not isinstance(routing_rules, dict):
                    routing_rules = {}
                    
                # Process conditional targets
                conditional_targets = routing_rules.get('conditional_targets', [])
                
                if not isinstance(conditional_targets, list):
                    conditional_targets = []
                
                # Connect router to all possible next nodes based on conditions
                for rule in conditional_targets:
                    if isinstance(rule, dict):
                        output_key = rule.get('output_key', '').strip()
                        target_node_id = rule.get('target_node_id')
                        
                        if output_key and target_node_id:
                            # Add conditional edge from router to target node
                            workflow.add_conditional_edges(
                                "router",
                                lambda state, key=output_key, graph=workflow: state.current_node_id == key,
                                {key: target_node_id for key in [output_key]}
                            )
                            
                # Add default route
                default_target = routing_rules.get('default_target', "END")
                
                if default_target == "END":
                    workflow.add_edge("router", END)
                else:
                    # Create default conditional edge
                    workflow.add_conditional_edges(
                        "router",
                        lambda state, node_id=node['id']: state.current_node_id == DEFAULT_ROUTING_KEY,
                        {DEFAULT_ROUTING_KEY: default_target}
                    )
        
        # Set the entry point as the first node
        if nodes and isinstance(nodes[0], dict):
            entrypoint_id = nodes[0].get('id')
            workflow.set_entry_point(entrypoint_id)
        
        # Compile the workflow
        compiled_graph = workflow.compile()
        
        # Store the compiled graph in session state
        st.session_state.compiled_graph = compiled_graph
        st.session_state.compile_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        
        st.success("Workflow compiled successfully!", icon="✅")
        return True
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        st.error(f"Compile failed: {e}", icon="🔥")
        return False

def get_node_display_name(node_id: str) -> str:
    """
    Get a human-readable display name for a node
    
    Args:
        node_id (str): The ID of the node
        
    Returns:
        str: The display name for the node, or "End" for the end node,
             or the node ID if no name is defined
    """
    if node_id == "END":
        return "End"
    
    for node in st.session_state.nodes:
        if isinstance(node, dict) and node.get('id') == node_id:
            return node.get('name', node_id)
    
    return node_id