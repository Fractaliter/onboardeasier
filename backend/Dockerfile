
FROM python:3.12.4
 
 ENV PYTHONUNBUFFERED=1
 
 WORKDIR /app/
 
 # Install uv
 COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/
 
 # Set path
 ENV PATH="/app/.venv/bin:$PATH"
 
 # Install dependencies **(without cache)**
 COPY uv.lock pyproject.toml /app/
 RUN uv sync --frozen --no-install-project
# Set Python path
ENV PYTHONPATH=/app
# Set up environment variables explicitly for build stage
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

# Expose these env variables inside the container
ENV DATABASE_URL=$DATABASE_URL
ENV POSTGRES_SERVER=$POSTGRES_SERVER
ENV POSTGRES_USER=$POSTGRES_USER
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD
ENV POSTGRES_DB=$POSTGRES_DB
ENV FIRST_SUPERUSER=$FIRST_SUPERUSER
ENV POSTGRES_PORT=$POSTGRES_PORT
ENV FIRST_SUPERUSER_PASSWORD=$FIRST_SUPERUSER_PASSWORD
ENV SECRET_KEY=$SECRET_KEY
ENV PROJECT_NAME=$PROJECT_NAME

# Copy app files
COPY ./scripts /app/scripts
COPY ./pyproject.toml ./uv.lock ./alembic.ini /app/
COPY ./app /app/app
# Copy test script
COPY ./scripts/test_db_connection.py /app/

# Run database connection test before migrations
RUN python /app/test_db_connection.py

# Install project dependencies
RUN uv sync

# Run database migrations before starting the app
RUN sleep 5 && alembic upgrade head

# **Use Gunicorn for production**
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8000"]