# Stage 1: Set up the common environment
FROM python:3.12-slim AS env

ARG MLFLOW_APP_PATH \
    MLFLOW_VENV_NAME \
    USERNAME=mlflow-user \
    USER_UID=1000 \
    USER_GID=1000

# Add a non-root user with permissions to a working directory
RUN groupadd --gid ${USER_GID} -r ${USERNAME} && \
    useradd --gid ${USER_GID} --uid ${USER_UID} -l -r ${USERNAME} && \
    mkdir -p ${MLFLOW_APP_PATH} && \
    chown -R ${USERNAME}:${USER_GID} ${MLFLOW_APP_PATH}


# Stage 2: Install all the packages
FROM env AS build

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=0 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR ${MLFLOW_APP_PATH}

COPY requirements-docker.txt ${MLFLOW_APP_PATH}

RUN apt-get update && \
    apt-get upgrade -y && \
    python -m venv ${MLFLOW_VENV_NAME} && \
    . ${MLFLOW_VENV_NAME}/bin/activate && \
    python -m pip install --upgrade pip setuptools && \
    pip install -r requirements-docker.txt && \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*


# Stage 3: Run the MLflow server
FROM env AS runtime

USER ${USERNAME}

ENV PATH=${MLFLOW_APP_PATH}/${MLFLOW_VENV_NAME}/bin:${PATH}

WORKDIR ${MLFLOW_APP_PATH}

# Copy the virtual environment from the build stage
COPY --from=build ${MLFLOW_APP_PATH}/${MLFLOW_VENV_NAME} ${MLFLOW_VENV_NAME}

EXPOSE ${MLFLOW_PORT}

CMD [ "mlflow", "server" ]
