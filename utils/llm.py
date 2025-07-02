"""
LLM API Integration Module

This module handles communication with various Large Language Model (LLM) APIs
like OpenAI's GPT and Anthropic's Claude. It provides functions to securely retrieve 
API keys and make calls to these services with appropriate error handling.

Author: R2Talk Team
Created: 2025
"""

# Standard library imports
import os                  # For accessing environment variables and file operations
import logging             # For logging errors and information during execution
from typing import Dict, Any, Optional  # For type hints to make code more readable and maintainable

# Third-party LLM API libraries
import openai              # Python client for the OpenAI API
from openai import OpenAI  # The main client class for OpenAI API
# Note: Anthropic is imported conditionally when needed

# Configure logging
# This sets up the logging system to show INFO level messages and above
# (INFO, WARNING, ERROR, CRITICAL)
logging.basicConfig(level=logging.INFO)
# Create a logger specific to this module
logger = logging.getLogger(__name__)  # __name__ will be 'utils.llm'

def get_api_key(provider: str) -> str:
    """
    Retrieve API key for the specified LLM provider from various possible sources.
    
    This function tries multiple methods to find an API key in this order:
    1. Environment variables (already set in the current session)
    2. .env file in the project directory
    3. Streamlit secrets (if running in a Streamlit app)
    
    Args:
        provider (str): The LLM provider name ('openai', 'anthropic', etc.)
        
    Returns:
        str: The API key if found, or an empty string if not found
        
    Note for beginners:
        API keys are like passwords that let your application use AI services.
        They should be kept secret and never shared or committed to public repositories.
    """
    try:
        # Try environment variables first (set by streamlit_app.py)
        # Environment variables are values stored at the operating system level
        if provider.lower() == "openai":
            # os.environ.get() looks for the named variable, returns None if not found
            key = os.environ.get("OPENAI_API_KEY")
        elif provider.lower() == "anthropic":
            key = os.environ.get("ANTHROPIC_API_KEY")
        else:
            # Log a warning if an unknown provider is requested
            logger.warning(f"Unknown provider: {provider}")
            return ""
            
        if key:
            # Remove any accidental quotes that might have been included
            # when setting the environment variable
            return key.strip('"\'')
            
            
        # If not found in environment, try other methods
        # Import these libraries only when needed (to avoid unnecessary imports)
        import streamlit as st
        from dotenv import load_dotenv
        
        # Load environment variables from .env file
        # A .env file is a simple text file that contains KEY=VALUE pairs
        # The load_dotenv() function reads this file and adds its contents to os.environ
        load_dotenv()
        
        # Try environment variables again after loading .env
        # Now that we've loaded the .env file, check again for our API keys
        if provider.lower() == "openai":
            key = os.environ.get("OPENAI_API_KEY")
        elif provider.lower() == "anthropic":
            key = os.environ.get("ANTHROPIC_API_KEY")
            
        if key:
            return key.strip('"\'')
            
        # Try Streamlit secrets as last resort
        # Streamlit secrets are stored in .streamlit/secrets.toml
        try:
            # Check both the default section and the root level of secrets
            if provider.lower() == "openai":
                # The 'or' operator returns the first non-False value
                key = st.secrets.get('default', {}).get('OPENAI_API_KEY') or st.secrets.get('OPENAI_API_KEY')
            elif provider.lower() == "anthropic":
                key = st.secrets.get('default', {}).get('ANTHROPIC_API_KEY') or st.secrets.get('ANTHROPIC_API_KEY')
                
            if key:
                return key.strip('"\'')
                
        except Exception as e:
            # This might happen if we're not running in a Streamlit environment
            logger.warning(f"Could not access st.secrets: {str(e)}")
        
        # If we've tried all methods and found nothing, log an error
        logger.error(f"No API key found for provider: {provider}")
        return ""  # Return empty string to indicate failure
        
    except Exception as e:
        # Catch any unexpected errors that might occur
        # exc_info=True includes the full stack trace in the log
        logger.error(f"Error getting API key: {str(e)}", exc_info=True)
        return ""  # Return empty string to indicate failure

def call_llm_api(
    prompt: str,
    model: str = "gpt-3.5-turbo",  # Default model if none specified
    temperature: float = 0.7,      # Controls randomness/creativity
    max_tokens: int = 2000,        # Limits response length
    **kwargs                       # Allows passing additional parameters
) -> str:
    """
    Call the appropriate LLM API based on the model name.
    
    This function serves as a unified interface to different AI models.
    It automatically detects which provider to use based on the model name
    and handles the specific API calls accordingly.
    
    Args:
        prompt (str): The text prompt to send to the AI model
        model (str): Which AI model to use (e.g., 'gpt-4', 'claude-3-opus')
        temperature (float): Controls randomness in the response:
            - 0.0: Very deterministic/factual
            - 0.7: Balanced (default)
            - 1.0: Very creative/random
        max_tokens (int): Maximum length of response (roughly 4 chars per token)
        **kwargs: Any additional parameters to pass to the specific API
        
    Returns:
        str: The AI model's response text, or an error message if something fails
        
    Note for beginners:
        This function handles all the complexity of talking to different AI services.
        You just need to provide a prompt and specify which model you want to use.
        
        What are tokens? Tokens are pieces of text that the AI processes. They're roughly
        4 characters each in English, so 100 tokens ≈ 75 words. Both your prompt and the
        AI's response count toward token usage, which affects API costs.
    """
    try:
        # Determine provider based on model name prefix
        # Each AI provider uses specific naming conventions for their models
        if model.startswith("gpt"):
            # OpenAI models start with "gpt" (e.g., "gpt-4", "gpt-3.5-turbo")
            return _call_openai(prompt, model, temperature, max_tokens, **kwargs)
        elif model.startswith("claude"):
            # Anthropic models start with "claude" (e.g., "claude-3-opus")
            return _call_anthropic(prompt, model, temperature, max_tokens, **kwargs)
        else:
            # If the model name doesn't match any known provider, log an error
            logger.error(f"Unsupported model: {model}")
            return f"Error: Unsupported model '{model}'"
    except Exception as e:
        # Catch and log any errors that occur during the API call
        logger.error(f"Error calling LLM API: {str(e)}")
        # Return a user-friendly error message
        return f"Error calling LLM API: {str(e)}"

def _call_openai(
    prompt: str,
    model: str,
    temperature: float,
    max_tokens: int,
    **kwargs
) -> str:
    """
    Call the OpenAI API with the given parameters.
    
    This is a private helper function (note the _ prefix) that handles
    the specifics of calling OpenAI's API. It's called by the main
    call_llm_api function when an OpenAI model is requested.
    
    Args:
        prompt: The text prompt to send to the model
        model: Which OpenAI model to use (e.g., 'gpt-4', 'gpt-3.5-turbo')
        temperature: Controls randomness (0.0 to 1.0)
        max_tokens: Maximum response length
        **kwargs: Additional parameters for the OpenAI API
        
    Returns:
        str: The model's response or an error message
        
    Note for beginners:
        This function creates a "chat completion" which simulates a conversation
        with the AI. We set up the conversation with a system message (instructions
        for the AI) and a user message (your prompt).
    """
    try:
        # First, get the API key using our helper function
        api_key = get_api_key("openai")
        if not api_key:
            # If no API key is found, create a helpful error message
            error_msg = "OpenAI API key not found. Please set it in .streamlit/secrets.toml or .env file."
            logger.error(error_msg)
            return f"Error: {error_msg}"
        
        # Create an OpenAI client with our API key
        # This client handles the HTTP requests to OpenAI's servers
        client = OpenAI(api_key=api_key)
        
        # Make the actual API call to generate a completion
        # This is where we send our prompt to the AI model and get a response
        response = client.chat.completions.create(
            model=model,  # The specific model to use (e.g., "gpt-4")
            messages=[
                # System message sets the behavior/role of the AI
                {"role": "system", "content": "You are a helpful assistant that analyzes contracts."},
                # User message contains our actual prompt
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,  # Controls randomness of output
            max_tokens=max_tokens,   # Limits the length of the response
            **kwargs  # Any additional parameters passed to the function
        )
        
        # Check if we got a valid response with content
        if not response.choices or not response.choices[0].message.content:
            return "Error: No response content from the model."
            
        # Extract and return just the text content from the response
        # strip() removes any leading/trailing whitespace
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        # Handle any errors that occur during the API call
        error_msg = f"OpenAI API error: {str(e)}"
        logger.error(error_msg)  # Log the error for debugging
        return f"Error: {error_msg}"  # Return a user-friendly error message

def _call_anthropic(
    prompt: str,
    model: str,
    temperature: float,
    max_tokens: int,
    **kwargs
) -> str:
    """
    Call the Anthropic API (Claude) with the given parameters.
    
    This is a private helper function that handles the specifics of calling
    Anthropic's API for Claude models. It's called by the main call_llm_api
    function when a Claude model is requested.
    
    Args:
        prompt: The text prompt to send to the model
        model: Which Anthropic model to use (e.g., 'claude-3-opus')
        temperature: Controls randomness (0.0 to 1.0)
        max_tokens: Maximum response length
        **kwargs: Additional parameters for the Anthropic API
        
    Returns:
        str: The model's response or an error message
        
    Note for beginners:
        Anthropic's Claude models work similarly to OpenAI's models but with a
        slightly different API structure. This function handles those differences
        so you don't have to worry about them.
    """
    # Get the API key using our helper function
    api_key = get_api_key("anthropic")
    if not api_key:
        # If no API key is found, create a helpful error message
        return "Error: Anthropic API key not found. Please add it to your .streamlit/secrets.toml file."
    
    # Create an Anthropic client with our API key
    client = anthropic.Anthropic(api_key=api_key)
    
    try:
        # Make the API call to generate a message
        # Anthropic uses a messages API similar to OpenAI's chat API
        response = client.messages.create(
            model=model,               # The specific Claude model to use
            max_tokens=max_tokens,     # Maximum response length
            temperature=temperature,   # Controls randomness
            messages=[
                # User message contains our prompt
                {"role": "user", "content": prompt}
            ],
            **kwargs                   # Any additional parameters
        )
        # Extract the text content from the response
        # Anthropic returns content as a list of content blocks
        return response.content[0].text
    except Exception as e:
        # Handle any errors that occur during the API call
        logger.error(f"Anthropic API error: {str(e)}")
        return f"Anthropic API error: {str(e)}"
