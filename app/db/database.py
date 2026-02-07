import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent / "email_logs.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS email_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                name TEXT,
                status TEXT NOT NULL,
                error TEXT,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def log_email(email: str, name: str, status: str, error: str | None = None):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO email_logs (email, name, status, error, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                email,
                name,
                status,
                error,
                datetime.utcnow().isoformat()
            )
        )
        conn.commit()
