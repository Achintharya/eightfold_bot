"""
Simplified Article Writer Module for Company Research Agent
"""

import os
import requests
import json
from datetime import datetime
from typing import Generator
from dotenv import load_dotenv

load_dotenv('config/.env')

def generate_chat_response(context, query, silent_mode=True):
    """
    Generate content using the Mistral API (non-streaming version for backward compatibility)
    
    Args:
        context (str): The context to use for generating the response
        query (str): The user query
        silent_mode (bool): If True, suppress output (default for agent use)
        
    Returns:
        str: The generated response
    """
    # Get the model and API key from environment
    api_key = os.getenv("MISTRAL_API_KEY")
    
    if not api_key:
        return "Error: Mistral API key not found. Please check your .env file."
    
    # Prepare the prompt message
    current_date = datetime.now().strftime("%Y-%m-%d")
    prompt_message = f"""Current Date: {current_date}
Context: {context}
Query: {query}"""

    try:
        # Prepare the API request
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        payload = {
            "model": "mistral-small-latest",
            "messages": [
                {
                    "role": "system", 
                    "content": "You are an AI that writes professionally about the context provided, WITHOUT hallucination. Write in markdown format."
                },
                {
                    "role": "user", 
                    "content": prompt_message
                }
            ]
        }
        
        # Make the API request
        response = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        # Check for errors
        response.raise_for_status()
        
        # Parse the response
        response_data = response.json()
        
        if not silent_mode:
            print("Content generation completed successfully")
            
        return response_data['choices'][0]['message']['content']

    except requests.exceptions.RequestException as e:
        error_msg = f"Error generating response: {str(e)}"
        if not silent_mode:
            print(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        if not silent_mode:
            print(error_msg)
        return error_msg


def generate_chat_response_stream(context: str, query: str) -> Generator[str, None, None]:
    """
    Generate content using the Mistral API with streaming for frontend display
    
    Args:
        context (str): The context to use for generating the response
        query (str): The user query
        
    Yields:
        str: Chunks of the generated response for streaming
    """
    # Get the model and API key from environment
    api_key = os.getenv("MISTRAL_API_KEY")
    
    if not api_key:
        yield json.dumps({"error": "Mistral API key not found. Please check your .env file."})
        return
    
    # Prepare the prompt message
    current_date = datetime.now().strftime("%Y-%m-%d")
    prompt_message = f"""Current Date: {current_date}
Context: {context}
Query: {query}"""

    try:
        # Prepare the API request for streaming
        headers = {
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
            "Authorization": f"Bearer {api_key}"
        }
        
        payload = {
            "model": "mistral-small-latest",
            "messages": [
                {
                    "role": "system", 
                    "content": "You are an AI that writes professionally about the context provided, WITHOUT hallucination. Write in markdown format."
                },
                {
                    "role": "user", 
                    "content": prompt_message
                }
            ],
            "stream": True  # Enable streaming
        }
        
        # Make the streaming API request
        response = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers=headers,
            json=payload,
            stream=True,
            timeout=30
        )
        
        # Check for errors
        response.raise_for_status()
        
        # Process the streaming response
        for line in response.iter_lines():
            if line:
                # Decode the line
                line_text = line.decode('utf-8')
                
                # Skip empty lines and comments
                if line_text.startswith('data: '):
                    # Extract JSON data
                    data_str = line_text[6:]  # Remove 'data: ' prefix
                    
                    # Check for end of stream
                    if data_str == '[DONE]':
                        break
                    
                    try:
                        # Parse JSON and extract content
                        data = json.loads(data_str)
                        
                        # Extract the delta content
                        if 'choices' in data and len(data['choices']) > 0:
                            delta = data['choices'][0].get('delta', {})
                            content = delta.get('content', '')
                            
                            if content:
                                # Yield the content chunk for streaming
                                yield json.dumps({"content": content})
                                
                    except json.JSONDecodeError:
                        # Skip malformed JSON
                        continue
                        
    except requests.exceptions.RequestException as e:
        yield json.dumps({"error": f"Error generating response: {str(e)}"})
    except Exception as e:
        yield json.dumps({"error": f"Unexpected error: {str(e)}"})


def save_to_file(content, filename):
    """
    Save content to a file
    
    Args:
        content (str): The content to save
        filename (str): The filename (without path)
        
    Returns:
        str: The full path of the saved file
    """
    # Ensure filename has .md extension
    if not filename.endswith('.md'):
        filename = f"{filename}.md"
    
    # Ensure articles directory exists
    articles_dir = "./articles"
    os.makedirs(articles_dir, exist_ok=True)
    
    # Full file path
    file_path = os.path.join(articles_dir, filename)
    
    # Save the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    return file_path
