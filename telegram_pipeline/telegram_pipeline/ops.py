from dagster import op
from pathlib import Path
import sys, pathlib
ROOT_DIR = pathlib.Path(__file__).resolve().parents[2]
SRC_DIR = ROOT_DIR
sys.path.append(str(SRC_DIR))

from dagster import op, Out, Output
from src.scraping.scrape_telegram import scrape_telegram_channels
import subprocess
from src.enrichment.run_yolo import run_yolo_on_images
from src.etl.load_image_detections import load_detections_to_postgres
from src.etl.load_raw_to_postgres import load_json_to_postgres





@op(out=Out(list))
def scrape_telegram_data():
    channels = [
        "lobelia4cosmetics",
        "tikvahpharma",
        "chemed123"
    ]
    json_files = scrape_telegram_channels(channels, limit=50)
    yield Output(json_files, output_name="result")



@op
def load_raw_to_postgres():
    load_json_to_postgres(verbose=True)
    
@op
def run_dbt_transformations():

    project_dir = Path(__file__).resolve().parent.parent.parent / "dbt_project"
    
    result = subprocess.run(
        ["dbt", "run"],
        cwd=project_dir,
        check=True,
        capture_output=True,
        text=True
    )




@op
def run_yolo_enrichment():
    run_yolo_on_images()
    load_detections_to_postgres()
    
