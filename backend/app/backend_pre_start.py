import logging
import os
from sqlalchemy import Engine
from sqlmodel import Session, select
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.core.db import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1

# Print environment variables for debugging
def print_env_vars():
    logger.info("🔍 DEBUG: Checking environment variables")
    logger.info(f"🔹 DATABASE_URL: {os.getenv('DATABASE_URL')}")
    logger.info(f"🔹 POSTGRES_SERVER: {os.getenv('POSTGRES_SERVER')}")
    logger.info(f"🔹 POSTGRES_USER: {os.getenv('POSTGRES_USER')}")
    logger.info(f"🔹 POSTGRES_PASSWORD: {os.getenv('POSTGRES_PASSWORD')}")
    logger.info(f"🔹 POSTGRES_DB: {os.getenv('POSTGRES_DB')}")
    logger.info(f"🔹 POSTGRES_PORT: {os.getenv('POSTGRES_PORT')}")

@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init(db_engine: Engine) -> None:
    try:
        with Session(db_engine) as session:
            session.exec(select(1))  # Test if DB is up
    except Exception as e:
        logger.error(f"🚨 Database connection error: {e}")
        raise e

def main() -> None:
    logger.info("🚀 Initializing service...")
    print_env_vars()  # 🔥 Debug print environment variables
    init(engine)
    logger.info("✅ Service finished initializing!")

if __name__ == "__main__":
    main()
