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

# Copy app files
COPY ./scripts /app/scripts
COPY ./pyproject.toml ./uv.lock ./alembic.ini /app/
COPY ./app /app/app

# Install project dependencies
RUN uv sync

# Run database migrations before starting the app
RUN alembic upgrade head

# **Use Gunicorn for production**
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8000"]
