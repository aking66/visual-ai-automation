# -*- coding: utf-8 -*-
"""
LLM initialization and management for the Visual AI Automation Workflow Builder
"""

import os
import streamlit as st
from typing import Optional, Any, Dict, Tuple, Literal
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from langchain_cohere import ChatCohere

from src.config.constants import TOOLS_LIST_FOR_BINDING, DEFAULT_MODEL, DEFAULT_TEMPERATURE

# Global LLM variables
llm: Optional[Any] = None
llm_with_search: Optional[Any] = None
current_provider: str = "google"

# Model mapping by provider
MODEL_MAPPING = {
    "google": {
        "default": "gemini-1.5-pro",
        "alternatives": ["gemini-1.5-flash", "gemini-pro"]
    },
    "anthropic": {
        "default": "claude-3-opus-20240229", 
        "alternatives": ["claude-3-sonnet-20240229", "claude-3-haiku-20240307"]
    },
    "cohere": {
        "default": "command-r-plus",
        "alternatives": ["command-r", "command"]
    }
}

def initialize_llm(provider: str = "google") -> bool:
    """
    Initialize LLM with API key from environment
    
    Args:
        provider: The LLM provider to use ("google", "anthropic", or "cohere")
    
    Returns:
        bool: True if LLM was successfully initialized
    """
    global llm, llm_with_search, current_provider
    
    # Get API keys
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
    cohere_api_key = os.environ.get("COHERE_API_KEY")
    
    # Check if requested provider is available
    provider_keys = {
        "google": google_api_key,
        "anthropic": anthropic_api_key,
        "cohere": cohere_api_key
    }
    
    if not provider_keys[provider]:
        st.warning(f"No API key found for {provider}. Please set the environment variable.")
        return False
    
    try:
        # Initialize the requested provider
        if provider == "google":
            base_llm = ChatGoogleGenerativeAI(
                model=MODEL_MAPPING[provider]["default"], 
                google_api_key=google_api_key, 
                temperature=DEFAULT_TEMPERATURE
            )
        elif provider == "anthropic":
            base_llm = ChatAnthropic(
                model=MODEL_MAPPING[provider]["default"],
                anthropic_api_key=anthropic_api_key,
                temperature=DEFAULT_TEMPERATURE
            )
        elif provider == "cohere":
            base_llm = ChatCohere(
                model=MODEL_MAPPING[provider]["default"],
                api_key=cohere_api_key,
                temperature=DEFAULT_TEMPERATURE
            )
        else:
            st.error(f"Unknown provider: {provider}")
            return False
            
        llm = base_llm
        llm_with_search = base_llm.bind_tools(TOOLS_LIST_FOR_BINDING)
        current_provider = provider
        print(f"LLM initialized ({provider}: {MODEL_MAPPING[provider]['default']}). Tool binding added.")
        return True
        
    except Exception as e: 
        st.error(f"LLM Init Error for {provider}: {e}", icon="🔥")
        llm = None
        llm_with_search = None
        return False

def get_llm_instances() -> Tuple[Optional[Any], Optional[Any]]:
    """
    Get the current LLM instances
    
    Returns:
        Tuple[Optional[Any], Optional[Any]]: Base LLM and LLM with search capabilities
    """
    return llm, llm_with_search

def get_available_providers() -> Dict[str, bool]:
    """
    Get available LLM providers based on environment variables
    
    Returns:
        Dict[str, bool]: Dictionary of providers and their availability
    """
    return {
        "google": bool(os.environ.get("GOOGLE_API_KEY")),
        "anthropic": bool(os.environ.get("ANTHROPIC_API_KEY")),
        "cohere": bool(os.environ.get("COHERE_API_KEY"))
    }

def get_available_models(provider: str) -> list:
    """
    Get available models for a specific provider
    
    Args:
        provider: The LLM provider to use ("google", "anthropic", or "cohere")
        
    Returns:
        list: List of available models
    """
    if provider in MODEL_MAPPING:
        return [MODEL_MAPPING[provider]["default"]] + MODEL_MAPPING[provider]["alternatives"]
    return []

def get_current_provider() -> str:
    """
    Get the currently active LLM provider
    
    Returns:
        str: Current provider name
    """
    return current_provider

def get_llm_response(prompt: str, use_search: bool = False) -> str:
    """
    Get a response from the LLM
    
    Args:
        prompt: The prompt to send to the LLM
        use_search: Whether to use the LLM with search capabilities
        
    Returns:
        str: The LLM response
    """
    model = llm_with_search if use_search else llm
    
    if model is None:
        if not initialize_llm():
            return "Error: LLM not initialized. Please check your API key."
        model = llm_with_search if use_search else llm
    
    try:
        response = model.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error calling LLM: {str(e)}"