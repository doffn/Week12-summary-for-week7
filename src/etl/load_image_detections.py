import psycopg2
import json
import os
from dotenv import load_dotenv
from pathlib import Path

def load_detections_to_postgres():
    BASE_DIR = Path(__file__).resolve().parent.parent.parent  
    load_dotenv(BASE_DIR / ".env")

    DB_CONFIG = {
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
    }

    DETECTIONS_FILE = BASE_DIR / "data" / "enriched" / "image_detections.json"
    if not DETECTIONS_FILE.exists():
        raise FileNotFoundError(f"Detections file not found: {DETECTIONS_FILE}")

    with open(DETECTIONS_FILE, "r", encoding="utf-8") as f:
        detections = json.load(f)

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS raw.image_detections (
            message_id BIGINT,
            image_path TEXT,
            object_class TEXT,
            confidence_score FLOAT,
            channel TEXT,
            date TEXT
        );
    """)

    for d in detections:
        cur.execute("""
            INSERT INTO raw.image_detections (
                message_id, image_path, object_class, confidence_score, channel, date
            )
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (
            d["message_id"],
            d["image_path"],
            d["object_class"],
            d["confidence_score"],
            d["channel"],
            d["date"]
        ))

    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Inserted {len(detections)} rows into raw.image_detections")

if __name__ == "__main__":
    load_detections_to_postgres()
    