from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import settings
from src.db.main import get_session
from src.db.models import User
from .schemas import TokenData

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

class AuthService:
    """
    Service class handling authentication, password hashing, 
    and JWT token operations.
    """

    def __init__(self, session: AsyncSession):
        """Initializes the service with a database session."""
        self.session = session

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifies a plain text password against a hashed password."""
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception:
            return False

    def get_password_hash(self, password: str) -> str:
        """Generates a bcrypt hash of the given password."""
        return pwd_context.hash(password)

    async def get_user_by_username(self, username: str) -> User | None:
        """Retrieves a user from the database by their username."""
        statement = select(User).where(User.username == username)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def authenticate_user(self, username: str, password: str) -> User | bool:
        """
        Authenticates a user by checking their username and password.
        Returns the user object if successful, False otherwise.
        """
        user = await self.get_user_by_username(username)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        """
        Creates a JWT access token with an optional expiration time.
        The 'sub' (subject) in data typically contains the username.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_session)
) -> User:
    """
    Dependency that retrieves the current authenticated user from the JWT token.
    Raises 401 Unauthorized if the token is invalid or the user doesn't exist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    
    auth_service = AuthService(session)
    user = await auth_service.get_user_by_username(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """
    Dependency that checks if the current user is active.
    Raises 400 Bad Request if the user is inactive.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
