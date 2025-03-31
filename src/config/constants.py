# -*- coding: utf-8 -*-
"""
Configuration constants for the Visual AI Automation Workflow Builder
"""

from langgraph.graph import END

# --- Routing Constants ---
ROUTING_KEY_MARKER = "ROUTING_KEY:"
DEFAULT_ROUTING_KEY = "__DEFAULT__"
START_NODE_ID = "__START__"
END_NODE_ID = END

# --- Tool Configuration ---
# Gemini requires valid function names with specific formatting
WEB_SEARCH_TOOL_DICT = {"type": "web_search", "name": "web_search"}
TOOLS_LIST_FOR_BINDING = [WEB_SEARCH_TOOL_DICT]

# --- LLM Settings ---
DEFAULT_MODEL = "gemini-1.5-pro"
DEFAULT_TEMPERATURE = 0.2