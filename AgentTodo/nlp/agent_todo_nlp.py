#for nlp
import spacy  # type: ignore

# Load spaCy small english language model
nlp = spacy.load("en_core_web_sm")

# Task list
tasks = []

# Define intents and associated keywords
intents = {
    "add_task": ["add", "include", "put", "create"],
    "remove_task": ["remove", "delete", "erase", "clear"],
    "show_tasks": ["show", "list", "display", "view"],
    "exit": ["exit", "quit", "bye"]
}

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
    Process user input, determine intent and entity, and respond accordingly.
    """
    intent, entity = identify_intent_and_entity(user_input)

    # Handle intents
    if intent == "add_task":
        if entity:
            tasks.append(entity)
            return f"Task '{entity}' added to your list!"
        else:
            return "I didn't catch what task to add. Could you clarify?"

    elif intent == "remove_task":
        if entity:
            if entity in tasks:
                tasks.remove(entity)
                return f"Task '{entity}' removed from your list!"
            else:
                return f"Task '{entity}' not found in your list."
        else:
            return "I didn't catch what task to remove. Could you clarify?"

    elif intent == "show_tasks":
        if tasks:
            task_list = "\n".join(f"- {task}" for task in tasks)
            return f"Here are your tasks:\n{task_list}"
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
