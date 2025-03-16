import logging
import os
from sqlalchemy import Engine
from sqlmodel import Session, select
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.core.db import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60  # 5 minutes
wait_seconds = 2

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
    init(engine)
    logger.info("✅ Service finished initializing!")

if __name__ == "__main__":
    main()
