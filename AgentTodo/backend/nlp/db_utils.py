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
            # Check if is_completed and actual_time columns exist
            c.execute("PRAGMA table_info(tasks)")
            columns = [column[1] for column in c.fetchall()]
            
            if 'tasks' not in [table[0] for table in c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]:
                # Create the table if it doesn't exist
                c.execute('''
                    CREATE TABLE tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        task TEXT NOT NULL,
                        time INTEGER,
                        is_completed BOOLEAN DEFAULT 0,
                        actual_time INTEGER
                    )
                ''')
            else:
                # Add columns if they don't exist
                if 'is_completed' not in columns:
                    c.execute('ALTER TABLE tasks ADD COLUMN is_completed BOOLEAN DEFAULT 0')
                if 'actual_time' not in columns:
                    c.execute('ALTER TABLE tasks ADD COLUMN actual_time INTEGER')
                
        conn.commit()

def add_task_to_db(task, time):
    with sqlite3.connect(DB_PATH) as conn:
        with closing(conn.cursor()) as c:
            c.execute('INSERT INTO tasks (task, time, is_completed) VALUES (?, ?, 0)', (task, time))
        conn.commit()

def get_all_tasks_from_db():
    with sqlite3.connect(DB_PATH) as conn:
        with closing(conn.cursor()) as c:
            c.execute('SELECT task, time, is_completed, actual_time FROM tasks')
            return c.fetchall()

def get_all_tasks_with_ids():
    with sqlite3.connect(DB_PATH) as conn:
        with closing(conn.cursor()) as c:
            c.execute('SELECT id, task, time, is_completed, actual_time FROM tasks')
            return c.fetchall()

def get_last_inserted_task():
    with sqlite3.connect(DB_PATH) as conn:
        with closing(conn.cursor()) as c:
            c.execute('SELECT id, task, time, is_completed, actual_time FROM tasks ORDER BY id DESC LIMIT 1')
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

def get_task_by_id(task_id):
    with sqlite3.connect(DB_PATH) as conn:
        with closing(conn.cursor()) as c:
            c.execute('SELECT id, task, time, is_completed, actual_time FROM tasks WHERE id = ?', (task_id,))
            return c.fetchone()

def update_task(task_id, new_task, new_time):
    with sqlite3.connect(DB_PATH) as conn:
        with closing(conn.cursor()) as c:
            c.execute('UPDATE tasks SET task = ?, time = ? WHERE id = ?', 
                     (new_task, new_time, task_id))
            conn.commit()
            return c.rowcount > 0

def complete_task(task_id, actual_time):
    with sqlite3.connect(DB_PATH) as conn:
        with closing(conn.cursor()) as c:
            c.execute('UPDATE tasks SET is_completed = 1, actual_time = ? WHERE id = ?', 
                     (actual_time, task_id))
            conn.commit()
            return c.rowcount > 0
