from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserResponse(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    is_active: bool

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
