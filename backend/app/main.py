from fastapi import FastAPI
from app.core.user_manager import fastapi_users, auth_backend
from app.schemas.user import UserRead, UserCreate, UserUpdate
from app.api.api_router import router as api_router

app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"]
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"]
)

app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "Welcome to the Onboarding API"}