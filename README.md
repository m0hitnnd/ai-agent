# ai-agent

## AI-Powered To-Do List Agent

This project implements a To-Do list manager with both command-line and native app interfaces, powered by AI for time estimation.

## Components

### 1. Command-Line Interfaces

There are two versions of the command-line agent available:

1.  **NLP Version (`AgentTodo/nlp/agent_todo_nlp.py`)**: Uses the [spaCy](https://spacy.io/) library for Natural Language Processing to understand user commands (add, remove, show tasks) and extract task details.
2.  **Rule-Based Version (`AgentTodo/rule-based/agent_todo_rule_based.py`)**: Uses predefined rules and fuzzy string matching to interpret commands. This version might be less flexible but potentially more reliable for simple commands.

### 2. Backend API

The project includes a RESTful API server (`AgentTodo/backend/`) that:
- Stores tasks in a database
- Uses OpenAI API to estimate time required for each task
- Serves task data to the native app

### 3. Native Apps

The project includes SwiftUI-based apps for macOS and iOS that provide a modern interface for managing your tasks. The app:
- Shows tasks sorted by estimated time
- Allows adding new tasks via a simple interface
- Displays AI-generated time estimates for each task

## Running the Command-Line Agent

To run either version of the agent, navigate to the project's root directory in your terminal and execute the desired Python script:

**To run the NLP version:**

```bash
python AgentTodo/nlp/agent_todo_nlp.py
```

if using python3

```bash
python3 AgentTodo/nlp/agent_todo_nlp.py
```

*(Note: You might need to install spaCy and its English language model first: `pip install spacy && python -m spacy download en_core_web_sm`)*

**To run the Rule-Based version:**

```bash
python AgentTodo/rule-based/agent_todo_rule_based.py
```

if using python3

```bash
python3 AgentTodo/rule-based/agent_todo_rule_based.py
```


