import sqlite3
from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database location
DB_PATH = BASE_DIR / "customer_support.db"


def get_connection():

    connection = sqlite3.connect(DB_PATH)

    connection.row_factory = sqlite3.Row

    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def initialize_database():

    schema_path = BASE_DIR / "database" / "schema.sql"

    with get_connection() as connection:

        schema = schema_path.read_text(encoding="utf-8")

        connection.executescript(schema)

    print("SQLite database initialized successfully.")
    print(f"Database location: {DB_PATH}")


if __name__ == "__main__":
    initialize_database()