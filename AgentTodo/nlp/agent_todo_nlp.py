import os
import re
import openai
import json 
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Task list - will store dictionaries: {'task': description, 'time': minutes}
tasks = []

def format_time(minutes):
    """Formats minutes into a human-readable string."""
    if minutes is None:
        return "N/A" # Handle cases where time is not applicable
    if minutes < 1:
        return "< 1 min"
    elif minutes < 60:
        return f"{minutes} mins"
    else:
        hours = minutes // 60
        mins = minutes % 60
        if mins == 0:
            return f"{hours} hr{'s' if hours > 1 else ''}"
        else:
            return f"{hours} hr{'s' if hours > 1 else ''} {mins} mins"

def get_llm_command_analysis(user_input):
    """Uses OpenAI API to determine intent, entity, and estimated time."""
    if not openai.api_key:
        print("Warning: OPENAI_API_KEY not set. Command processing may fail.")
        # Return a default 'unknown' structure
        return {"intent": "unknown", "entity": None, "estimated_time": None}

    prompt = f"""
Analyze the user's request for a to-do list manager. Identify the intent, extract the task entity if applicable, and estimate the time in minutes ONLY if the intent is to add a task.

Respond ONLY with a valid JSON object containing the following keys:
- "intent": One of ["add_task", "remove_task", "show_tasks", "exit", "unknown"]
- "entity": The specific task description (string), or null if not applicable (e.g., for 'show_tasks' or 'exit'). Extract the core task, omitting instructions like 'add' or 'remove'.
- "estimated_time": The estimated time in minutes (integer) ONLY if the intent is "add_task", otherwise null.

User Request: "{user_input}"

JSON Output:
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-4o", # Or another suitable model
            messages=[
                {"role": "system", "content": "You are an assistant that analyzes to-do list commands and responds in JSON format."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1, # Low temperature for consistent JSON output
            max_tokens=150, # Allow enough tokens for JSON response
            response_format={ "type": "json_object" } # Request JSON output if model supports it
        )

        content = response.choices[0].message.content.strip()
        print(f"--- OpenAI API Response Start ---\n{content}\n--- OpenAI API Response End ---")

        # Attempt to parse the JSON response
        analysis = json.loads(content)

        # Basic validation of the received structure
        if not all(k in analysis for k in ["intent", "entity", "estimated_time"]):
            print(f"Warning: LLM response missing expected keys: {content}")
            return {"intent": "unknown", "entity": None, "estimated_time": None}

        # print(f"DEBUG: LLM Analysis: {analysis}") # Debug
        return analysis

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from LLM response: {e}. Response: {content}")
        return {"intent": "unknown", "entity": None, "estimated_time": None}
    except Exception as e:
        print(f"Error calling OpenAI API for command analysis: {e}")
        return {"intent": "unknown", "entity": None, "estimated_time": None}

def process_input(user_input):
    """
    Process user input using LLM analysis, manage tasks, and respond.
    """
    # Get analysis from LLM
    analysis = get_llm_command_analysis(user_input)
    intent = analysis.get("intent", "unknown")
    entity = analysis.get("entity") # Can be None
    estimated_time = analysis.get("estimated_time") # Can be None

    # Handle intents based on LLM analysis
    if intent == "add_task":
        if entity:
            # Time estimation is now part of the analysis
            if estimated_time is None:
                 print(f"Warning: LLM provided add_task intent for '{entity}' but no time estimate. Defaulting to 60.")
                 estimated_time = 60 # Default if LLM forgets
            task_item = {'task': entity, 'time': estimated_time}
            tasks.append(task_item)
            tasks.sort(key=lambda x: (x['time'] is None, x['time'])) # Sort, handling None
            return f"Task '{entity}' (est. {format_time(estimated_time)}) added to your list!"
        else:
            # Ask LLM to re-phrase if entity is missing?
            # For now, use a generic message
            return "I understood you want to add a task, but couldn't identify what. Could you be more specific?"

    elif intent == "remove_task":
        if entity:
            task_found = False
            # Iterate backwards to safely remove items
            for i in range(len(tasks) - 1, -1, -1):
                 # Using 'in' for flexible matching based on LLM entity extraction
                 # Consider exact match if LLM entity extraction is reliable:
                 # if tasks[i]['task'].lower() == entity.lower():
                if entity.lower() in tasks[i]['task'].lower():
                    removed_task = tasks.pop(i)
                    task_found = True
                    return f"Task '{removed_task['task']}' removed from your list!"

            if not task_found:
                 # Use entity provided by LLM in the message
                 return f"Could not find a task related to '{entity}' in your list."
        else:
             # Ask LLM to re-phrase?
            return "I understood you want to remove a task, but couldn't identify which one. Could you specify?"

    elif intent == "show_tasks":
        if tasks:
            tasks.sort(key=lambda x: (x['time'] is None, x['time'])) # Sort, handling None
            task_items_formatted = [f"- {item['task']} (~{format_time(item['time'])})" for item in tasks]
            task_list = "\n".join(task_items_formatted)
            return f"Here are your tasks (prioritized by estimated time):\n{task_list}"
        else:
            return "Your task list is empty!"

    elif intent == "exit":
        return "Goodbye! Have a productive day!"

    else: # Handles 'unknown' intent
        return "Sorry, I didn't quite understand that. Could you please rephrase? You can add, remove, or show tasks."

# Main loop to interact with the AI agent
def to_do_list_agent():
    print("Hi! I'm your To-Do List Manager. You can type things like:")
    print("- 'Add groceries to my list.'")
    print("- 'Can you show my tasks?'")
    print("- 'Delete groceries from my list.'")
    print("- 'Exit' to quit.")
    while True:
        user_input = input("You: ")
        response = process_input(user_input)
        print(f"AI: {response}")
        if "goodbye" in response.lower():
            break

# Run the AI agent
to_do_list_agent()
