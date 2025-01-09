from difflib import get_close_matches

# Initialize an empty task list
tasks = []

# Define valid commands and their synonyms
command_map = {
    "add": ["add", "put", "insert", "include"],
    "remove": ["remove", "delete", "erase", "clear"],
    "show": ["show", "list", "display", "view"],
    "exit": ["exit", "bye", "quit"]
}

# Flatten the command map for fuzzy matching
all_commands = {word: action for action, synonyms in command_map.items() for word in synonyms}

def process_input(user_input):
    # Convert input to lowercase for consistency
    user_input = user_input.lower()

    # Identify the main command from the input
    words = user_input.split()
    main_action = words[0] if words else ""
    closest_match = get_close_matches(main_action, all_commands.keys(), n=1, cutoff=0.7)

    # If no valid command is found, return a suggestion
    if not closest_match:
        return "Sorry, I didn't understand that. Try saying 'Add', 'Remove', or 'Show'."

    # Map the matched synonym to the main action
    action = all_commands[closest_match[0]]

    # Confirm correction for misspelled actions
    if closest_match[0] != main_action:
        confirmation = input(f"Did you mean '{action}'? (yes/no): ").lower()
        if confirmation != "yes":
            return "Okay, no changes made."

    # Adding a task
    if action == "add":
        task = extract_task(user_input, main_action)
        if task:
            tasks.append(task)
            return f"Task '{task}' added to your list!"
        else:
            return "Please specify the task to add, e.g., Add 'Buy groceries'."

    # Removing a task
    elif action == "remove":
        task = extract_task(user_input, main_action)
        if task:
            if task in tasks:
                tasks.remove(task)
                return f"Task '{task}' removed from your list!"
            else:
                return f"Task '{task}' not found in your list."
        else:
            return "Please specify the task to remove, e.g., Remove 'Buy groceries'."

    # Viewing tasks
    elif action == "show":
        if tasks:
            return "Here are your tasks:\n" + "\n".join(f"- {task}" for task in tasks)
        else:
            return "Your task list is empty!"

    # Exiting
    elif action == "exit":
        return "Goodbye! Have a productive day!"

    # Default response
    else:
        return "Sorry, I didn't understand that. Try saying 'Add', 'Remove', or 'Show'."

def extract_task(user_input, action):
    """
    Extract the task description from the user's input.
    """
    # Remove the action part
    task_part = user_input[len(action):].strip()

    # If the task is surrounded by quotes, extract it
    if "'" in task_part:
        start = task_part.find("'") + 1
        end = task_part.rfind("'")
        return task_part[start:end].strip()

    # Otherwise, take the remaining part as the task
    return task_part.strip()

# Main loop to interact with the AI agent
def to_do_list_agent():
    print("Hi! I'm your To-Do List Manager. How can I help you?")
    while True:
        user_input = input("You: ")
        response = process_input(user_input)
        print(f"AI: {response}")
        if "goodbye" in response.lower():
            break

# Run the AI agent
to_do_list_agent()
