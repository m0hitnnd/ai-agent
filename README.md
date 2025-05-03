# ai-agent

## AI-Powered To-Do List Agent

This project implements a simple command-line To-Do list manager that you can interact with using natural language.

There are two versions of the agent available:

1.  **NLP Version (`AgentTodo/nlp/agent_todo_nlp.py`)**: Uses the [spaCy](https://spacy.io/) library for Natural Language Processing to understand user commands (add, remove, show tasks) and extract task details.
2.  **Rule-Based Version (`AgentTodo/rule-based/agent_todo_rule_based.py`)**: Uses predefined rules and fuzzy string matching to interpret commands. This version might be less flexible but potentially more reliable for simple commands.

## Running the Agent

To run either version of the agent, navigate to the project's root directory in your terminal and execute the desired Python script:

**To run the NLP version:**

```bash
python AgentTodo/nlp/agent_todo_nlp.py
```

*(Note: You might need to install spaCy and its English language model first: `pip install spacy && python -m spacy download en_core_web_sm`)*

**To run the Rule-Based version:**

```bash
python AgentTodo/rule-based/agent_todo_rule_based.py
```

