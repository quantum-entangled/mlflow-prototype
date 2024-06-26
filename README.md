This repository provides a simple Docker configuration for running the MLflow Tracking Server. It uses PostgreSQL as the metadata backend and a local directory for artifact storage.

## Set Up MLflow via Docker

1. Install Docker for your system: [Docker Installation](https://docs.docker.com/engine/install/).
2. Clone the repository to your local machine. Navigate to the project directory using the terminal or command prompt.
3. Run `docker compose build --no-cache` the first time you run the project or if you want to completely rebuild it. Setting up the containers might take a while.
4. Every time you want to start the containers, run `docker compose up` or use Docker Desktop. The startup of all services might take a while. The MLflow tracking server and UI will run at the host and port specified by your `.env` file (defaults to `localhost:8080`).
5. To stop the containers, run `docker compose stop` in a separate terminal; press `Ctrl+C` in the terminal you started it from; or use Docker Desktop.

You may want to create your own `.env` file in the project directory with all the required variables for the containers to run. The following snippet shows an example of the file's content with all the necessary variables:

```text
POSTGRES_USER=mlflow-user
POSTGRES_PASSWORD=mlflow-password
POSTGRES_DB=mlflow-metadata
POSTGRES_PORT=5432
POSTGRES_DATA_PATH=postgresql/data
MLFLOW_HOST=0.0.0.0
MLFLOW_PORT=8080
MLFLOW_ARTIFACTS_DESTINATION=artifacts
MLFLOW_APP_PATH=/code
MLFLOW_VENV_NAME=.venv
```

Otherwise, you can rely on the default values.

## Set Up the Environment to Run the Examples

1. Install Python for your system: [Official Website](https://www.python.org/downloads/).
2. Ensure that you are in the project directory and Python is on your `PATH`.
3. Run `python -m venv .venv` to create the virtual environment.
4. Activate the virtual environment by running either `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` / `. .venv/bin/activate` (Unix-like).
5. Run `pip install -r requirements.txt` to install the dependencies.
6. Execute scripts in the `examples` folder and track the results on your MLflow server.

## Notes

Docker will mount your local directory folders to the ones inside the containers for backend metadata and artifact storage. This means that any changes made on your side or inside the container will immediately show up on the other side without any overhead to transfer these files. The default mount folders on the local side are `postgresql` and `artifacts`.

While executing the project, additional folders might be created in the default setup, including `mlruns` for MLflow runs metadata and `checkpoints` for saved models during TensorFlow training.
