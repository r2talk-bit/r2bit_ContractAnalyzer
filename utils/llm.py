import os
import logging
from typing import Dict, Any, Optional

# Import LLM libraries
import openai
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_api_key(provider: str) -> str:
    """
    Retrieve API key for the specified provider from environment variables,
    Streamlit secrets, or .env file.
    
    Args:
        provider: The LLM provider name (openai, anthropic, etc.)
        
    Returns:
        str: The API key
    """
    try:
        # Try environment variables first (set by streamlit_app.py)
        if provider.lower() == "openai":
            key = os.environ.get("OPENAI_API_KEY")
        elif provider.lower() == "anthropic":
            key = os.environ.get("ANTHROPIC_API_KEY")
        else:
            logger.warning(f"Unknown provider: {provider}")
            return ""
            
        if key:
            return key.strip('"\'')
            
        # If not found in environment, try other methods
        import streamlit as st
        from dotenv import load_dotenv
        
        # Load environment variables from .env file
        load_dotenv()
        
        # Try environment variables again after loading .env
        if provider.lower() == "openai":
            key = os.environ.get("OPENAI_API_KEY")
        elif provider.lower() == "anthropic":
            key = os.environ.get("ANTHROPIC_API_KEY")
            
        if key:
            return key.strip('"\'')
            
        # Try Streamlit secrets as last resort
        try:
            if provider.lower() == "openai":
                key = st.secrets.get('default', {}).get('OPENAI_API_KEY') or st.secrets.get('OPENAI_API_KEY')
            elif provider.lower() == "anthropic":
                key = st.secrets.get('default', {}).get('ANTHROPIC_API_KEY') or st.secrets.get('ANTHROPIC_API_KEY')
                
            if key:
                return key.strip('"\'')
                
        except Exception as e:
            logger.warning(f"Could not access st.secrets: {str(e)}")
        
        logger.error(f"No API key found for provider: {provider}")
        return ""
        
    except Exception as e:
        logger.error(f"Error getting API key: {str(e)}", exc_info=True)
        return ""

def call_llm_api(
    prompt: str,
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.7,
    max_tokens: int = 2000,
    **kwargs
) -> str:
    """
    Call the appropriate LLM API based on the model name.
    
    Args:
        prompt: The formatted prompt to send to the LLM
        model: The model to use (e.g., gpt-4, claude-3-opus)
        temperature: Controls randomness (0.0 = deterministic, 1.0 = creative)
        max_tokens: Maximum number of tokens in the response
        **kwargs: Additional parameters to pass to the API
        
    Returns:
        str: The LLM response
    """
    try:
        # Determine provider based on model name
        if model.startswith("gpt"):
            return _call_openai(prompt, model, temperature, max_tokens, **kwargs)
        elif model.startswith("claude"):
            return _call_anthropic(prompt, model, temperature, max_tokens, **kwargs)
        else:
            logger.error(f"Unsupported model: {model}")
            return f"Error: Unsupported model '{model}'"
    except Exception as e:
        logger.error(f"Error calling LLM API: {str(e)}")
        return f"Error calling LLM API: {str(e)}"

def _call_openai(
    prompt: str,
    model: str,
    temperature: float,
    max_tokens: int,
    **kwargs
) -> str:
    """Call OpenAI API"""
    try:
        api_key = get_api_key("openai")
        if not api_key:
            error_msg = "OpenAI API key not found. Please set it in .streamlit/secrets.toml or .env file."
            logger.error(error_msg)
            return f"Error: {error_msg}"
        
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes contracts."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        
        if not response.choices or not response.choices[0].message.content:
            return "Error: No response content from the model."
            
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        error_msg = f"OpenAI API error: {str(e)}"
        logger.error(error_msg)
        return f"Error: {error_msg}"

def _call_anthropic(
    prompt: str,
    model: str,
    temperature: float,
    max_tokens: int,
    **kwargs
) -> str:
    """Call Anthropic API"""
    api_key = get_api_key("anthropic")
    if not api_key:
        return "Error: Anthropic API key not found. Please add it to your .streamlit/secrets.toml file."
    
    client = anthropic.Anthropic(api_key=api_key)
    
    try:
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[
                {"role": "user", "content": prompt}
            ],
            **kwargs
        )
        return response.content[0].text
    except Exception as e:
        logger.error(f"Anthropic API error: {str(e)}")
        return f"Anthropic API error: {str(e)}"
