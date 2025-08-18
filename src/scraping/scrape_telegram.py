import os
import json
from datetime import datetime
from pathlib import Path
from typing import List
from telethon.sync import TelegramClient
from dotenv import load_dotenv


def scrape_telegram_channels(channels: List[str], limit: int = 50) -> List[Path]:
    """
    Scrape messages and images from a list of Telegram channels.

    Args:
        channels (List[str]): Telegram usernames.
        limit (int): Max number of messages per channel.

    Returns:
        List[Path]: List of paths to JSON files created.
    """
    load_dotenv(".env")

    api_id = os.getenv("TG_API_ID")
    api_hash = os.getenv("TG_API_HASH")
    session_file_path = os.getenv("SESSION_FILE_PATH")

    if not all([api_id, api_hash, session_file_path]):
        raise EnvironmentError("Missing one of TG_API_ID, TG_API_HASH, or SESSION_FILE_PATH")

    session_path = Path(session_file_path).resolve()
    if not session_path.exists() or not session_path.is_file():
        raise FileNotFoundError(f"Invalid session file: {session_path}")

    session_name = session_path.stem
    raw_data_dir = Path("data/raw")
    today = datetime.today().strftime("%Y-%m-%d")
    saved_files = []

    with TelegramClient(str(session_path), api_id, api_hash) as client:
        for channel in channels:
            print(f"📡 Scraping {channel}...")

            messages = client.iter_messages(channel, limit=limit)
            channel_dir = raw_data_dir / today / channel
            channel_dir.mkdir(parents=True, exist_ok=True)

            collected = []

            for i, message in enumerate(messages, start=1):
                msg_data = {
                    "id": message.id,
                    "date": str(message.date),
                    "text": message.text,
                    "sender_id": str(message.sender_id),
                    "has_photo": bool(message.photo),
                }

                if message.photo:
                    file_path = channel_dir / f"{message.id}.jpg"
                    client.download_media(message, file=str(file_path))
                    msg_data["photo_path"] = str(file_path)
                    print(f"[{i}] 🖼️ Saved: {file_path.name}")

                if message.text:
                    print(f"[{i}] 📝 {message.text[:50]}...")

                collected.append(msg_data)

            json_file = channel_dir / f"{channel}_messages.json"
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(collected, f, ensure_ascii=False, indent=2)

            print(f"✅ {len(collected)} messages saved to: {json_file}")
            saved_files.append(json_file)

    return saved_files


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--channel", nargs="+", required=True)
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()

    scrape_telegram_channels(args.channel, limit=args.limit)