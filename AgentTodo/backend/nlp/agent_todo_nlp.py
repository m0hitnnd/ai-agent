import os
import openai
import json
from dotenv import load_dotenv
import db_utils

# Load environment variables from .env file
load_dotenv()

# Load API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_llm_command_analysis(user_input):
    """Uses OpenAI API to estimate the time required for a task in minutes."""
    if not openai.api_key:
        print("Warning: OPENAI_API_KEY not set. Command processing may fail.")
        return {"estimated_time": None}

    prompt = f"""
Estimate the time required (in minutes, as an integer) to complete the following task description. Respond ONLY with a valid JSON object in the format: {{\"estimated_time\": <integer>}}.

Task: \"{user_input}\"

JSON Output:
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an assistant that estimates the time required for tasks and responds in JSON format."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=50,
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content.strip()
        print(f"--- OpenAI API Response Start ---\n{content}\n--- OpenAI API Response End ---")

        # Attempt to parse the JSON response
        analysis = json.loads(content)
        estimated_time = analysis.get("estimated_time")
        return {"estimated_time": estimated_time}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from LLM response: {e}. Response: {content}")
        return {"estimated_time": None}
    except Exception as e:
        print(f"Error calling OpenAI API for command analysis: {e}")
        return {"estimated_time": None}