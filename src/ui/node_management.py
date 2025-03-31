# -*- coding: utf-8 -*-
"""
Node management UI components for Visual AI Automation Workflow Builder
"""

import uuid
import json
import streamlit as st
from typing import List, Dict, Any, Optional, Tuple

from src.config.constants import END_NODE_ID
from src.core.graph_compiler import get_node_display_name

def select_node(node_id: Optional[str]):
    """Set the selected node ID in session state"""
    st.session_state.selected_node_id = node_id

def get_node_options_for_select(include_end=True, exclude_node_id: Optional[str] = None) -> List[Tuple[str, str]]:
    """
    Get options list for node selection dropdowns
    
    Args:
        include_end (bool): Whether to include the END node in the options
        exclude_node_id (Optional[str]): Node ID to exclude from options (e.g., self)
        
    Returns:
        List[tuple[str, str]]: List of (id, display name) tuples for selection
    """
    options = []
    node_list = st.session_state.get("nodes", [])
    
    if isinstance(node_list, list):
        options.extend([
            (node.get("id"), f"{i+1}. {node.get('name', 'Unnamed')}")
            for i, node in enumerate(node_list) 
            if isinstance(node, dict) and node.get("id") != exclude_node_id
        ])
    
    if include_end and END_NODE_ID != exclude_node_id:
        options.append((END_NODE_ID, get_node_display_name(END_NODE_ID)))
    
    return options

def update_node_data_ui(node_id: str, data: Dict[str, Any]):
    """
    Update a node's data in the session state
    
    Args:
        node_id (str): ID of the node to update
        data (Dict[str, Any]): New data to apply to the node
    """
    updated = False
    node_list = st.session_state.get("nodes", [])
    
    if isinstance(node_list, list):
        for i, node in enumerate(node_list):
            if isinstance(node, dict) and node.get("id") == node_id:
                try:
                    # Safely serialize/deserialize the routing rules to validate them
                    new_rules = json.loads(json.dumps(data.get("routing_rules", {})))
                except Exception:
                    st.error("Serialize Error.")
                    return
                
                # Update node properties
                node["name"] = data.get("name", node.get("name"))
                node["prompt"] = data.get("prompt", node.get("prompt"))
                node["routing_rules"] = new_rules
                updated = True
                break
    
    if updated:
        # Invalidate the compiled graph when nodes are modified
        st.session_state.compiled_graph = None
        st.toast(f"Node '{data.get('name', node_id)}' updated.", icon="💾")
        st.session_state.selected_node_id = node_id
    else:
        st.error(f"Node {node_id} not found.")

def delete_node_ui(node_id_to_delete: str):
    """
    Delete a node from the workflow
    
    Args:
        node_id_to_delete (str): ID of the node to delete
    """
    node_list = st.session_state.get("nodes", [])
    
    if isinstance(node_list, list):
        original_len = len(node_list)
        node_name_deleted = get_node_display_name(node_id_to_delete)
        
        # Filter out the node to delete
        st.session_state.nodes = [
            n for n in node_list 
            if not (isinstance(n, dict) and n.get("id") == node_id_to_delete)
        ]
        
        if len(st.session_state.nodes) < original_len:
            st.session_state.compiled_graph = None
            # If the deleted node was selected, select the first available node
            if st.session_state.selected_node_id == node_id_to_delete:
                st.session_state.selected_node_id = (
                    st.session_state.nodes[0]['id'] if st.session_state.nodes else None
                )
            st.toast(f"Deleted {node_name_deleted}", icon="🗑️")
            st.rerun()
        else:
            st.warning(f"Node {node_id_to_delete} not found.")

def move_node_ui(node_id_to_move: str, direction: int):
    """
    Move a node up or down in the workflow order
    
    Args:
        node_id_to_move (str): ID of the node to move
        direction (int): Direction to move (-1 for up, 1 for down)
    """
    node_list = st.session_state.get("nodes", [])
    
    if isinstance(node_list, list):
        try:
            # Find the index of the node to move
            index = next(
                i for i, n in enumerate(node_list) 
                if isinstance(n, dict) and n.get("id") == node_id_to_move
            )
            
            new_index = index + direction
            # Check if new position is valid
            if 0 <= new_index < len(node_list):
                node = node_list.pop(index)
                node_list.insert(new_index, node)
                st.session_state.compiled_graph = None
                st.session_state.selected_node_id = node_id_to_move
                st.rerun()
        except StopIteration:
            st.warning(f"Node {node_id_to_move} not found for moving.")

def add_conditional_rule_ui(node_id: str):
    """
    Add a new conditional routing rule to a node
    
    Args:
        node_id (str): ID of the node to add a rule to
    """
    node_list = st.session_state.get("nodes", [])
    
    if isinstance(node_list, list):
        for i, node in enumerate(node_list):
            if isinstance(node, dict) and node.get("id") == node_id:
                # Initialize routing rules structure if not present
                if not isinstance(node.get("routing_rules"), dict):
                    node["routing_rules"] = {}
                
                if not isinstance(node["routing_rules"].get("conditional_targets"), list):
                    node["routing_rules"]["conditional_targets"] = []
                
                # Add a new blank rule
                node["routing_rules"]["conditional_targets"].append({
                    "output_key": "",
                    "target_node_id": END_NODE_ID
                })
                
                st.session_state.compiled_graph = None
                st.session_state.selected_node_id = node_id
                st.rerun()
                return
                
    st.error(f"Node {node_id} not found.")

def delete_conditional_rule_ui(node_id: str, rule_index: int):
    """
    Delete a conditional routing rule from a node
    
    Args:
        node_id (str): ID of the node to modify
        rule_index (int): Index of the rule to delete
    """
    node_list = st.session_state.get("nodes", [])
    
    if isinstance(node_list, list):
        for i, node in enumerate(node_list):
            if isinstance(node, dict) and node.get("id") == node_id:
                rules_list = node.get("routing_rules", {}).get("conditional_targets")
                
                if isinstance(rules_list, list) and 0 <= rule_index < len(rules_list):
                    del node["routing_rules"]["conditional_targets"][rule_index]
                    st.session_state.compiled_graph = None
                    st.session_state.selected_node_id = node_id
                    st.rerun()
                    return
                else:
                    st.warning(f"Invalid rule index {rule_index}.")
                    return
                    
        st.error(f"Node {node_id} not found.")

def add_new_node(new_node_name: str):
    """
    Add a new node to the workflow
    
    Args:
        new_node_name (str): Name for the new node
    """
    if not new_node_name:
        st.error("Node Name required.", icon="❗")
        return
        
    # Check if name already exists
    if any(
        isinstance(n, dict) and n.get('name') == new_node_name 
        for n in st.session_state.nodes
    ): 
        st.warning(f"Name exists.", icon="⚠️")
        return
        
    # Create new node with default settings
    node_id = f"node_{uuid.uuid4().hex[:6]}"
    new_node = {
        "id": node_id,
        "name": new_node_name,
        "type": "llm_call",
        "prompt": f"Task: {new_node_name}\nInput: {{input_text}}\n(Use web search if needed.)",
        "routing_rules": {
            "default_target": END_NODE_ID,
            "conditional_targets": []
        }
    }
    
    st.session_state.nodes.append(new_node)
    st.session_state.compiled_graph = None
    st.session_state.selected_node_id = node_id
    st.toast(f"Added: {new_node_name}", icon="➕")
    st.rerun()