import streamlit as st
import os
import pathlib
import toml
import pdfplumber
from io import BytesIO
from utils.llm import call_llm_api
from utils.prompt import format_prompt

# Hide the hamburger menu and Deploy button
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""

# --- Helper Functions ---

def load_api_key():
    """Load OpenAI API key from environment variables or secrets.toml."""
    # First try to get from environment variables
    api_key = os.getenv('OPENAI_API_KEY')
    
    # If not found in environment, try secrets.toml
    if not api_key:
        secrets_path = pathlib.Path(__file__).parent / '.streamlit' / 'secrets.toml'
        if secrets_path.exists():
            secrets = toml.load(secrets_path)
            api_key = secrets.get("default", {}).get("OPENAI_API_KEY")
    
    if not api_key:
        st.error("Error: OPENAI_API_KEY not found in environment variables or secrets.toml")
    
    return api_key

def extract_text_from_pdf(uploaded_file):
    """Extract text from uploaded PDF file."""
    try:
        with pdfplumber.open(BytesIO(uploaded_file.getvalue())) as pdf:
            return "\n\n".join(filter(None, (p.extract_text() for p in pdf.pages)))
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return ""

# --- Main App ---

def main():
    # Set page config first as it must be the first Streamlit command
    st.set_page_config(
        page_title="Contract Analyzer",
        page_icon="📄",
        layout="wide"
    )
    
    # Check if the request is coming from the allowed domain (only in production)
    try:
        ctx = st.runtime.scriptrunner.get_script_run_ctx()
        if ctx and hasattr(ctx, 'request') and ctx.request:
            host = ctx.request.headers.get('host', '')
            if host and not host.endswith('r2talk.com.br'):
                st.error("Access denied: This application can only be accessed from r2talk.com.br domains")
                st.stop()
    except Exception as e:
        # If there's any error in domain checking, log it but continue
        import logging
        logging.warning(f"Domain check warning: {str(e)}")
    
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    st.title("📄 Contract Analyzer")
    st.caption("Upload a contract PDF and get an AI-powered analysis.")

    api_key = load_api_key()
    if not api_key:
        st.error("OpenAI API key not found. Please add it to `.streamlit/secrets.toml`.")
        st.info("Example:\n[default]\nOPENAI_API_KEY = \"your-api-key-here\"")
        return
    os.environ["OPENAI_API_KEY"] = api_key

    # --- Layout: Sidebar for input, main for output ---
    with st.sidebar:
        st.image("assets/r2bit1.png")  # Original size
        st.header("Instructions")
        instructions = st.text_area(
            "Describe what you want the AI to analyze:",
            value="Please analyze this contract and provide a detailed breakdown of key terms, obligations, and notable clauses.",
            height=120
        )
        uploaded_file = st.file_uploader(
            "Upload Contract PDF (max 2MB)",
            type=["pdf"],
            accept_multiple_files=False
        )
        
        if uploaded_file is not None and uploaded_file.size > 2 * 1024 * 1024:  # 2MB in bytes
            st.error("Error: The uploaded file exceeds the 2MB size limit. Please upload a smaller file.")
            uploaded_file = None
        run_analysis = st.button("Run Analysis", type="primary", use_container_width=True)

    # --- Main area: Results ---
    st.subheader("Analysis Results")

    if "llm_response" not in st.session_state:
        st.session_state.llm_response = "Results will appear here after analysis."

    if run_analysis:
        if not uploaded_file:
            st.warning("Please upload a PDF file first.")
        else:
            contract_text = extract_text_from_pdf(uploaded_file)
            if not contract_text.strip():
                st.error("Could not extract text from the PDF. Please check the file.")
            else:
                with st.spinner("Analyzing contract..."):
                    prompt = format_prompt(
                        analysis_type="Avaliação de Contrato de Compra e Venda de Imóveis",
                        content=contract_text,
                        instructions=instructions
                    )
                    try:
                        response = call_llm_api(
                            prompt=prompt,
                            model="gpt-4",
                            temperature=0.0,
                            max_tokens=2000
                        )
                        st.session_state.llm_response = response
                    except Exception as e:
                        st.session_state.llm_response = f"Error: {e}"

    st.text_area(
        "AI Analysis Output:",
        value=st.session_state.llm_response,
        height=400,
        key="llm_response_display"
    )

    st.markdown("---")
    st.info("Your data is processed securely and not stored.")

if __name__ == "__main__":
    main()
