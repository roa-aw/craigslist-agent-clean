import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "inventory.db")


def get_conn() -> sqlite3.Connection:
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(
            f"Database not found at {DB_PATH}.\n"
            "Run:  python -m db.setup   (after placing vehicles.csv in data/)"
        )
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn