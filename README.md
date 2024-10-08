# Gobble Cube - Setup and Testing

## Debugging Queries

To view detailed query logs, set the log level to debug:

- **Option 1:** Update your `.env` file with `GOBBLE_CUBE_LOG_LEVEL=DEBUG`.
- **Option 2:** Directly set the log level to debug in your configuration.

## Generating and Using CSV Files

Run the script in the root directory to generate the necessary CSV files required for the application.

```bash
poetry run python scripts/gen_fake_csv.py
```

This script will generate three CSV files that are essential for the application.

## Populating the Database

After generating the CSV files, use the csv files or use the provided script to populate the database with sample data.

```bash
poetry run python scripts/gen_fake_data.py
```

## Testing Features

Once the database is populated, use the application documentation to test various features and verify functionality.

## Additional Notes

- Feel Free to use the generated CSV or make tweaks in the values
- The generated CSV files can be uploaded to the respective routes in your application as needed.


## Poetry

This project uses poetry. It's a modern dependency management
tool.

To run the project use this set of commands:

```bash
poetry install
poetry run python -m gobble_cube
```

This will start the server on the configured host.

You can find swagger documentation at `/api/docs`.

You can read more about poetry here: https://python-poetry.org/

## Docker

You can start the project with docker using this command:

```bash
docker-compose up --build
```

If you want to develop in docker with autoreload and exposed ports add `-f deploy/docker-compose.dev.yml` to your docker command.
Like this:

```bash
docker-compose -f docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up --build
```

This command exposes the web application on port 8000, mounts current directory and enables autoreload.

But you have to rebuild image every time you modify `poetry.lock` or `pyproject.toml` with this command:

```bash
docker-compose build
```

## Project structure

```bash
$ tree "gobble_cube"
gobble_cube
├── conftest.py  # Fixtures for all tests.
├── db  # module contains db configurations
│   ├── dao  # Data Access Objects. Contains different classes to interact with database.
│   └── models  # Package contains different models for ORMs.
├── __main__.py  # Startup script. Starts uvicorn.
├── services  # Business Logic and Package for different external services such as rabbit or redis etc.
├── settings.py  # Main configuration settings for project.
├── static  # Static content.
├── tests  # Tests for project.
└── web  # Package contains web server. Handlers, startup config.
    ├── api  # Package with all handlers.
    │   └── views.py  # Main router.
    ├── application.py  # FastAPI application configuration.
    └── lifespan.py  # Contains actions to perform on startup and shutdown.
```

## Configuration

This application can be configured with environment variables.

You can create `.env` file in the root directory and place all
environment variables here. 

All environment variables should start with "GOBBLE_CUBE_" prefix.

For example if you see in your "gobble_cube/settings.py" a variable named like
`random_parameter`, you should provide the "GOBBLE_CUBE_RANDOM_PARAMETER" 
variable to configure the value. This behaviour can be changed by overriding `env_prefix` property
in `gobble_cube.settings.Settings.Config`.

An example of .env file:
```bash
GOBBLE_CUBE_RELOAD="True"
GOBBLE_CUBE_PORT="8000"
GOBBLE_CUBE_ENVIRONMENT="dev"
```

You can read more about BaseSettings class here: https://pydantic-docs.helpmanual.io/usage/settings/

## Pre-commit

To install pre-commit simply run inside the shell:
```bash
pre-commit install
```

pre-commit is very useful to check your code before publishing it.
It's configured using .pre-commit-config.yaml file.

By default it runs:
* black (formats your code);
* mypy (validates types);
* ruff (spots possible bugs);


You can read more about pre-commit here: https://pre-commit.com/


## Running tests

If you want to run it in docker, simply run:

```bash
docker-compose run --build --rm api pytest -vv .
docker-compose down
```

For running tests on your local machine.


2. Run the pytest.
```bash
pytest -vv .
```
