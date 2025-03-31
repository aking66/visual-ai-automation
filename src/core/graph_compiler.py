# -*- coding: utf-8 -*-
"""
Graph compilation for the Visual AI Automation Workflow Builder
"""

import streamlit as st
import traceback
from langgraph.graph import StateGraph, START, END

from src.models.state import WorkflowState
from src.config.constants import DEFAULT_ROUTING_KEY, START_NODE_ID, END_NODE_ID
from src.core.llm import get_llm_instances
from src.core.node_processor import create_agent_node_function
from src.core.router import generic_router

def get_node_display_name(node_id: str) -> str:
    """
    Get a display name for a node based on its ID
    
    Args:
        node_id (str): The node ID to get a display name for
        
    Returns:
        str: A human-readable display name for the node
    """
    if node_id == START_NODE_ID: 
        return "⏹️ START"
    if node_id == END_NODE_ID: 
        return "🏁 END"
    
    if "nodes" in st.session_state and isinstance(st.session_state.nodes, list):
        for i, node in enumerate(st.session_state.nodes):
            if isinstance(node, dict) and node.get("id") == node_id: 
                return f"{i+1}. {node.get('name', f'Unk ({node_id})')}"
    
    return f"Unknown ({node_id})"

def compile_graph() -> bool:
    """
    Compile the workflow graph based on the nodes in st.session_state.nodes
    
    Returns:
        bool: True if compilation was successful, False otherwise
    """
    llm, _ = get_llm_instances()
    
    if not llm: 
        st.error("LLM not initialized.", icon="🔥")
        return False
    
    if not st.session_state.nodes: 
        st.warning("No nodes defined.", icon="⚠️")
        return False
    
    print("\n--- Compiling Graph (Dictionary State) ---")
    
    try:
        # Initialize the graph builder
        graph_builder = StateGraph(WorkflowState)
        
        # Filter valid nodes (with required fields)
        valid_nodes = [
            n for n in st.session_state.nodes 
            if isinstance(n, dict) and all(k in n for k in ["id", "name", "prompt"])
        ]
        
        if not valid_nodes: 
            st.warning("No valid nodes.", icon="⚠️")
            return False
        
        # Get the set of node IDs and the start node
        node_ids = {node['id'] for node in valid_nodes}
        start_node_id_actual = valid_nodes[0]["id"]
        
        print("  Adding Nodes:")
        possible_keys_per_node = {}
        
        # Add nodes to the graph
        for node_data in valid_nodes:
            node_id = node_data["id"]
            node_name = node_data["name"]
            node_prompt = node_data["prompt"]
            
            print(f"    - ID: {node_id}, Name: '{node_name}'")
            
            # Extract possible routing keys from routing rules
            routing_rules = node_data.get("routing_rules", {})
            cond_keys = {
                rule.get("output_key", "").strip() 
                for rule in routing_rules.get("conditional_targets", []) 
                if rule.get("output_key")
            }
            
            all_keys = cond_keys.union({DEFAULT_ROUTING_KEY, "error"})
            possible_keys_per_node[node_id] = list(all_keys)
            
            # Create the node function and add it to the graph
            agent_func = create_agent_node_function(
                node_id, node_name, node_prompt, possible_keys_per_node[node_id]
            )
            graph_builder.add_node(node_id, agent_func)
        
        # Add edges to the graph
        print("  Adding Edges:")
        # Add the edge from START to the first node
        graph_builder.add_edge(START, start_node_id_actual)
        print(f"    - START -> {get_node_display_name(start_node_id_actual)}")
        
        all_targets_valid = True
        
        for node_data in valid_nodes:
            node_id = node_data["id"]
            node_name = node_data["name"]
            
            routing_rules = node_data.get("routing_rules", {})
            default_target = routing_rules.get("default_target", END_NODE_ID)
            conditional_targets = routing_rules.get("conditional_targets", [])
            
            path_map = {}
            print(f"    - Edges from '{node_name}' ({node_id}):")
            seen_keys_for_node = set()
            node_targets_valid = True
            
            # Process conditional targets
            for rule_idx, rule in enumerate(conditional_targets):
                key = rule.get("output_key", "").strip()
                target_id = rule.get("target_node_id")
                
                if key and target_id:
                    # Validate that target exists
                    if target_id != END_NODE_ID and target_id not in node_ids:
                        st.error(
                            f"❌ Invalid Target: {node_name} '{key}'->'{get_node_display_name(target_id)}'", 
                            icon="🔥"
                        )
                        all_targets_valid = False
                        node_targets_valid = False
                        continue
                    
                    # Check for duplicate keys
                    if key in seen_keys_for_node:
                        st.warning(f"⚠️ Duplicate key '{key}' in '{node_name}'.", icon="⚠️")
                    
                    # Add the routing rule
                    path_map[key] = target_id
                    seen_keys_for_node.add(key)
                    print(f"      - If key '{key}' -> {get_node_display_name(target_id)}")
                
                elif key or target_id:
                    st.warning(f"Node '{node_name}' incomplete rule #{rule_idx+1}. Ignored.", icon="⚠️")
            
            # Add default routing if not overridden by a conditional rule
            if DEFAULT_ROUTING_KEY not in path_map:
                # Validate default target
                if default_target != END_NODE_ID and default_target not in node_ids:
                    st.error(
                        f"❌ Invalid Default Target: {node_name}->'{get_node_display_name(default_target)}'", 
                        icon="🔥"
                    )
                    all_targets_valid = False
                    node_targets_valid = False
                else:
                    path_map[DEFAULT_ROUTING_KEY] = default_target
                    print(f"      - If key '{DEFAULT_ROUTING_KEY}' -> {get_node_display_name(default_target)}")
            
            # Add implicit error route to END
            if "error" not in path_map:
                path_map["error"] = END_NODE_ID
                print(f"      - If key 'error' -> {get_node_display_name(END_NODE_ID)} (Implicit)")
            
            # Add conditional edges for this node
            if node_targets_valid:
                graph_builder.add_conditional_edges(node_id, generic_router, path_map)
            else:
                print(f"      -> Skipping edges for '{node_name}'.")
        
        # Stop compilation if any targets are invalid
        if not all_targets_valid:
            st.error("Compilation failed.", icon="🔥")
            return False
        
        # Set recursion limit based on graph size
        recursion_limit = len(valid_nodes) * 3 + 10
        print(f"  Setting recursion limit to: {recursion_limit}")
        
        # Compile the graph
        st.session_state.compiled_graph = graph_builder.compile(checkpointer=None)
        st.session_state.recursion_limit = recursion_limit
        
        print("✅ Graph compiled successfully!")
        st.toast("Workflow compiled!", icon="✅")
        return True
    
    except Exception as e:
        st.error(f"Compile error: {e}", icon="🔥")
        print(f"❌ Compile Error: {e}")
        traceback.print_exc()
        st.session_state.compiled_graph = None
        return False