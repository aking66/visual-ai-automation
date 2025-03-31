import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from src.core.graph_compiler import compile_workflow_graph

class TestGraphCompiler(unittest.TestCase):
    
    def test_compile_workflow_graph_basic(self):
        # Test data
        nodes = {
            "start_node": {
                "id": "start_node",
                "name": "Start Node",
                "prompt": "Process this: {input}",
                "routing_rules": {"default": "second_node"}
            },
            "second_node": {
                "id": "second_node",
                "name": "Second Node",
                "prompt": "Further process: {input}",
                "routing_rules": {"default": None}
            }
        }
        
        # Execute
        result = compile_workflow_graph(nodes, "start_node")
        
        # Assert
        self.assertTrue("nodes" in result)
        self.assertTrue("start_node_id" in result)
        self.assertEqual(result["start_node_id"], "start_node")
        self.assertEqual(len(result["nodes"]), 2)
        
    def test_compile_workflow_graph_complex_routing(self):
        # Test data
        nodes = {
            "start_node": {
                "id": "start_node",
                "name": "Sentiment Analysis",
                "prompt": "Analyze sentiment: {input}",
                "routing_rules": {
                    "positive": "positive_node",
                    "negative": "negative_node",
                    "default": "neutral_node"
                }
            },
            "positive_node": {
                "id": "positive_node",
                "name": "Positive Response",
                "prompt": "Generate positive response: {input}",
                "routing_rules": {"default": None}
            },
            "negative_node": {
                "id": "negative_node",
                "name": "Negative Response",
                "prompt": "Generate negative response: {input}",
                "routing_rules": {"default": None}
            },
            "neutral_node": {
                "id": "neutral_node",
                "name": "Neutral Response",
                "prompt": "Generate neutral response: {input}",
                "routing_rules": {"default": None}
            }
        }
        
        # Execute
        result = compile_workflow_graph(nodes, "start_node")
        
        # Assert
        self.assertEqual(len(result["nodes"]), 4)
        self.assertEqual(result["start_node_id"], "start_node")

if __name__ == '__main__':
    unittest.main()