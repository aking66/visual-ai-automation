import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from src.core.node_processor import process_node

class TestNodeProcessor(unittest.TestCase):
    
    @patch('src.core.llm.get_llm_response')
    def test_process_node_basic(self, mock_get_llm_response):
        # Setup mock
        mock_get_llm_response.return_value = "Processed text response"
        
        # Test data
        node_config = {
            "id": "test_node",
            "name": "Test Node",
            "prompt": "Process this text: {input}",
            "routing_rules": {"default": "next_node"}
        }
        input_text = "Sample input"
        state = {"history": []}
        
        # Execute
        result = process_node(node_config, input_text, state)
        
        # Assert
        self.assertEqual(result["output"], "Processed text response")
        self.assertEqual(result["next"], "next_node")
        mock_get_llm_response.assert_called_once()
    
    @patch('src.core.llm.get_llm_response')
    def test_process_node_conditional_routing(self, mock_get_llm_response):
        # Setup mock
        mock_get_llm_response.return_value = "positive"
        
        # Test data
        node_config = {
            "id": "test_node",
            "name": "Test Node",
            "prompt": "Analyze sentiment: {input}",
            "routing_rules": {
                "positive": "positive_node",
                "negative": "negative_node",
                "default": "neutral_node"
            }
        }
        input_text = "I love this product"
        state = {"history": []}
        
        # Execute
        result = process_node(node_config, input_text, state)
        
        # Assert
        self.assertEqual(result["output"], "positive")
        self.assertEqual(result["next"], "positive_node")

if __name__ == '__main__':
    unittest.main()