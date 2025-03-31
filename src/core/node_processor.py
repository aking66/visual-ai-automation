# -*- coding: utf-8 -*-
"""
Node processing logic for the Visual AI Automation Workflow Builder
"""

import re
import streamlit as st
from typing import List, Dict, Any

from src.models.state import WorkflowState
from src.core.llm import get_llm_instances
from src.config.constants import ROUTING_KEY_MARKER, DEFAULT_ROUTING_KEY

def create_agent_node_function(node_id: str, node_name: str, node_prompt: str, possible_keys: List[str]):
    """
    Factory function that creates node execution functions
    
    Args:
        node_id (str): Unique identifier for the node
        node_name (str): Display name for the node
        node_prompt (str): The prompt template for the LLM
        possible_keys (List[str]): List of possible routing keys for this node
        
    Returns:
        function: The node function that can be called during workflow execution
    """
    def agent_node_function(state: WorkflowState) -> WorkflowState:
        print(f"\n--- Executing Node: {node_name} ({node_id}) ---")
        if "execution_log" not in st.session_state: 
            st.session_state.execution_log = []
        st.session_state.execution_log.append(f"⚙️ Executing Node: **{node_name}**")

        # Get the LLM instances
        _, llm_with_search = get_llm_instances()
        
        if not llm_with_search:  # Error handling for LLM init
            error_msg = f"ERROR: LLM not initialized."
            st.session_state.execution_log.append(f"  -> ❌ Error: {error_msg}")
            updated_state = state.copy()
            updated_state["last_response_content"] = f"{error_msg} {ROUTING_KEY_MARKER} error"
            updated_state["current_node_id"] = node_id
            return updated_state

        # --- Prepare Context ---
        context_input = ""
        is_first_node = not state.get("last_response_content")
        
        if is_first_node:
            context_input = state.get("input", "")
            print(f"DEBUG: First node, input: '{context_input[:100]}...'")
        else:
            prev_content = state.get("last_response_content", "")
            print(f"DEBUG: Prev content type: {type(prev_content)}")
            
            if isinstance(prev_content, str): 
                context_input = re.sub(rf"\s*{ROUTING_KEY_MARKER}\s*\w+\s*$", "", prev_content).strip()
            else: 
                print("ERROR: Prev content not str")
                context_input = str(prev_content)  # Fallback
            
            print(f"DEBUG: Context input: '{context_input[:100]}...'")

        # --- Prepare Prompt ---
        prompt_with_context = node_prompt
        if '{input_text}' in node_prompt:
            prompt_with_context = node_prompt.replace('{input_text}', context_input)
        elif context_input:
            prompt_with_context += f"\n\nInput Context:\n{context_input}"
            
        current_task_prompt = f"Current Task ({node_name}):\n{prompt_with_context}\n(Search web if needed)."
        key_options_text = ", ".join(f"'{k}'" for k in possible_keys if k and k != DEFAULT_ROUTING_KEY)
        routing_instruction = f"\n\n--- ROUTING ---\nAfter response, MUST end with '{ROUTING_KEY_MARKER} <key>' (e.g., from [{key_options_text}]).\n--- END ROUTING ---"
        full_prompt = current_task_prompt + routing_instruction
        
        print(f"DEBUG: Full prompt type: {type(full_prompt)}")
        print(f"Node '{node_name}' sending prompt: {full_prompt[:300]}...")
        st.session_state.execution_log.append(f"  📝 Prompt Snippet: {prompt_with_context[:100]}...")

        try:
            # --- Invoke LLM ---
            result = llm_with_search.invoke(full_prompt)
            response_content = ""  # Default empty

            # --- Content Extraction ---
            if hasattr(result, 'content'):
                raw_content = result.content
                if isinstance(raw_content, str):
                    response_content = raw_content  # It was already a string
                elif isinstance(raw_content, list) and len(raw_content) > 0 and isinstance(raw_content[0], dict) and 'text' in raw_content[0]:
                    # Standard case for structured output: extract text from first block
                    response_content = raw_content[0].get('text', '')  # Use .get for safety
                    print("DEBUG: Extracted text from result.content[0]['text']")
                else:  # Handle unexpected formats
                    print(f"WARNING: Unexpected format for result.content: {type(raw_content)}. Trying str().")
                    response_content = str(raw_content)  # Fallback
            else: 
                print("WARNING: result has no 'content' attribute.")

            # --- Debugging & Logging ---
            print(f"\nDEBUG: Raw result type: {type(result)}")
            print(f"DEBUG: response_content type: {type(response_content)}")
            print(f"DEBUG: response_content value: '{str(response_content)[:500]}...'")
            log_snippet = str(response_content)[:100] if response_content is not None else "[No text content]"
            st.session_state.execution_log.append(f"  🤖 LLM Response Snippet: {log_snippet}...")

            # --- Tool Call Warning (if they still appear) ---
            if hasattr(result, 'tool_calls') and result.tool_calls:
                 calls = result.tool_calls
                 call_details = [f"{call.get('name', '?')}({call.get('args', {})})" for call in calls]
                 warning_msg = f"  ⚠️ WARNING: LLM response included 'tool_calls' ({call_details}). Graph not handling them."
                 print(warning_msg)
                 st.session_state.execution_log.append(warning_msg)
                 st.warning(warning_msg)

            # --- Routing Key Check ---
            if isinstance(response_content, str):
                match = re.search(rf"{ROUTING_KEY_MARKER}\s*(\w+)\s*$", response_content)
                if match:
                    st.session_state.execution_log.append(f"  🔑 Detected key: '{match.group(1)}'.")
                else:
                    st.session_state.execution_log.append(f"  ⚠️ WARNING: No routing key found.")
                    response_content += f" {ROUTING_KEY_MARKER} {DEFAULT_ROUTING_KEY}"
                    st.session_state.execution_log.append(f"  🔧 Appended default key.")
            else:  # Should not happen with current extraction, but kept as safeguard
                 st.session_state.execution_log.append(f"  ⚠️ ERROR: Extracted content not str ({type(response_content)}).")
                 response_content = f"Error: Invalid type {ROUTING_KEY_MARKER} {DEFAULT_ROUTING_KEY}"

            # --- Update State ---
            updated_state = state.copy()
            if "node_outputs" not in updated_state or not isinstance(updated_state["node_outputs"], dict):
                updated_state["node_outputs"] = {}
            updated_state["node_outputs"][node_id] = str(response_content)  # Store string
            updated_state["last_response_content"] = str(response_content)  # Store string
            updated_state["current_node_id"] = node_id
            return updated_state

        # --- Exception Handling ---
        except Exception as e:  # Catch any errors during invoke/processing
            error_msg = f"Error in node {node_name} ({node_id}): {e}"
            print(error_msg)
            st.session_state.execution_log.append(f"  -> ❌ Error: {e}")
            updated_state = state.copy()
            updated_state["last_response_content"] = f"ERROR: {error_msg} {ROUTING_KEY_MARKER} error"
            updated_state["current_node_id"] = node_id
            import traceback
            traceback.print_exc()
            return updated_state

    return agent_node_function