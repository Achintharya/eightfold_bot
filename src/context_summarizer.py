"""
Simplified Context Summarizer Module for Company Research Agent
"""

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv('config/.env')

def summarize_context(silent_mode=True):
    """
    Summarize the context from the JSON file and save it to a text file
    
    Args:
        silent_mode: If True, suppress output
        
    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    try:
        # Load JSON file
        with open("data/context.json", "r") as file:
            json_data = json.load(file)
        
        if not json_data:
            if not silent_mode:
                print("Warning: No context data found to summarize.")
            return 1
        
        # Use Groq API directly for summarization
        api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key:
            # Fallback: Simple text extraction if no API key
            summary = "\n".join([
                f"- {item.get('summary', item.get('url', 'Unknown source'))}"
                for item in json_data if not item.get('error', False)
            ])
        else:
            # Prepare the prompt
            context = json.dumps(json_data, indent=2)
            prompt = f"""Summarize the following research data into clear, detailed points without any JSON formatting:

{context}

Provide a comprehensive summary that extracts all relevant information, organized by topics."""
            
            try:
                # Make API request to Groq
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": "llama-3.1-8b-instant",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a technical writer who excels at extracting and formatting all relevant useful data into clear summaries."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.3,
                    "max_tokens": 2000
                }
                
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    response_data = response.json()
                    summary = response_data['choices'][0]['message']['content']
                else:
                    # Fallback to simple extraction
                    summary = "\n".join([
                        f"- {item.get('summary', 'No summary available')}"
                        for item in json_data if not item.get('error', False)
                    ])
                    
            except Exception as e:
                if not silent_mode:
                    print(f"API error, using simple extraction: {e}")
                # Fallback to simple extraction
                summary = "\n".join([
                    f"- {item.get('summary', 'No summary available')}"
                    for item in json_data if not item.get('error', False)  
                ])
        
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Save the summary to file
        with open("data/context.txt", "w", encoding='utf-8') as file:
            file.write(summary)
        
        if not silent_mode:
            print("\nContext summarization completed successfully!")
        
        return 0
        
    except FileNotFoundError:
        if not silent_mode:
            print("Error: Context JSON file not found. Please run web context extraction first.")
        return 1
    except Exception as e:
        if not silent_mode:
            print(f"Error during context summarization: {e}")
        return 1


def get_context_summary():
    """
    Get the current context summary
    
    Returns:
        str: The context summary text, or empty string if not found
    """
    try:
        with open("data/context.txt", "r", encoding='utf-8') as file:
            return file.read()
    except:
        return ""


if __name__ == "__main__":
    exit_code = summarize_context(silent_mode=False)
    exit(exit_code)
