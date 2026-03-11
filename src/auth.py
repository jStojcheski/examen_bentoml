import jwt
import logging
from datetime import datetime, timedelta, timezone
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Optional

from src.data_types import load_users_db, User

AUTH_SECRET_KEY = "69216c27822f6ac142b7a5a4d8ad4595b19f335a10671c0527a520bc6166ad78"
AUTH_ALGORITHM = "HS256"
USERS = load_users_db()


def authenticate_user(username: str, password: str) -> Optional[User]:
    for user in USERS:
        if username == user.name and password == user.password:
            logging.info(f"User with name >> {user.name} << found in the DB!")
            return user
    return None


def create_access_token(data: dict, is_admin: bool) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)
    if is_admin:
        expire += timedelta(hours=12)
    else:
        expire += timedelta(minutes=30)
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    return jwt.encode(to_encode, AUTH_SECRET_KEY, algorithm=AUTH_ALGORITHM)


class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.url.path.endswith("/predict"):
            token = request.headers.get("Authorization")
            if not token:
                return JSONResponse(status_code=401, content={"detail": "Missing authentication token"})
            try:
                token = token.split()[1]  # Bearer <token>
                payload = jwt.decode(token, AUTH_SECRET_KEY, algorithms=[AUTH_ALGORITHM])
            except jwt.ExpiredSignatureError:
                return JSONResponse(status_code=401, content={"detail": "Token has expired"})
            except jwt.InvalidTokenError:
                return JSONResponse(status_code=401, content={"detail": "Invalid token"})
            request.state.user = payload.get("sub")
        return await call_next(request)
