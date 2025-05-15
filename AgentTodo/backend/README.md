# AgentTodo Backend

A FastAPI backend for the AgentTodo application with SQLite database and OpenAI integration.

## Local Development

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Set up environment variables (create a `.env` file):
```
OPENAI_API_KEY=your_openai_api_key
```

3. Run the server:
```
uvicorn api_server:app --reload --port 8000
```

## Deployment to Render

1. Create a new Web Service on Render.com
2. Link your GitHub repository
3. Configure the following settings:
   - **Name**: agent-todo-api (or your preferred name)
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -k uvicorn.workers.UvicornWorker api_server:app`
   - **Add environment variables**:
     - `OPENAI_API_KEY`: Your OpenAI API key
     - `DATABASE_URL`: `/var/data/tasks.db` (or your preferred location)

4. Click "Create Web Service"

## API Endpoints

- `GET /tasks`: List all tasks
- `POST /tasks`: Create a new task
- `DELETE /tasks/{task_id}`: Delete a task by ID 