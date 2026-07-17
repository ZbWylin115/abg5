"""
SQLite connection and schema initialization for ABG Bible.

Milestone 1: sets up the database file and a placeholder table so the
wiring is proven end-to-end. Real tables get added as features land.
"""

import sqlite3
from pathlib import Path
from contextlib import contextmanager

DB_PATH = Path(__file__).parent / "abg_bible.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@contextmanager
def get_db():
    """Context-managed connection for use in request handlers."""
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    """Create tables if they don't exist. Safe to call on every startup."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS app_meta (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            INSERT OR IGNORE INTO app_meta (key, value)
            VALUES ('schema_version', '1')
            """
        )
        conn.commit()
