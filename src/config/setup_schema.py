import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}

CREATE_SQL = """
CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.telegram_messages (
    id BIGINT PRIMARY KEY,
    date TIMESTAMP,
    sender_id TEXT,
    text TEXT,
    has_photo BOOLEAN,
    photo_path TEXT,
    channel TEXT
);
"""

def setup_schema():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(CREATE_SQL)
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Schema and table created successfully.")

if __name__ == "__main__":
    setup_schema()
