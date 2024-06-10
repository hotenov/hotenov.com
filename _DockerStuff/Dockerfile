# syntax=docker.io/docker/dockerfile:1.5.0

# pull official base image
FROM python:3.12.4-alpine AS base

# Global settings
# ****************

# set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONUSERBASE=/opt/py_user_base

# for pip
ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100

# for poetry and pipx
ENV POETRY_HOME=/opt/poetry_data_dir \
    POETRY_CACHE_DIR=/opt/poetry_cache \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=0 \
    \
    PIPX_BIN_DIR=/opt/pipx_bin

# paths to bin and venv
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$PYTHONUSERBASE/bin:$PATH"
ENV PATH="$PIPX_BIN_DIR:$PATH"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# ****************

WORKDIR /usr/src/app


FROM base AS builder

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# upgrade pip
RUN pip install --upgrade pip

# install pipx and poetry
RUN python -m pip install --user pipx

# Install poetry with specified version
ARG POETRY_VER
ENV POETRY_VER=${POETRY_VER:-1.7.0}
RUN pipx install poetry==$POETRY_VER

# install venv (and it will be activated)
RUN python -m venv $VIRTUAL_ENV

COPY --from=project_root pyproject.toml poetry.lock ./

ARG POETRY_DEPS_TO_INSTALL
ENV POETRY_DEPS_TO_INSTALL=${POETRY_DEPS_TO_INSTALL:-"--only main"}
# install dependencies (except project itself and path dependencies)
# to avoid cache busting during 'src' modifications or in path dependencies
# See: https://python-poetry.org/docs/faq/
RUN poetry install --no-root --no-directory $POETRY_DEPS_TO_INSTALL

# copy project (from Dockerfile context 'src' to WORKDIR '/usr/src/app')
COPY --from=src . .

# install your project itself
# Pay attention that '--only-root'
# You should also install all your path (directory) dependencies groups if you use them
RUN poetry install --only-root


FROM base as final

COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV

# copy project
COPY --from=src . .

# copy entrypoint.sh
COPY entrypoint.sh /usr/local/bin/
RUN sed -i 's/\r$//g' /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Expose port between containers
ARG WEB_PORT
ENV WEB_PORT=${WEB_PORT:-8833}
EXPOSE $WEB_PORT

# run entrypoint.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
