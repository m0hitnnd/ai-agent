#for nlp
import spacy  # type: ignore

# Load spaCy small english language model
nlp = spacy.load("en_core_web_sm")

# Task list - will store dictionaries: {'task': description, 'time': minutes}
tasks = []

# Define intents and associated keywords
intents = {
    "add_task": ["add", "include", "put", "create"],
    "remove_task": ["remove", "delete", "erase", "clear"],
    "show_tasks": ["show", "list", "display", "view"],
    "exit": ["exit", "quit", "bye"]
}

def estimate_task_time(task_description):
    """Estimates the time required for a task based on keywords."""
    doc = nlp(task_description.lower())
    # Default to 1 hour 51 minutes (in minutes) if no specific keywords found
    time_minutes = 111

    # Keywords indicating duration (values in minutes)
    time_hints = {
        # Short tasks
        "email": 10, "call": 15, "quick": 15, "reply": 10, "message": 5, "text": 5,
        "buy": 30, "groceries": 45, "shop": 45, "errand": 30, "check": 10,
        # Medium tasks
        "meeting": 60, "schedule": 20, "plan": 90, "review": 45, "read": 60, "watch": 90,
        "organize": 75, "clean": 90, "fix": 60,
        # Long tasks
        "project": 240, "report": 180, "research": 120, "write": 120, "develop": 300, "build": 300,
        "assignment": 180, "presentation": 150, "study": 120, "learn": 180
    }

    found_hint = False
    # Check tokens first for direct hints
    for token in doc:
        if token.lemma_ in time_hints:
            time_minutes = time_hints[token.lemma_]
            found_hint = True
            break

    # If no direct token hint, check noun chunks
    if not found_hint:
        for chunk in doc.noun_chunks:
             # Check individual words within the chunk
             for word in chunk.text.split():
                 if word in time_hints:
                     time_minutes = time_hints[word]
                     found_hint = True
                     break # Use first hint found in the chunk
             if found_hint:
                 break # Exit outer loop once hint found

    return time_minutes

def format_time(minutes):
    """Formats minutes into a human-readable string."""
    if minutes < 1:
        return "< 1 min"
    if minutes < 60:
        return f"{minutes} mins"
    elif minutes < 60 * 24:
        hours = minutes // 60
        rem_minutes = minutes % 60
        if rem_minutes == 0:
            return f"{hours} hr{'s' if hours > 1 else ''}"
        else:
            # Only show minutes if significant (e.g., avoid "1 hr 0 mins")
            return f"{hours} hr{'s' if hours > 1 else ''} {rem_minutes} mins"
    else:
        days = minutes // (60 * 24)
        rem_hours = (minutes % (60 * 24)) // 60
        if rem_hours == 0:
             return f"{days} day{'s' if days > 1 else ''}"
        else:
             # Approximate days/hours for simplicity if needed, or be more precise:
             return f"{days} day{'s' if days > 1 else ''} {rem_hours} hr{'s' if rem_hours > 1 else ''}"

def identify_intent_and_entity(user_input):
    """
    Identify the user's intent and extract the task entity using spaCy.
    """
    # Process input text with spaCy
    doc = nlp(user_input.lower())

     # Print the contents of the doc object for debugging
    print("\n--- Debugging: spaCy Doc Tokens ---")
    for token in doc:
        print(f"Text: {token.text}, Lemma: {token.lemma_}, POS: {token.pos_}, Dep: {token.dep_}, Head: {token.head.text}")
    print("--- End of Debugging ---\n")

    # Default intent and entity
    intent = None
    entity = None

    # Find intent by matching keywords
    for token in doc:
        for key, keywords in intents.items():
            if token.lemma_ in keywords:  # Lemma ensures base word comparison
                intent = key
                break
        if intent:
            break

    print("\n--- Debugging: Noun Chunks ---")
    for chunk in doc.noun_chunks:
        print(f"Text: {chunk.text}, Root: {chunk.root.text}, Root Dep: {chunk.root.dep_}")
    print("--- End of Debugging ---\n")

    # Extract entity (task) from noun chunks
    for chunk in doc.noun_chunks:
        # Consider direct objects (dobj) or prepositional objects (pobj)
        if chunk.root.dep_ in ["dobj", "pobj"]:
            entity = chunk.text.strip()
            break

    return intent, entity

def process_input(user_input):
    """
    Process user input, determine intent and entity, estimate time,
    prioritize, and respond accordingly.
    """
    intent, entity = identify_intent_and_entity(user_input)

    # Handle intents
    if intent == "add_task":
        if entity:
            estimated_time = estimate_task_time(entity)
            task_item = {'task': entity, 'time': estimated_time}
            tasks.append(task_item)
            # Sort tasks immediately after adding, shortest first
            tasks.sort(key=lambda x: x['time'])
            return f"Task '{entity}' (est. {format_time(estimated_time)}) added to your list!"
        else:
            return "I didn't catch what task to add. Could you clarify?"

    elif intent == "remove_task":
        if entity:
            task_found = False
            # Iterate backwards to safely remove items
            for i in range(len(tasks) - 1, -1, -1):
                 # Simple substring matching for removal for flexibility
                 # Or use exact match: if tasks[i]['task'] == entity:
                if entity in tasks[i]['task']:
                    removed_task = tasks.pop(i)
                    task_found = True
                    # Removed the first match found when iterating backwards
                    return f"Task '{removed_task['task']}' removed from your list!"

            if not task_found:
                 return f"Task containing '{entity}' not found in your list."
        else:
            return "I didn't catch what task to remove. Could you clarify?"

    elif intent == "show_tasks":
        if tasks:
            # Ensure tasks are sorted by time before displaying
            tasks.sort(key=lambda x: x['time'])
            # Format list with estimated time
            task_items_formatted = [f"- {item['task']} (~{format_time(item['time'])})" for item in tasks]
            task_list = "\n".join(task_items_formatted)
            return f"Here are your tasks (prioritized by estimated time):\n{task_list}"
        else:
            return "Your task list is empty!"

    elif intent == "exit":
        return "Goodbye! Have a productive day!"

    else:
        return "Sorry, I didn't understand that. You can try commands like 'add', 'remove', or 'show'."

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
