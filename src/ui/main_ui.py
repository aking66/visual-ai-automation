# This is the main UI component for the Visual AI Automation Builder
# It handles the layout and rendering of the application interface

def render_main_layout():
    """Render the main layout of the application."""
    # Set the page title and icon
    st.set_page_config(
        page_title="Visual AI Automation Builder",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Application title
    st.title("🤖🧠 Visual AI Automation Builder")

    # Sidebar rendering
    llm_ready = render_sidebar()

    # Main layout with three columns
    col1, col2, col3 = st.columns([1, 2, 1])

    # Left column: Node Configuration
    with col1:
        render_node_config_section()

    # Middle column: Workflow Graph
    with col2:
        render_graph_section()

    # Right column: Placeholder for future sections or additional content
    with col3:
        st.subheader("🔧 Additional Tools")
        st.info("This space can be used for additional tools or information.")

    # Divider and Execution Section
    st.divider()
    render_execution_section(llm_ready)

    # Divider and Results Section
    st.divider()
    render_results_section()

# Call the main layout rendering function
render_main_layout()