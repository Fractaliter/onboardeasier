# Use a stable Python image
FROM python:3.12.4

# Ensure output is flushed immediately
ENV PYTHONUNBUFFERED=1 

# Set the working directory
WORKDIR /app/

# Install required system utilities
RUN apt-get update && apt-get install -y netcat-openbsd

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

# Set path
ENV PATH="/app/.venv/bin:$PATH"

# Install dependencies **without cache**
COPY uv.lock pyproject.toml /app/
RUN uv sync --frozen --no-install-project

# Set Python path
ENV PYTHONPATH=/app

# ✅ **Use ARG for build-time variables**
ARG DATABASE_URL
ARG POSTGRES_SERVER
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_DB
ARG POSTGRES_PORT
ARG FIRST_SUPERUSER
ARG FIRST_SUPERUSER_PASSWORD
ARG SECRET_KEY
ARG PROJECT_NAME

# ✅ **Set ENV variables correctly for runtime**
ENV DATABASE_URL=${DATABASE_URL}
ENV POSTGRES_SERVER=${POSTGRES_SERVER}
ENV POSTGRES_USER=${POSTGRES_USER}
ENV POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
ENV POSTGRES_DB=${POSTGRES_DB}
ENV POSTGRES_PORT=${POSTGRES_PORT}
ENV FIRST_SUPERUSER=${FIRST_SUPERUSER}
ENV FIRST_SUPERUSER_PASSWORD=${FIRST_SUPERUSER_PASSWORD}
ENV SECRET_KEY=${SECRET_KEY}
ENV PROJECT_NAME=${PROJECT_NAME}

# ✅ **Copy app files AFTER defining env variables**
COPY ./scripts /app/scripts
COPY ./pyproject.toml ./uv.lock ./alembic.ini /app/
COPY ./app /app/app

# ✅ **Run `uv sync` to install dependencies**
RUN uv sync


# ✅ **Use Gunicorn for production**
CMD ["gunicorn", "-w", "2", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8000"]
