import sqlite3
from pathlib import Path
from datetime import datetime

# Localização do banco de dados
BASE_DIR = Path(__file__).parent
DB_DIR = BASE_DIR / "database"
DB_DIR.mkdir(exist_ok=True)

DB_PATH = DB_DIR / "assistant.db"


def connect():
    return sqlite3.connect(DB_PATH)


def initialize():
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)


def save_message(role, content):
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO messages (role, content, created_at)
            VALUES (?, ?, ?)
            """,
            (role, content, datetime.now().isoformat())
        )


def get_recent_messages(limit=10):
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT role, content
            FROM messages
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        ).fetchall()

    return [
        {"role": role, "content": content}
        for role, content in reversed(rows)
    ]


def clear_history():
    with connect() as conn:
        conn.execute("DELETE FROM messages")

def save_memory(content):
    with connect() as conn:
        cursor = conn.execute(
            """
            INSERT INTO memories (content, created_at)
            VALUES (?, ?)
            """,
            (content, datetime.now().isoformat())
        )

        return cursor.lastrowid

def get_memories():
    with connect() as conn:
        return conn.execute(
            """
            SELECT id, content, created_at
            FROM memories
            ORDER BY id DESC
            """
        ).fetchall()


def delete_memory(memory_id):
    with connect() as conn:
        cursor = conn.execute(
            "DELETE FROM memories WHERE id = ?",
            (memory_id,)
        )
        return cursor.rowcount > 0

def reset_memory():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM memories")
        cursor.execute("""
            DELETE FROM sqlite_sequence
            WHERE name = 'memories'
        """)
def memory_exists(content):
    with connect() as conn:
        rows = conn.execute(
            "SELECT content FROM memories"
        ).fetchall()

    normalized = content.strip().casefold()

    return any(
        row[0].strip().casefold() == normalized
        for row in rows
    )
