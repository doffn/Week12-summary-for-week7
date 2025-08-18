import os
import json
import psycopg2
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional
from datetime import datetime


# --- Load env ---
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")


DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}

DEFAULT_DATA_DIR = BASE_DIR / "data/raw"


def load_json_to_postgres(data_dir: Optional[Path] = None, verbose: bool = True):
    data_dir = data_dir or DEFAULT_DATA_DIR

    if not data_dir.exists():
        raise FileNotFoundError(f"Raw data directory not found: {data_dir}")

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS raw.telegram_messages (
            id BIGINT PRIMARY KEY,
            date TIMESTAMP,
            sender_id TEXT,
            text TEXT,
            has_photo BOOLEAN,
            photo_path TEXT,
            channel TEXT
        );
    """)

    loaded_count = 0

    for day_dir in data_dir.iterdir():
        if not day_dir.is_dir():
            continue
        for channel_dir in day_dir.iterdir():
            if not channel_dir.is_dir():
                continue

            for file in channel_dir.glob("*_messages.json"):
                with open(file, "r", encoding="utf-8") as f:
                    messages = json.load(f)

                for msg in messages:
                    try:
                        cur.execute("""
                            INSERT INTO raw.telegram_messages (
                                id, date, sender_id, text, has_photo, photo_path, channel
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (id) DO NOTHING;
                        """, (
                            msg["id"],
                            msg["date"],
                            msg.get("sender_id"),
                            msg.get("text"),
                            msg.get("has_photo", False),
                            msg.get("photo_path"),
                            channel_dir.name
                        ))
                        loaded_count += 1
                    except Exception as e:
                        print(f"⚠️ Failed to insert message {msg['id']} from {file.name}: {e}")

                if verbose:
                    print(f"📁 Loaded {len(messages)} messages from {file.name}")

    conn.commit()
    cur.close()
    conn.close()

    print(f"\n✅ Inserted {loaded_count} messages into raw.telegram_messages")


# --- Optional CLI entry ---
if __name__ == "__main__":
    print("📥 Loading raw data into PostgreSQL...")
    load_json_to_postgres()
