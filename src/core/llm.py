# -*- coding: utf-8 -*-
"""
LLM initialization module for the Visual AI Automation Workflow Builder

This module handles the initialization and configuration of Language Models
used for processing nodes in the workflow. It currently supports Google's
Gemini model and provides functions to verify API key availability.
"""

import os
from typing import Dict, Any, Optional

import streamlit as st
from langchain_core.language_models.base import BaseLanguageModel
from langchain_google_genai import ChatGoogleGenerativeAI
from src.config.constants import WEB_SEARCH_TOOL_DICT

def initialize_llm() -> bool:
    """
    Initialize the LLM instances for workflow processing
    
    This function:
    1. Verifies that the Google API key is available
    2. Initializes the LLM instances with appropriate settings
    3. Caches the LLM instances in session state
    
    Returns:
        bool: True if initialization was successful, False otherwise
    """
    if not os.environ.get("GOOGLE_API_KEY"):
        st.session_state.llm_instances = None
        return False
        
    try:
        # Create processor LLM instance (with web search if available)
        if WEB_SEARCH_TOOL_DICT:
            processor_llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-pro",
                tools=[WEB_SEARCH_TOOL_DICT],
                convert_system_message_to_human=True,
                temperature=0.2,
            )
        else:
            processor_llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-pro",
                convert_system_message_to_human=True,
                temperature=0.2,
            )
            
        # Store the LLM instances in session state
        st.session_state.llm_instances = {
            'processor_llm': processor_llm,
        }
        return True
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"LLM Init Error: {e}")
        st.session_state.llm_instances = None
        return False

def get_llm_instances() -> Dict[str, BaseLanguageModel]:
    """
    Get the initialized LLM instances
    
    Returns the cached LLM instances or initializes them if not available.
    
    Returns:
        Dict[str, BaseLanguageModel]: Dictionary of LLM instances or empty dict if initialization failed
    """
    if not hasattr(st.session_state, 'llm_instances') or not st.session_state.llm_instances:
        init_success = initialize_llm()
        if not init_success:
            return {}
            
    return st.session_state.llm_instances or {}