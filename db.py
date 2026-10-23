
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "cricbuzz.db"


def get_connection():
    """Connect to the project database."""
    return sqlite3.connect(DB_PATH)
