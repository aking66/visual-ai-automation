# Visual AI Automation Workflow Builder

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.1.0--alpha.1-orange)](https://github.com/yourusername/visual-ai-automation)
[![Tests](https://github.com/yourusername/visual-ai-automation/actions/workflows/ci_cd.yml/badge.svg)](https://github.com/yourusername/visual-ai-automation/actions)

## 🤖 Overview

Visual AI Automation Workflow Builder is an application that enables creating AI-powered automated workflows through a graphical interface. It allows you to create complex workflows with multiple flows and branches, where each node processes inputs using artificial intelligence models.

## 🔑 Key Features

- **Visual User Interface** - Design workflows through a drag-and-drop graphical interface
- **AI Nodes** - Utilize Google Gemini model for intelligent text processing
- **Conditional Routing Rules** - Define paths and branches for next steps based on previous node results
- **Web Search** - Ability to use web search system to obtain updated information
- **Ready-made Workflow Templates** - Several pre-configured templates for different purposes like sentiment analysis, classification, and deep research

## 🏗️ Project Structure

```
.
├── README.md               # This file
├── CHANGELOG.md            # Change log
├── run.py                  # Main application execution file
└── src/                    # Source code
   ├── __init__.py
   ├── config/             # Configurations and constants
   ├── core/               # Core business logic
   ├── models/             # Data model definitions
   ├── ui/                 # User interface components
   ├── utils/              # Helper tools
   └── workflows/          # Ready-made workflow templates
```

## 📋 Requirements

- Python 3.8+
- streamlit
- langgraph
- langchain-google-genai
- google-generativeai
- streamlit-agraph (for graph visualization)
- **New in Version 1.1.0**: Support for Anthropic and Cohere models

## ⚙️ Installation and Setup

1. **Install the requirements**:

```bash
pip install -r requirements.txt
```

2. **Get API keys**:
   - Register for a Google Gemini API key from [Google AI Studio](https://ai.google.dev/)
   - Optional: To take advantage of multi-model support in version 1.1.0:
    - Register for an Anthropic Claude API key from [Anthropic Console](https://console.anthropic.com/)
    - Register for a Cohere API key from [Cohere Dashboard](https://dashboard.cohere.com/)
   - Copy the `.env.example` file to `.env` and add your API keys

3. **Run the application**:

```bash
streamlit run run.py
```

Or use the included script:

```bash
./start.sh
```

## 🚀 How to Use

1. **Add Nodes**:
   - Use the "Node Palette" in the sidebar to add new nodes
   - Or select one of the ready-made workflow templates to start

2. **Configure Nodes**:
   - Select a node to edit in the "Node Configuration" section
   - Modify the name, model prompt text, and routing rules

3. **Compile the Workflow**:
   - After configuring all nodes, click on "Compile Workflow" in the sidebar

4. **Execute the Workflow**:
   - Enter the initial message in the "Execute Workflow" area
   - Click "Run Workflow" to start execution
   - View results in the "Execution Results" area

## 📝 Available Workflow Templates

- **Summarizer** - Simple model for text summarization
- **Sentiment** - Sentiment analysis with different paths for positive, negative, and neutral responses
- **Classify** - Classification of user intent and extraction of important information
- **Deep Research** - Conduct in-depth multi-angle research with cross-verification
- **Advanced Hedge Fund** - Advanced investment analysis with macroeconomic, sector, and company analysis

## 🧪 Testing

The project includes a comprehensive suite of tests to validate core components:

```bash
pytest --cov=src tests/
```

## 🚀 How to Run a Local Version

```bash
# Clone the repository
git clone https://github.com/yourusername/visual-ai-automation.git
cd visual-ai-automation

# Install requirements
pip install -r requirements.txt

# Set up environment file
cp .env.example .env
# Edit the .env file to add your API keys

# Run the application
streamlit run run.py
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the project
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
