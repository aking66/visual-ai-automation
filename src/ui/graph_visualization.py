# -*- coding: utf-8 -*-
"""
Graph visualization components for the Visual AI Automation Workflow Builder
"""

from typing import List, Dict, Any, Tuple
from streamlit_agraph import Node, Edge, Config
from src.config.constants import START_NODE_ID, END_NODE_ID

def generate_agraph_data(nodes_data: List[Dict[str, Any]]) -> Tuple[List[Node], List[Edge]]:
    """
    Generate visualization data for the streamlit-agraph component
    
    Args:
        nodes_data (List[Dict[str, Any]]): The list of workflow nodes
        
    Returns:
        tuple[List[Node], List[Edge]]: Lists of nodes and edges for graph visualization
    """
    agraph_nodes: List[Node] = []
    agraph_edges: List[Edge] = []
    
    # Add START node
    agraph_nodes.append(Node(
        id=START_NODE_ID,
        label="START",
        shape="ellipse",
        color="#4CAF50",
        title="Workflow Entry Point"
    ))
    
    # Filter valid nodes for visualization
    valid_nodes_vis = [node for node in nodes_data if isinstance(node, dict) and 'id' in node]
    node_ids_vis = {node['id'] for node in valid_nodes_vis}
    node_indices = {node['id']: i for i, node in enumerate(valid_nodes_vis)}
    
    # Process each workflow node
    for i, node in enumerate(valid_nodes_vis):
        node_id = node['id']
        node_name = node.get('name', 'Unnamed')
        node_prompt_snippet = node.get('prompt', '')[:100] + "..."
        
        # Check if this node is currently selected
        is_selected = False
        if 'selected_node_id' in globals():
            is_selected = selected_node_id == node_id
        elif 'selected_node_id' in locals():
            is_selected = selected_node_id == node_id
        
        # Styling based on selection state
        border_width = 3 if is_selected else 1
        node_color = "#FFC107" if is_selected else "#90CAF9"
        
        # Create node visualization
        agraph_nodes.append(Node(
            id=node_id,
            label=f"{i+1}. {node_name}",
            shape="box",
            color=node_color,
            borderWidth=border_width,
            title=f"ID: {node_id}\nPrompt: {node_prompt_snippet}"
        ))
        
        # Connect first node to START
        if i == 0:
            agraph_edges.append(Edge(
                source=START_NODE_ID,
                target=node_id,
                label="Start Flow",
                color="#4CAF50",
                width=2
            ))
        
        # Process routing rules to create edges
        routing_rules = node.get("routing_rules", {})
        default_target = routing_rules.get("default_target", END_NODE_ID)
        conditional_targets = routing_rules.get("conditional_targets", [])
        added_vis_edges = set()
        
        # Add default target edge if it exists and is valid
        if default_target == END_NODE_ID or default_target in node_ids_vis:
            is_overridden = any(
                r.get("output_key") == "__DEFAULT__" for r in conditional_targets
            )
            edge_id = (node_id, default_target, "__DEFAULT__")
            
            if not is_overridden and edge_id not in added_vis_edges:
                agraph_edges.append(Edge(
                    source=node_id,
                    target=default_target,
                    label="__DEFAULT__",
                    color="#9E9E9E",
                    dashes=True,
                    arrows="to",
                    font={'align': 'middle'}
                ))
                added_vis_edges.add(edge_id)
        
        # Add conditional routing edges
        for rule in conditional_targets:
            key = rule.get("output_key", "").strip()
            target_id = rule.get("target_node_id")
            
            if key and target_id and (target_id == END_NODE_ID or target_id in node_ids_vis):
                edge_id = (node_id, target_id, key)
                
                if edge_id not in added_vis_edges:
                    # Check if this is a loopback (edge to an earlier node)
                    is_loopback = False
                    if target_id in node_indices and node_id in node_indices:
                        if node_indices[target_id] < node_indices[node_id]:
                            is_loopback = True
                    
                    edge_color = "#FF5722" if is_loopback else "#2196F3"
                    edge_label = f"LOOP: {key}" if is_loopback else key
                    
                    agraph_edges.append(Edge(
                        source=node_id,
                        target=target_id,
                        label=edge_label,
                        color=edge_color,
                        arrows="to",
                        font={'align': 'middle'}
                    ))
                    added_vis_edges.add(edge_id)
    
    # Add END node only if there are edges leading to it
    if any(hasattr(edge, 'target') and edge.target == END_NODE_ID for edge in agraph_edges):
        agraph_nodes.append(Node(
            id=END_NODE_ID,
            label="END",
            shape="ellipse",
            color="#F44336",
            title="Workflow End"
        ))
    
    return agraph_nodes, agraph_edges

def get_graph_config():
    """
    Get the configuration for the streamlit-agraph component
    
    Returns:
        Config: The graph configuration object
    """
    return Config(
        width='100%',
        height=500,
        directed=True,
        physics={
            'enabled': True,
            'solver': 'forceAtlas2Based',
            'forceAtlas2Based': {
                'gravitationalConstant': -60,
                'centralGravity': 0.01,
                'springLength': 120,
                'springConstant': 0.1,
                'damping': 0.3
            }
        },
        interaction={
            'navigationButtons': True,
            'tooltipDelay': 300,
            'hover': True
        },
        nodes={
            'font': {'size': 14}
        },
        edges={
            'font': {'size': 12, 'align': 'middle'}
        },
        layout={
            'hierarchical': False
        },
        manipulation=False
    )