# -*- coding: utf-8 -*-
"""
State definitions for the Visual AI Automation Workflow Builder
"""

from typing import Dict, TypedDict

# --- LangGraph State Definition ---
class WorkflowState(TypedDict):
    """Dictionary-based state passed between workflow nodes"""
    input: str  # Original input text
    node_outputs: Dict[str, str]  # Store outputs from each node
    last_response_content: str  # Content from the last executed node
    current_node_id: str  # The ID of the node that was just executed