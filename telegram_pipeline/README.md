# telegram\_pipeline

This repository contains a [Dagster](https://dagster.io/) project, created using the [`dagster project scaffold`](https://docs.dagster.io/guides/build/projects/creating-a-new-project) command.

## Getting Started

1. Install the project as a Python package in editable mode so that changes in your local code are reflected immediately:

```
pip install -e ".[dev]"
```

2. Launch the Dagster development UI:

```
dagster dev
```

3. Visit [http://localhost:3000](http://localhost:3000) in your browser to explore the project.

You can begin defining assets in `telegram_pipeline/assets.py`. Any assets you create will be automatically loaded into the Dagster code location.

## Development Guide

### Adding Dependencies

Add additional Python dependencies by updating the `setup.py` file.

### Running Tests

Unit tests are located in the `telegram_pipeline_tests` directory. Run them with:

```
pytest telegram_pipeline_tests
```

### Using Schedules and Sensors

To use Dagster [Schedules](https://docs.dagster.io/guides/automate/schedules/) or [Sensors](https://docs.dagster.io/guides/automate/sensors/), ensure the [Dagster Daemon](https://docs.dagster.io/guides/deploy/execution/dagster-daemon) is running.
The daemon is started automatically when running `dagster dev`. Once active, you can enable schedules and sensors for your jobs.

## Deployment with Dagster+

The recommended way to deploy this project is via **Dagster+**.
Refer to the [Dagster+ documentation](https://docs.dagster.io/dagster-plus/) for deployment instructions.

---
