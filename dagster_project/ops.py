import os
import subprocess
from dagster import op, Out, In, Nothing

# Base directories inside the container
SCRIPTS_DIR = "/app/scripts"
DBT_PROJECT_DIR = "/app/dbt_project"
FASTAPI_APP_DIR = "/app/fastapi_app"


def run_subprocess(command: list, success_msg: str, error_msg: str):
    """Helper function to run subprocess commands with error handling."""
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        if result.stdout:
            print(f"{success_msg} output:\n{result.stdout}")
        if result.stderr:
            print(f"{success_msg} errors:\n{result.stderr}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"{error_msg}: {e.stderr}")


@op(out=Out(Nothing))
def scrape_telegram_data_op():
    """Scrape Telegram data."""
    print("Executing Telegram data scraping...")
    run_subprocess(
        ["python", os.path.join(SCRIPTS_DIR, "telegram_scraper.py")],
        success_msg="Telegram scraping",
        error_msg="Telegram scraping failed"
    )
    print("Telegram data scraping completed.")


@op(out=Out(Nothing), ins={"start": In(Nothing)})
def load_raw_to_postgres_op():
    """Load raw JSON data into PostgreSQL."""
    print("Loading raw data into PostgreSQL...")
    run_subprocess(
        ["python", os.path.join(SCRIPTS_DIR, "load_raw_to_postgres.py")],
        success_msg="Raw data loading",
        error_msg="Raw data loading failed"
    )
    print("Raw data loading completed.")


@op(out=Out(Nothing), ins={"start": In(Nothing)})
def run_dbt_transformations_op():
    """Run dbt transformations."""
    print("Running dbt transformations...")
    run_subprocess(
        ["dbt", "build", "--project-dir", DBT_PROJECT_DIR],
        success_msg="dbt transformations",
        error_msg="dbt transformations failed"
    )
    print("dbt transformations completed.")


@op(out=Out(Nothing), ins={"start": In(Nothing)})
def run_yolo_enrichment_op():
    """Run YOLOv8 for data enrichment."""
    print("Executing YOLOv8 enrichment...")
    run_subprocess(
        ["python", os.path.join(SCRIPTS_DIR, "yolo_enrichment.py")],
        success_msg="YOLO enrichment",
        error_msg="YOLO enrichment failed"
    )
    print("YOLOv8 enrichment completed.")


@op(out=Out(Nothing), ins={"start": In(Nothing)})
def start_fastapi_op():
    """
    Start the FastAPI application.
    Note: In production, FastAPI should run as a standalone service, not a Dagster op.
    """
    print("Starting FastAPI application...")
    try:
        command = f"uvicorn {FASTAPI_APP_DIR.replace('/app/', '')}.main:app --host 0.0.0.0 --port 8000"
        print(f"To run FastAPI, execute:\n{command}")
        # Uncomment to run directly (blocking):
        # subprocess.run(command.split(), check=True)
    except Exception as e:
        raise RuntimeError(f"Failed to start FastAPI: {e}")
    print("FastAPI application command displayed.")
