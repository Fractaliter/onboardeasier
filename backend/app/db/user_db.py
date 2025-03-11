from fastapi_users.db import SQLAlchemyUserDatabase
from app.db.database import SessionLocal
from app.models.user import User

# User database adapter for FastAPI Users
def get_user_db():
    db = SessionLocal()
    try:
        yield SQLAlchemyUserDatabase(db, User)
    finally:
        db.close()
