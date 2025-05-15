import sqlite3
from contextlib import closing
import os

# Allow configuration of DB path through environment variable
DB_PATH = os.getenv('DATABASE_URL', os.path.join(os.path.dirname(__file__), 'tasks.db'))

def init_db():
    # Ensure the directory exists if DB_PATH includes a directory
    db_dir = os.path.dirname(DB_PATH)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
        
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

def get_all_tasks_with_ids():
    with sqlite3.connect(DB_PATH) as conn:
        with closing(conn.cursor()) as c:
            c.execute('SELECT id, task, time FROM tasks')
            return c.fetchall()

def get_last_inserted_task():
    with sqlite3.connect(DB_PATH) as conn:
        with closing(conn.cursor()) as c:
            c.execute('SELECT id, task, time FROM tasks ORDER BY id DESC LIMIT 1')
            return c.fetchone()

def delete_task_by_id(task_id):
    with sqlite3.connect(DB_PATH) as conn:
        with closing(conn.cursor()) as c:
            c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            return c.rowcount

def remove_task_from_db(task):
    with sqlite3.connect(DB_PATH) as conn:
        with closing(conn.cursor()) as c:
            c.execute('DELETE FROM tasks WHERE task LIKE ?', (f'%{task}%',))
        conn.commit()
