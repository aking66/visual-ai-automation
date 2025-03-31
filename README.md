# 🤖🧠 Visual AI Automation Workflow Builder

A powerful, N8N-inspired visual workflow builder for AI auto
mations using Streamlit and LangGraph.

![Visual AI Automation Builder](https://img.shields.io/badge/AI-Automation-blue) ![LangGraph](https://img.shields.io/badge/LangGraph-Powered-green) ![Streamlit](https://img.shields.io/badge/Streamlit-App-red)

## 📋 Overview

The Visual AI Automation Workflow Builder is a sophisticated application that allows you to create, visualize, and execute complex AI-powered automation workflows through an intuitive graphical interface. Built on Streamlit and LangGraph, it enables non-developers to design multi-step AI processes with conditional branching, web search capabilities, and visual flow control.

## ✨ Features

- **Visual Node-Based Editor**: Create workflows by connecting nodes with an intuitive graph interface
- **Conditional Routing**: Design complex decision trees with rule-based routing between nodes
- **Web Search Integration**: Nodes can access the web to retrieve up-to-date information
- **Pre-Built Templates**: Several example workflows included (Summarizer, Sentiment Analysis, Classification, Research, Investment Analysis)
- **Live Execution**: Run workflows and see real-time execution logs
- **Dynamic Visualization**: Interactive graph display using streamlit-agraph
- **OpenAI GPT-4o Integration**: Powered by advanced language models for intelligent processing

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- OpenAI API Key

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/visual-ai-automation-builder.git
   cd visual-ai-automation-builder
   ```

2. Install required dependencies:
   ```
   pip install streamlit streamlit-agraph langchain-openai langgraph typing-extensions regex langchain-core
   ```

3. (Optional) Set your OpenAI API key as an environment variable:
   ```
   export OPENAI_API_KEY='your-api-key'
   ```

## 🚀 Usage

1. Run the application:
   ```
   streamlit run run.py
   ```

2. Access the UI in your browser (typically http://localhost:8501)

3. Input your OpenAI API key in the sidebar if not set as an environment variable

4. Create a workflow:
   - Add nodes using the Node Palette
   - Configure each node's prompt and routing rules
   - Connect nodes together by setting up conditional targets
   - Compile the workflow
   - Execute with your input text

## 📊 Example Workflows

The application comes with several pre-built example workflows:

### 📄 Simple Summarizer
A basic workflow that condenses text into 1-2 concise sentences.

### 🎭 Sentiment Analysis
Analyzes input text for sentiment and responds accordingly with different paths for positive, negative, and neutral sentiments.

### 🏷️ Classification
Classifies user input into different categories (complaint, query, compliment) and handles each appropriately.

### 🔬 Deep Research
A multi-stage research workflow that breaks research into angles, investigates each independently, cross-references findings, synthesizes results, and generates a final report.

### 📈 Enhanced Hedge Fund
A sophisticated investment workflow that analyzes goals and risk profiles, researches macro conditions, sectors and companies, validates findings, and provides tailored portfolio strategies.

## 💡 Creating Your Own Workflow

1. Add a node using the "Add LLM Node" button in the sidebar
2. Configure the node's prompt (use `{input_text}` as a placeholder for incoming data)
3. Set up routing rules to determine the flow based on the node's output
4. Add additional nodes and connect them
5. Compile the workflow when finished
6. Execute with your initial input

## ⚙️ Node Configuration

Each node has the following properties:

- **Name**: Identifies the node in the workflow
- **Prompt**: Instructions for the LLM to process
- **Routing Rules**: 
  - Default Target: Where to send output if no conditional rules match
  - Conditional Targets: Rules that route to different nodes based on specific outputs

Nodes automatically append a routing key to their responses (e.g., `ROUTING_KEY: done`), which determines the next node in the flow.

## 🔄 Workflow Execution

The application follows these steps during execution:

1. Starts at the first node with the user's input text
2. Processes the text through the LLM according to the node's prompt
3. Extracts a routing key from the LLM's response
4. Follows the appropriate path based on routing rules
5. Continues until reaching an END node
6. Displays the final output and execution log

## 🔍 Technical Details

- **State Management**: Uses dictionary-based state tracking via TypedDict
- **Graph Visualization**: Implemented with streamlit-agraph
- **LLM Integration**: Uses OpenAI's GPT-4o with tool binding for web search
- **Routing System**: Conditional paths based on extracted routing keys
- **Content Extraction**: Robust parsing of LLM responses for consistent results

## 🤝 Contributing

Contributions welcome! Feel free to submit issues or pull requests.

## 📜 License

MIT License

## 📱 Subscribe

Created by [Deep Charts](https://www.youtube.com/@DeepCharts). Subscribe for more AI tools and tutorials.
