#!/bin/bash
# Script for starting the Visual AI Automation Workflow Builder

echo "Starting Visual AI Automation Workflow Builder..."
echo "Loading environment variables from .env file if it exists"

if [ -f ".env" ]; then
    echo "Found .env file, loading environment variables"
    export $(grep -v '^#' .env | xargs)
fi

echo "Starting Streamlit application..."
streamlit run run.py