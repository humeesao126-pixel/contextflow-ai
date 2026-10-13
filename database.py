
import sqlite3
from pathlib import Path

# Database stored in the project directory
DB_PATH = Path(__file__).resolve().parent / "contextflow.db"


def get_connection():
    """Create a connection to the SQLite database."""
    connection = sqlite3.connect(DB_PATH, timeout=10)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    """Create database tables if they do not exist."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL DEFAULT 'New Chat',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER NOT NULL,
                role TEXT NOT NULL
                    CHECK (role IN ('user', 'assistant')),
                content TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conversation_id)
                    REFERENCES conversations(id)
                    ON DELETE CASCADE
            )
        """)


def create_conversation(title="New Chat"):
    """Create a new chat and return its ID."""
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO conversations (title) VALUES (?)",
            (title,)
        )
        return cursor.lastrowid


def save_message(conversation_id, role, content):
    """Save one message to a conversation."""
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO messages
                (conversation_id, role, content)
            VALUES (?, ?, ?)
            """,
            (conversation_id, role, content)
        )


def load_messages(conversation_id):
    """Load all messages from a conversation."""
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT role, content
            FROM messages
            WHERE conversation_id = ?
            ORDER BY id ASC
            """,
            (conversation_id,)
        ).fetchall()

    return [
        {"role": role, "content": content}
        for role, content in rows
    ]


def list_conversations():
    """List conversations with newest first."""
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, title, created_at
            FROM conversations
            ORDER BY id DESC
            """
        ).fetchall()

    return rows


def delete_conversation(conversation_id):
    """Delete a conversation and its messages."""
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM conversations WHERE id = ?",
            (conversation_id,)
        )


def rename_conversation(conversation_id, new_title):
    """Rename an existing conversation."""
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE conversations
            SET title = ?
            WHERE id = ?
            """,
            (new_title, conversation_id)
        )
def save_exchange(conversation_id, user_text, assistant_text):
    """Save a complete conversation exchange atomically."""
    with get_connection() as conn:
        conn.executemany(
            """
            INSERT INTO messages
                (conversation_id, role, content)
            VALUES (?, ?, ?)
            """,
            [
                (conversation_id, "user", user_text),
                (conversation_id, "assistant", assistant_text)
            ]
        )