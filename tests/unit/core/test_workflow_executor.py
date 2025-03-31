import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from src.core.workflow_executor import execute_workflow

class TestWorkflowExecutor(unittest.TestCase):
    
    @patch('src.core.node_processor.process_node')
    def test_execute_workflow_single_node(self, mock_process_node):
        # Setup mock
        mock_process_node.return_value = {
            "output": "Processed result",
            "next": None
        }
        
        # Test data
        workflow = {
            "nodes": {
                "start_node": {
                    "id": "start_node",
                    "name": "Start Node",
                    "prompt": "Process this text: {input}",
                    "routing_rules": {"default": None}
                }
            },
            "start_node_id": "start_node"
        }
        input_text = "Sample input"
        
        # Execute
        result = execute_workflow(workflow, input_text)
        
        # Assert
        self.assertTrue("execution_path" in result)
        self.assertTrue("final_output" in result)
        self.assertEqual(result["final_output"], "Processed result")
        mock_process_node.assert_called_once()
    
    @patch('src.core.node_processor.process_node')
    def test_execute_workflow_multiple_nodes(self, mock_process_node):
        # Setup mock with different return values for consecutive calls
        mock_process_node.side_effect = [
            {"output": "First node output", "next": "second_node"},
            {"output": "Final output", "next": None}
        ]
        
        # Test data
        workflow = {
            "nodes": {
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
            },
            "start_node_id": "start_node"
        }
        input_text = "Sample input"
        
        # Execute
        result = execute_workflow(workflow, input_text)
        
        # Assert
        self.assertEqual(len(result["execution_path"]), 2)
        self.assertEqual(result["final_output"], "Final output")
        self.assertEqual(mock_process_node.call_count, 2)

if __name__ == '__main__':
    unittest.main()