"""
QR Studio Pro — Data layer
Opens a fresh SQLite connection per operation (safe under Streamlit's
multi-threaded rerun model) instead of sharing one global connection/cursor.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "history.db")


def _connect():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS qr_history(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                qr_type TEXT NOT NULL,
                data TEXT NOT NULL,
                file_name TEXT,
                label TEXT,
                is_favorite INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Lightweight migration for older DBs created before "label"/"is_favorite" existed
        existing_cols = {row[1] for row in conn.execute("PRAGMA table_info(qr_history)")}
        if "label" not in existing_cols:
            conn.execute("ALTER TABLE qr_history ADD COLUMN label TEXT")
        if "is_favorite" not in existing_cols:
            conn.execute("ALTER TABLE qr_history ADD COLUMN is_favorite INTEGER DEFAULT 0")
        conn.commit()


def add_history(qr_type, data, file_name, label=None):
    with _connect() as conn:
        cur = conn.execute(
            "INSERT INTO qr_history(qr_type, data, file_name, label) VALUES (?,?,?,?)",
            (qr_type, data, file_name, label),
        )
        conn.commit()
        return cur.lastrowid


def get_history():
    with _connect() as conn:
        rows = conn.execute(
            "SELECT id, qr_type, data, file_name, label, is_favorite, created_at "
            "FROM qr_history ORDER BY created_at DESC"
        ).fetchall()
        return [dict(r) for r in rows]


def delete_record(record_id):
    with _connect() as conn:
        conn.execute("DELETE FROM qr_history WHERE id=?", (record_id,))
        conn.commit()


def delete_all():
    with _connect() as conn:
        conn.execute("DELETE FROM qr_history")
        conn.commit()


def toggle_favorite(record_id):
    with _connect() as conn:
        conn.execute(
            "UPDATE qr_history SET is_favorite = 1 - is_favorite WHERE id=?",
            (record_id,),
        )
        conn.commit()


def get_stats():
    """Aggregate stats for the Analytics dashboard and home page."""
    with _connect() as conn:
        total = conn.execute("SELECT COUNT(*) AS c FROM qr_history").fetchone()["c"]

        by_type = conn.execute(
            "SELECT qr_type, COUNT(*) AS c FROM qr_history GROUP BY qr_type ORDER BY c DESC"
        ).fetchall()

        by_day = conn.execute(
            "SELECT DATE(created_at) AS day, COUNT(*) AS c FROM qr_history "
            "GROUP BY DATE(created_at) ORDER BY day"
        ).fetchall()

        favorites = conn.execute(
            "SELECT COUNT(*) AS c FROM qr_history WHERE is_favorite=1"
        ).fetchone()["c"]

        return {
            "total": total,
            "by_type": [dict(r) for r in by_type],
            "by_day": [dict(r) for r in by_day],
            "favorites": favorites,
        }


init_db()
