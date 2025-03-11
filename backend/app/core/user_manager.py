from fastapi_users import FastAPIUsers, BaseUserManager, UUIDIDMixin
from app.db.user_db import get_user_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.core.auth import auth_backend  # Use new authentication system

class UserManager(UUIDIDMixin, BaseUserManager[User, int]):
    user_db_model = User

async def get_user_manager(user_db=next(get_user_db())):
    yield UserManager(user_db)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],  # Use new authentication backend
)
