from dagster import Definitions, load_assets_from_modules
from telegram_pipeline import assets  # noqa: TID252
from telegram_pipeline.jobs import telegram_pipeline_job 

all_assets = load_assets_from_modules([assets])

defs = Definitions(
    assets=all_assets,
    jobs=[telegram_pipeline_job],
)
