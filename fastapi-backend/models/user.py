from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str

class UserCreate(BaseModel):
    username: str
    password: str

class UserUpdatePassword(BaseModel):
    username: str
    old_password: str
    new_password: str