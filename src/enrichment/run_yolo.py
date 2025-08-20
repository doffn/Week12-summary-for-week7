import os
import json
from ultralytics import YOLO
from pathlib import Path
from dotenv import load_dotenv



def run_yolo_on_images():
    load_dotenv()


    BASE_DIR = Path(__file__).resolve().parent.parent.parent 
    RAW_DIR = BASE_DIR / "data" / "raw"
    OUTPUT_JSON = BASE_DIR / "data" / "enriched" / "image_detections.json"
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)

    model = YOLO("yolov8n.pt")  # small model

    detections = []
    RELEVANT_CLASSES = {
        "bottle", "toothbrush", "toothpaste", "scissors", "handbag", "laptop", "book", "cup", "remote",
        "perfume", "lotion", "cream", "mirror", "cell phone", "soap", "cosmetics", "syringe", "pill"
    }

    for date_dir in RAW_DIR.iterdir():
        if not date_dir.is_dir():
            continue

        for channel_dir in date_dir.iterdir():
            if not channel_dir.is_dir():
                continue

            for img_file in channel_dir.glob("*.jpg"):
                results = model(img_file, verbose=False)[0]

                for box in results.boxes:
                    class_id = int(box.cls)
                    object_name = model.names[class_id]

                    if object_name not in RELEVANT_CLASSES:
                        continue  # Skip irrelevant objects like person, mouse, car

                    detection = {
                        "message_id": int(img_file.stem.split("_")[0]),
                        "image_path": str(img_file),
                        "object_class": object_name,
                        "confidence_score": round(float(box.conf), 4),
                        "channel": channel_dir.name,
                        "date": date_dir.name
                    }
                    detections.append(detection)
                    


    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(detections, f, indent=2)

    print(f"✅ Saved {len(detections)} detections to {OUTPUT_JSON}")

if __name__ == "__main__":
    run_yolo_on_images()