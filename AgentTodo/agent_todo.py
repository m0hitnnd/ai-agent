# Simple AI Agent: To-Do List Manager
tasks = []  # List to store tasks

def process_input(user_input):
    # Convert input to lowercase for consistency
    user_input = user_input.lower()

    # Adding a task
    if "add" in user_input:
        task_start = user_input.find("'") + 1
        task_end = user_input.rfind("'")
        if task_start > 0 and task_end > task_start:
            task = user_input[task_start:task_end]
            tasks.append(task)
            return f"Task '{task}' added to your list!"
        else:
            return "I couldn't understand the task. Use quotes like: Add 'Task name'."

    # Viewing tasks
    elif "show" in user_input or "list" in user_input:
        if tasks:
            return "Here are your tasks:\n" + "\n".join(f"- {task}" for task in tasks)
        else:
            return "Your task list is empty!"

    # Removing a task
    elif "remove" in user_input:
        task_start = user_input.find("'") + 1
        task_end = user_input.rfind("'")
        if task_start > 0 and task_end > task_start:
            task = user_input[task_start:task_end]
            if task in tasks:
                tasks.remove(task)
                return f"Task '{task}' removed from your list!"
            else:
                return f"Task '{task}' not found in your list."
        else:
            return "I couldn't understand which task to remove. Use quotes like: Remove 'Task name'."

    # Exiting
    elif "bye" in user_input or "exit" in user_input:
        return "Goodbye! Have a productive day!"

    # Unrecognized input
    else:
        return "Sorry, I didn't understand that. You can say things like 'Add', 'Show', or 'Remove'."

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
