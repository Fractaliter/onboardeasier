from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, String, Boolean
from app.db.database import Base

class User(SQLAlchemyBaseUserTable[int], Base):  # Explicitly specify ID type
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  # Ensure ID is defined as PK
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
