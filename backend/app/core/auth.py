import os
from dotenv import load_dotenv
from fastapi_users.authentication import BearerTransport, AuthenticationBackend, JWTStrategy

# Load environment variables
load_dotenv()

SECRET = os.getenv("SECRET_KEY", "defaultsecret")
JWT_LIFETIME = int(os.getenv("JWT_LIFETIME_SECONDS", "3600"))

# Define JWT Strategy
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=JWT_LIFETIME)

# Use Bearer token authentication
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
