"""
R2Bit Contract Analyzer - Main Application File

This file contains the main Streamlit web application for analyzing legal contracts.
The app allows users to upload PDF contracts and get AI-powered analysis of the content.

Author: R2Talk Team
Created: 2025
"""

# --- Import Libraries ---

# Streamlit - Web app framework that turns Python scripts into interactive web apps
# OS - Provides functions for interacting with the operating system (like reading environment variables)
# Pathlib - Object-oriented way to handle file paths
# TOML - Library for parsing TOML configuration files (used for secrets management)
# PDFPlumber - Library for extracting text and data from PDFs
# BytesIO - Allows working with bytes data as if it were a file
# Custom utility functions for calling AI models (OpenAI, etc.)
# Custom utility functions for formatting prompts to send to AI models

import streamlit as st
import os
import pathlib
import toml
import pdfplumber
from io import BytesIO
from utils.llm import call_llm_api
from utils.prompt import format_prompt

# --- Custom Styling ---

# This CSS customizes the Streamlit interface appearance
# Hide the hamburger menu, Deploy button, and sidebar close button
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}  /* Hides the hamburger menu in the top-right */
footer {visibility: hidden;}     /* Hides the "Made with Streamlit" footer */
header {visibility: hidden;}     /* Hides the header section */
/* Hide the sidebar close button (X) */
[data-testid="stSidebarCollapseButton"] {
    display: none;
}
/* Change primary button color to blue for better visibility */
.stButton>button:first-child {
    background-color: #1E88E5;  /* Sets button background to blue */
    border-color: #1E88E5;      /* Sets button border to match background */
}
.stButton>button:first-child:hover {
    background-color: #1565C0;  /* Darker blue on hover for visual feedback */
    border-color: #1565C0;
}
</style>
"""

# --- Helper Functions ---

def load_api_key():
    """
    Load OpenAI API key from environment variables or secrets.toml.
    
    This function tries two methods to find your OpenAI API key:
    1. First checks if it's set as an environment variable called 'OPENAI_API_KEY'
    2. If not found there, looks for it in the .streamlit/secrets.toml file
    
    Returns:
        str: The OpenAI API key if found, None otherwise
    
    Note for beginners:
        API keys are like passwords that let your application use OpenAI's services.
        They should be kept secret and never shared or committed to public repositories.
    """
    # First try to get from environment variables
    # os.getenv looks for a named variable in your system's environment
    api_key = os.getenv('OPENAI_API_KEY')
    
    # If not found in environment, try secrets.toml
    if not api_key:
        # Create the path to the secrets file relative to this script's location
        # __file__ refers to the current file's path
        # pathlib.Path makes working with file paths easier
        secrets_path = pathlib.Path(__file__).parent / '.streamlit' / 'secrets.toml'
        if secrets_path.exists():
            # Load and parse the TOML file
            secrets = toml.load(secrets_path)
            # Try to get the API key from the 'default' section
            # The get() method returns None if the key doesn't exist
            api_key = secrets.get("default", {}).get("OPENAI_API_KEY")
    
    # Show an error if the API key wasn't found anywhere
    if not api_key:
        st.error("Error: OPENAI_API_KEY not found in environment variables or secrets.toml")
    
    return api_key

def extract_text_from_pdf(uploaded_file):
    """
    Extract text from uploaded PDF file.
    
    This function takes a PDF file that was uploaded through Streamlit's
    file_uploader and extracts all the text content from it.
    
    Args:
        uploaded_file: A file object from st.file_uploader
        
    Returns:
        str: The extracted text from all pages, with pages separated by double newlines.
             Returns an empty string if extraction fails.
    
    Note for beginners:
        PDFs can store text in different ways. This function extracts readable text,
        but might not work well with scanned documents or images of text.
    """
    try:
        # Convert the uploaded file to bytes that pdfplumber can read
        # BytesIO creates an in-memory file-like object
        with pdfplumber.open(BytesIO(uploaded_file.getvalue())) as pdf:
            # Extract text from each page and join them with double newlines
            # This is a list comprehension - a compact way to process each page
            # filter(None, ...) removes any pages that returned None (no text)
            return "\n\n".join(filter(None, (p.extract_text() for p in pdf.pages)))
    except Exception as e:
        # If anything goes wrong, show an error and return empty string
        st.error(f"Error extracting text from PDF: {e}")
        return ""

# --- Main App ---

def main():
    """
    Main application function that sets up the Streamlit interface and handles the workflow.
    
    This function:
    1. Configures the page layout and appearance
    2. Checks domain access restrictions (in production)
    3. Sets up the sidebar for user inputs
    4. Handles file uploads and validation
    5. Processes the contract when requested
    6. Displays results to the user
    
    Note for beginners:
        This is the central function that runs when you start the app.
        It coordinates all the different parts of the application.
    """
    # Set page config first as it must be the first Streamlit command
    # This configures the page title, icon and layout
    st.set_page_config(
        page_title="Contract Analyzer",  # This appears in the browser tab
        page_icon="📄",                # This emoji appears in the browser tab
        layout="wide"                  # Uses the full width of the browser
    )
    
    # Security check: Only allow access from specific domains
    # This is a basic form of access control for when the app is deployed online
    try:
        # Get the current runtime context (information about the current request)
        ctx = st.runtime.scriptrunner.get_script_run_ctx()
        if ctx and hasattr(ctx, 'request') and ctx.request:
            # Extract the hostname from the request
            host = ctx.request.headers.get('host', '')
            # Check if the hostname ends with our allowed domain
            if host and not host.endswith('r2talk.com.br'):
                st.error("Access denied: This application can only be accessed from r2talk.com.br domains")
                st.stop()  # Stops execution if domain check fails
    except Exception as e:
        # If there's any error in domain checking, log it but continue
        # This prevents the app from crashing if there's an issue with the domain check
        import logging
        logging.warning(f"Domain check warning: {str(e)}")
    
    # Apply the custom CSS styling defined earlier
    # unsafe_allow_html=True is needed because we're injecting custom HTML/CSS
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # Set the main title and caption for the app
    st.title("📄 Contract Analyzer")
    st.caption("Upload a contract PDF and get an AI-powered analysis.")

    # Load the API key and check if it exists
    api_key = load_api_key()
    if not api_key:
        # Show helpful error messages if API key is missing
        st.error("OpenAI API key not found. Please add it to `.streamlit/secrets.toml`.")
        st.info("Example:\n[default]\nOPENAI_API_KEY = \"your-api-key-here\"")
        return  # Exit the function early if no API key
    
    # Set the API key as an environment variable so the OpenAI library can use it
    os.environ["OPENAI_API_KEY"] = api_key

    # --- Create the sidebar for user inputs ---
    # Streamlit's 'with' statement creates a new container for UI elements
    with st.sidebar:
        st.header("Instructions")
        # Text area for custom instructions to guide the AI analysis
        instructions = st.text_area(
            "Additional guidelines for generation:",  # Label shown above the text area
            value="Please analyze this contract and provide a detailed breakdown of key terms, obligations, and notable clauses.",  # Default text
            height=120  # Height of the text area in pixels
        )
        # File uploader that only accepts PDF files
        uploaded_file = st.file_uploader(
            "Upload Contract PDF (max 2MB)",  # Label shown above the uploader
            type=["pdf"],                     # Only allow PDF files
            accept_multiple_files=False      # Only allow one file at a time
        )
        
        # Check if the uploaded file is too large (2MB limit)
        if uploaded_file is not None and uploaded_file.size > 2 * 1024 * 1024:  # 2MB in bytes
            st.error("Error: The uploaded file exceeds the 2MB size limit. Please upload a smaller file.")
            uploaded_file = None  # Reset the file to None so it's not processed
            
    # Add the "Run Analysis" button to the sidebar
    # type="primary" makes it blue, use_container_width=True makes it full width
    run_analysis = st.sidebar.button("Run Analysis", type="primary", use_container_width=True)

    # --- Main area: Instructions section ---
    st.subheader("How to Use the Contract Analyzer")
    # Markdown for formatting the instructions nicely
    # Triple quotes """ allow for multi-line strings in Python
    st.markdown("""
    Follow these steps to analyze your contract:
    
    1. **Upload your contract** - Use the file uploader in the sidebar to select a PDF contract (max 2MB)
    2. **Customize instructions** - Modify the analysis guidelines in the sidebar if needed
    3. **Run the analysis** - Click the "Run Analysis" button to process your document
    4. **Review results** - The AI-generated analysis will appear in the results section below
    5. **Iterate if needed** - You can upload different contracts or modify instructions for new analyses
    
    The analyzer works best with clearly formatted legal documents and provides insights on key terms, obligations, and potential issues.
    """)
    
    # --- Results section ---
    st.subheader("Analysis Results")

    # Initialize the session state variable if it doesn't exist
    # Session state persists data between reruns of the app
    # (Streamlit reruns the entire script on any interaction)
    if "llm_response" not in st.session_state:
        st.session_state.llm_response = "Results will appear here after analysis."

    # Handle the analysis process when the button is clicked
    if run_analysis:
        if not uploaded_file:
            # Remind user to upload a file if they haven't
            st.warning("Please upload a PDF file first.")
        else:
            # Extract text from the PDF using our helper function
            contract_text = extract_text_from_pdf(uploaded_file)
            if not contract_text.strip():  # .strip() removes whitespace, checking if any text remains
                # Show error if no text could be extracted
                st.error("Could not extract text from the PDF. Please check the file.")
            else:
                # Show a spinner while processing (gives visual feedback during wait)
                with st.spinner("Analyzing contract..."):
                    # Format the prompt for the AI using our utility function
                    # This prepares the text to be sent to the AI model
                    prompt = format_prompt(
                        analysis_type="Avaliação de Contrato de Compra e Venda de Imóveis",  # Type of analysis to perform
                        content=contract_text,        # The extracted contract text
                        instructions=instructions     # User's custom instructions
                    )
                    try:
                        # Call the AI model to analyze the contract
                        response = call_llm_api(
                            prompt=prompt,
                            model="gpt-4o",      # Using GPT-4 for high-quality analysis
                            temperature=0.0,    # 0.0 means more deterministic/factual responses
                            max_tokens=2000     # Limit response length to 2000 tokens
                        )
                        # Store the response in session state so it persists
                        st.session_state.llm_response = response
                    except Exception as e:
                        # Handle any errors that occur during API call
                        st.session_state.llm_response = f"Error: {e}"

    # Display the analysis results in a text area
    # The height parameter makes it large enough to show substantial results
    st.text_area(
        "AI Analysis Output:",               # Label above the text area
        value=st.session_state.llm_response,  # Content to display (from session state)
        height=400,                          # Height in pixels
        key="llm_response_display"           # Unique key for this element
    )

    # Footer section with privacy note
    st.markdown("---")  # Horizontal rule (divider line)
    st.info("Your data is processed securely and not stored.")  # Blue info box

# --- Application Entry Point ---

if __name__ == "__main__":
    main()  # Call the main function to start the application
