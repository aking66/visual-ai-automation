# -*- coding: utf-8 -*-
"""
Node processor module for the Visual AI Automation Workflow Builder

This module handles the processing of individual workflow nodes using LLMs.
It prepares prompts, manages LLM interactions, extracts routing keys, and updates workflow state.
"""

import re
import uuid
import streamlit as st
from typing import Dict, Any, Optional, Tuple

from langchain_core.language_models import BaseLanguageModel

from src.models.state import WorkflowState
from src.config.constants import ROUTING_KEY_MARKER, DEFAULT_ROUTING_KEY

def process_node(state: WorkflowState, node_data: Dict[str, Any], llm: BaseLanguageModel) -> WorkflowState:
    """
    Process a single workflow node using an LLM
    
    This function:
    1. Prepares the prompt for the LLM by replacing variables
    2. Calls the LLM with the prepared prompt
    3. Extracts any routing keys from the LLM response
    4. Updates the workflow state with results
    5. Logs the execution for the UI
    
    Args:
        state (WorkflowState): The current workflow state
        node_data (Dict[str, Any]): The node configuration data
        llm (BaseLanguageModel): The LLM instance to use for processing
        
    Returns:
        WorkflowState: The updated workflow state
    """
    # Extract node information
    node_id = node_data.get('id', f"unknown_{uuid.uuid4().hex[:8]}")
    node_name = node_data.get('name', 'Unnamed Node')
    node_prompt_template = node_data.get('prompt', "")
    
    # Log node execution start
    st.session_state.execution_log.append(f"🔄 **Node: {node_name}** (`{node_id}`)")
    
    # Prepare the prompt text with input from previous state
    prompt_text = node_prompt_template
    
    # Replace {input_text} with actual input text
    if "{input_text}" in prompt_text:
        input_text = state.input if state.current_node_id == "" else state.last_response_content
        prompt_text = prompt_text.replace("{input_text}", input_text)
    
    # Add state context if needed
    # Add more variable replacements here as needed
    
    # Log node prompt (truncated for UI)
    st.session_state.execution_log.append(
        f"📝 Prompt: {prompt_text[:150]}{'...' if len(prompt_text) > 150 else ''}"
    )
    
    try:
        # Call LLM with the prompt
        llm_response = llm.invoke(prompt_text)
        response_content = llm_response.content
        
        # Extract routing key if present
        routing_key, cleaned_content = extract_routing_key(
            response_content, 
            default_key=DEFAULT_ROUTING_KEY
        )
        
        # Log LLM response (truncated for UI)
        truncated_response = f"{cleaned_content[:250]}{'...' if len(cleaned_content) > 250 else ''}"
        st.session_state.execution_log.append(f"🤖 Response: {truncated_response}")
        
        if routing_key != DEFAULT_ROUTING_KEY:
            st.session_state.execution_log.append(f"🔀 Routing Key: `{routing_key}`")
        
        # Update workflow state
        new_state = state.copy()
        new_state.last_response_content = response_content
        new_state.node_outputs[node_id] = response_content  # Store full output with routing key
        new_state.current_node_id = routing_key
        
        return new_state
        
    except Exception as e:
        # Log error for UI
        st.session_state.execution_log.append(f"❌ **Error in node {node_name}**: {e}")
        print(f"Error processing node {node_id}: {e}")
        
        # Return state unchanged, but with error
        new_state = state.copy()
        new_state.last_response_content = f"ERROR: Node '{node_name}' failed: {e}"
        new_state.current_node_id = DEFAULT_ROUTING_KEY
        
        return new_state

def extract_routing_key(content: str, default_key: str = DEFAULT_ROUTING_KEY) -> Tuple[str, str]:
    """
    Extract the routing key from LLM response content
    
    Parses the content for a routing key marker followed by a key word.
    Returns both the key and the content with the key marker removed.
    
    Args:
        content (str): The LLM response content to parse
        default_key (str): The default key to use if no key is found
        
    Returns:
        Tuple[str, str]: (routing_key, cleaned_content)
    """
    if not content:
        return default_key, ""
        
    # Look for the routing key marker pattern
    pattern = rf"\s*{ROUTING_KEY_MARKER}\s*(\w+)\s*$"
    match = re.search(pattern, content)
    
    if match:
        routing_key = match.group(1).strip()
        # Remove the routing key from content
        cleaned_content = re.sub(pattern, "", content).strip()
        return routing_key, cleaned_content
    else:
        return default_key, content