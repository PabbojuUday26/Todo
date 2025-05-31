import sqlite3
import pandas as pd
from datetime import datetime

DB_NAME = "todo.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            completed BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            due_date DATE,
            priority INTEGER DEFAULT 1
        )
    ''')
    conn.commit()
    conn.close()

def get_tasks():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql('SELECT * FROM tasks', conn)
    conn.close()
    return df

def add_task(task, due_date=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO tasks (task, due_date) VALUES (?, ?)
    ''', (task, due_date))
    conn.commit()
    conn.close()

def update_task(task_id, task=None, completed=None, due_date=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    updates = []
    params = []
    
    if task is not None:
        updates.append("task = ?")
        params.append(task)
    if completed is not None:
        updates.append("completed = ?")
        params.append(completed)
    if due_date is not None:
        updates.append("due_date = ?")
        params.append(due_date)
    
    if updates:
        query = "UPDATE tasks SET " + ", ".join(updates) + " WHERE id = ?"
        params.append(task_id)
        c.execute(query, params)
    
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

def clear_completed():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE completed = TRUE')
    conn.commit()
    conn.close()