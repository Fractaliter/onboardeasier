from fastapi_users import schemas

class UserRead(schemas.BaseUser[int]):  # User schema for reading user data
    full_name: str | None = None

class UserCreate(schemas.BaseUserCreate):  # Schema for user creation
    full_name: str | None = None

class UserUpdate(schemas.BaseUserUpdate):  # Schema for user updates
    full_name: str | None = None
