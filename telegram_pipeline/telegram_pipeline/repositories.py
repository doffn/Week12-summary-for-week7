from dagster import repository
from .jobs import telegram_pipeline_job

@repository
def telegram_repo():
    return [telegram_pipeline_job]