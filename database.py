import sqlite3
from contextlib import contextmanager
from datetime import datetime

DB_PATH = "qr_history.db"


@contextmanager
def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def _init_db():
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS history (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                qr_type      TEXT NOT NULL,
                data         TEXT NOT NULL,
                file_name    TEXT,
                label        TEXT,
                created_at   TEXT NOT NULL,
                is_favorite  INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        conn.commit()


_init_db()


def add_history(qr_type: str, data: str, file_name: str, label: str = None):
    """Insert a new history record for a generated QR code."""
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO history (qr_type, data, file_name, label, created_at, is_favorite)
            VALUES (?, ?, ?, ?, ?, 0)
            """,
            (qr_type, data, file_name, label, datetime.now().isoformat(timespec="seconds")),
        )
        conn.commit()


def get_history():
    """Return every history record, most recent first, as a list of dicts."""
    with _connect() as conn:
        rows = conn.execute("SELECT * FROM history ORDER BY created_at DESC").fetchall()
        return [dict(r) for r in rows]


def delete_record(record_id: int):
    with _connect() as conn:
        conn.execute("DELETE FROM history WHERE id = ?", (record_id,))
        conn.commit()


def delete_all():
    """Wipe every history record. Image files on disk are intentionally left alone."""
    with _connect() as conn:
        conn.execute("DELETE FROM history")
        conn.commit()


def toggle_favorite(record_id: int):
    with _connect() as conn:
        row = conn.execute(
            "SELECT is_favorite FROM history WHERE id = ?", (record_id,)
        ).fetchone()
        if row is None:
            return
        new_value = 0 if row["is_favorite"] else 1
        conn.execute(
            "UPDATE history SET is_favorite = ? WHERE id = ?", (new_value, record_id)
        )
        conn.commit()


def get_stats():
    """Aggregate stats used by the Analytics page."""
    with _connect() as conn:
        total = conn.execute("SELECT COUNT(*) AS c FROM history").fetchone()["c"]
        favorites = conn.execute(
            "SELECT COUNT(*) AS c FROM history WHERE is_favorite = 1"
        ).fetchone()["c"]
        by_type = conn.execute(
            "SELECT qr_type, COUNT(*) AS c FROM history GROUP BY qr_type ORDER BY c DESC"
        ).fetchall()
        by_day = conn.execute(
            """
            SELECT substr(created_at, 1, 10) AS day, COUNT(*) AS c
            FROM history GROUP BY day ORDER BY day
            """
        ).fetchall()

    return {
        "total": total,
        "favorites": favorites,
        "by_type": [dict(r) for r in by_type],
        "by_day": [dict(r) for r in by_day],
    }
