import os
import sqlite3
from pathlib import Path

# Create DB directory relative to this file so it works regardless of CWD
BASE_DIR = Path(__file__).resolve().parents[3]  # .../models/tools/agents/services/database -> repo root
DB_DIR = BASE_DIR / "database"
DB_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DB_DIR / "farmer.db"

conn = sqlite3.connect(
    str(DB_PATH),
    check_same_thread=False,
)

cur = conn.cursor()

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS chats(
        id INTEGER PRIMARY KEY,
        question TEXT,
        answer TEXT
    )
    """
)

conn.commit()

