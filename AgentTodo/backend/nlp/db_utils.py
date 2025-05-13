import sqlite3
from contextlib import closing

DB_PATH = 'AgentTodo/backend/nlp/tasks.db'

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        with closing(conn.cursor()) as c:
            c.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL,
                    time INTEGER
                )
            ''')
        conn.commit()

def add_task_to_db(task, time):
    with sqlite3.connect(DB_PATH) as conn:
        with closing(conn.cursor()) as c:
            c.execute('INSERT INTO tasks (task, time) VALUES (?, ?)', (task, time))
        conn.commit()

def get_all_tasks_from_db():
    with sqlite3.connect(DB_PATH) as conn:
        with closing(conn.cursor()) as c:
            c.execute('SELECT task, time FROM tasks')
            return c.fetchall()

def remove_task_from_db(task):
    with sqlite3.connect(DB_PATH) as conn:
        with closing(conn.cursor()) as c:
            c.execute('DELETE FROM tasks WHERE task LIKE ?', (f'%{task}%',))
        conn.commit()
