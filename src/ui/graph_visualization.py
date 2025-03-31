# -*- coding: utf-8 -*-
"""
Graph visualization components for the Visual AI Automation Workflow Builder
This module handles the generation of graph data for visualization using streamlit-agraph
"""

from typing import List, Dict, Any, Tuple
from streamlit_agraph import Node, Edge, Config
from src.config.constants import START_NODE_ID, END_NODE_ID
import logging

# Configure logging system for debugging visualization issues
# Logs will be written to graph_debug.log in the project root
logging.basicConfig(
    filename='graph_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('graph_visualization')

def generate_agraph_data(nodes_data: List[Dict[str, Any]]) -> Tuple[List[Node], List[Edge]]:
    """
    Generates nodes and edges for the agraph visualization from workflow data
    
    This function processes the workflow nodes data and creates a visual representation
    by generating Node and Edge objects for the streamlit-agraph component.
    
    Args:
        nodes_data: List of node dictionaries containing workflow definition
        
    Returns:
        Tuple containing two lists:
        - List of Node objects for visualization
        - List of Edge objects for visualization
        
    Raises:
        Exception: Any error during graph data generation
    """
    logger.info("Starting to generate agraph data")
    logger.debug(f"Received nodes_data: {nodes_data}")

    agraph_nodes: List[Node] = []
    agraph_edges: List[Edge] = []

    try:
        # Add START node as the workflow entry point
        logger.info("Adding START node")
        agraph_nodes.append(Node(
            id=START_NODE_ID,
            label="START",
            shape="ellipse",
            color="#4CAF50",
            title="Workflow Entry Point"
        ))

        # Filter valid nodes for visualization (must be dictionaries with 'id' key)
        valid_nodes_vis = [node for node in nodes_data if isinstance(node, dict) and 'id' in node]
        logger.debug(f"Valid nodes for visualization: {valid_nodes_vis}")

        # Create lookup sets for node IDs and indices
        node_ids_vis = {node['id'] for node in valid_nodes_vis}
        node_indices = {node['id']: i for i, node in enumerate(valid_nodes_vis)}

        # Process each workflow node
        for i, node in enumerate(valid_nodes_vis):
            node_id = node['id']
            node_name = node.get('name', 'Unnamed')
            logger.info(f"Processing node: {node_id} - {node_name}")

            # Create node visualization (numbered box with node name)
            agraph_nodes.append(Node(
                id=node_id,
                label=f"{i+1}. {node_name}",
                shape="box",
                color="#90CAF9",
                borderWidth=1,
                title=f"ID: {node_id}\nPrompt: {node.get('prompt', '')[:100]}..."
            ))

            # Connect first node to START
            if i == 0:
                logger.info(f"Connecting START to node: {node_id}")
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

            # Add default target edge if it exists and is valid
            if default_target == END_NODE_ID or default_target in node_ids_vis:
                logger.info(f"Adding default edge from {node_id} to {default_target}")
                agraph_edges.append(Edge(
                    source=node_id,
                    target=default_target,
                    label="__DEFAULT__",
                    color="#9E9E9E",
                    dashes=True,  # Dashed line for default routes
                    arrows="to",
                    font={'align': 'middle'}
                ))

            # Add conditional routing edges (based on output keys)
            for rule in conditional_targets:
                key = rule.get("output_key", "").strip()
                target_id = rule.get("target_node_id")

                if key and target_id and (target_id == END_NODE_ID or target_id in node_ids_vis):
                    logger.info(f"Adding conditional edge from {node_id} to {target_id} with key: {key}")
                    agraph_edges.append(Edge(
                        source=node_id,
                        target=target_id,
                        label=key,  # The condition key that triggers this route
                        color="#2196F3",  # Blue for conditional routes
                        arrows="to",
                        font={'align': 'middle'}
                    ))

        # Add END node only if there are edges leading to it
        # This prevents showing an orphaned END node when no edges lead to it
        if any(hasattr(edge, 'target') and edge.target == END_NODE_ID for edge in agraph_edges):
            logger.info("Adding END node")
            agraph_nodes.append(Node(
                id=END_NODE_ID,
                label="END",
                shape="ellipse",
                color="#F44336",  # Red for end node
                title="Workflow End"
            ))

    except Exception as e:
        logger.error(f"Error generating agraph data: {e}")
        raise

    logger.info(f"Finished generating agraph data: {len(agraph_nodes)} nodes, {len(agraph_edges)} edges")
    return agraph_nodes, agraph_edges

def get_graph_config():
    """
    Get the configuration for the streamlit-agraph component
    
    Defines how the graph should be displayed, including physics, interaction options,
    and visual properties of nodes and edges.
    
    Returns:
        Config: The graph configuration object for streamlit-agraph
    """
    return Config(
        width='100%',
        height=500,
        directed=True,  # We need a directed graph for workflows
        physics={
            'enabled': True,  # Enable physics for automatic layout
            'solver': 'forceAtlas2Based',
            'forceAtlas2Based': {
                'gravitationalConstant': -60,  # Negative value pushes nodes apart
                'centralGravity': 0.01,       # Low value allows more spread
                'springLength': 120,          # Distance between connected nodes
                'springConstant': 0.1,        # How rigid the connections are
                'damping': 0.3                # How quickly the system stabilizes
            }
        },
        interaction={
            'navigationButtons': True,  # Show navigation controls
            'tooltipDelay': 300,        # How quickly tooltips appear
            'hover': True               # Enable hover effects
        },
        nodes={
            'font': {'size': 14}  # Node label font size
        },
        edges={
            'font': {'size': 12, 'align': 'middle'}  # Edge label font size and position
        },
        layout={
            'hierarchical': False  # Use force-directed layout instead of hierarchical
        },
        manipulation=False  # Don't allow users to manipulate the graph structure
    )