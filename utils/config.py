"""
Configuration file for Weather Data Parser & API Assistant.
Handles loading the system prompt from prompt.txt file.
"""

import os


def load_system_prompt() -> str:
    """Load the system prompt from prompt.txt file."""
    # TODO: Get the path to prompt.txt file
    prompt_file_path = os.path.join(os.path.dirname(__file__), '../prompt.txt')
    try:
        with open(prompt_file_path,'r') as file:
            content = file.read()
            return content.strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"prompt.txt file not found at {prompt_file_path}")
    
    # TODO: Handle other exceptions with appropriate message
    except Exception as e:
        raise Exception(f"Error loading prompt.txt: {str(e)}")



def get_system_prompt() -> str:
    """Get the system prompt with weather data placeholder."""
    return load_system_prompt()

# TODO: Export the system prompt as SYSTEM_PROMPT
SYSTEM_PROMPT = get_system_prompt()