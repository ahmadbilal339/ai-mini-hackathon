"""
LLM integration for TaskSum using Google Gemini.
"""
import os
import logging
import time
from typing import List
from google import genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    logger.warning("GEMINI_API_KEY not found in environment variables")

# Initialize the client
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

def generate_summary(completed_tasks: List[str]) -> str:
    """
    Generate a one-paragraph summary of completed tasks using Gemini.
    """
    if not completed_tasks:
        return "No tasks completed yet. Complete some tasks to generate a summary!"
    
    if not GEMINI_API_KEY or not client:
        return "Error: Gemini API key is not configured. Please check your .env file."
    
    # List of models to try (in case one is overloaded)
    models_to_try = [
        "gemini-flash-latest",
        "gemini-2.5-pro",
        "gemini-3-flash-preview",
        "gemini-2.5-flash",
    ]
    
    last_error = None
    
    # Try each model with retry
    for model_name in models_to_try:
        for attempt in range(3):  # 3 retries per model
            try:
                # Create the prompt
                tasks_list = "\n".join(f"- {task}" for task in completed_tasks)
                
                prompt = f"""
You are a helpful assistant that creates motivational summaries of completed tasks.

Here are the tasks that were completed today:
{tasks_list}

Generate a ONE-PARAGRAPH summary (2-4 sentences) that:
1. Celebrates the progress made
2. Mentions what was accomplished
3. Sounds natural and professional

Do not use bullet points. Just return a single paragraph.
"""
                
                # Generate response
                response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=prompt
                )
                
                # Extract and return the summary
                summary = response.text.strip()
                logger.info(f"Generated summary using model: {model_name}")
                return summary
                
            except Exception as e:
                last_error = str(e)
                logger.warning(f"Attempt {attempt+1} with {model_name} failed: {last_error}")
                
                # Wait before retry (exponential backoff)
                if attempt < 2:
                    wait_time = (attempt + 1) * 2  # 2, 4, 6 seconds
                    logger.info(f"Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                continue
        
        # If all retries for this model fail, try next model
        logger.warning(f"All retries failed for {model_name}, trying next model...")
    
    # If all models fail
    return f"Unable to generate summary: All models failed. Last error: {last_error}"