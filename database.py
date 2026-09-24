import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent / "honeypot.db"


def init_db():
    """Create the database and events table if they do not exist."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                ip TEXT NOT NULL,
                method TEXT NOT NULL,
                path TEXT NOT NULL,
                user_agent TEXT NOT NULL
            )
            """
        )
        connection.commit()


def add_event(timestamp, ip, method, path, user_agent):
    """Store one honeypot request event."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            """
            INSERT INTO events (timestamp, ip, method, path, user_agent)
            VALUES (?, ?, ?, ?, ?)
            """,
            (timestamp, ip, method, path, user_agent),
        )
        connection.commit()


def get_events():
    """Return all events, newest first."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.execute(
            """
            SELECT id, timestamp, ip, method, path, user_agent
            FROM events
            ORDER BY id DESC
            """
        )
        return cursor.fetchall()
