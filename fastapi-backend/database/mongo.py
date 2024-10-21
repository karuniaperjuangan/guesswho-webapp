from datetime import datetime, timedelta, timezone
from pymongo import MongoClient
from pymongo.collection import Collection
import dotenv
import os
import jwt
from passlib.context import CryptContext
from models.user import UserCreate, User
from typing import Annotated
from fastapi import Depends
from auth.auth import *
from jwt.exceptions import InvalidTokenError
import dotenv

dotenv.load_dotenv()

def get_user_colection():
    # Connect to MongoDB
    client = MongoClient(os.getenv('MONGO_URI'))

    db = client['guesswho']

    return db['users']

async def register_user(user: UserCreate, user_collection: Annotated[Collection, Depends(get_user_colection)]):
    """
    Registers a new user in the database.

    Args:
        user (UserCreate): The user information to create.

    Raises:
        HTTPException: If the username is already registered.

    Returns:
        User: The newly created user with hashed password.
    """
    user_dict = user.model_dump()
    user_dict['password'] = pwd_context.hash(user_dict['password'])
    user_collection.insert_one(user_dict)
    return User(**user_dict)

def authenticate_user(username: str, password: str, user_collection: Annotated[Collection, Depends(get_user_colection)]):
    """
    Authenticates a user in the database.

    Args:
        username (str): The username to authenticate.
        password (str): The password to authenticate.

    Raises:
        HTTPException: If the username or password is incorrect.

    Returns:
        User: The authenticated user.
    """
    user = user_collection.find_one({'username': username})
    if not user:
        return False
    if not verify_password(password, user['password']):
        return False
    return User(**user)

async def get_current_user(token:  Annotated[str, Depends(oauth2_scheme)], user_collection: Annotated[Collection, Depends(get_user_colection)]):
    """
    Authenticates a user in the database.

    Args:
        token (str): The token to authenticate.

    Raises:
        HTTPException: If the token is invalid.

    Returns:
        User: The authenticated user.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return False
        user = user_collection.find_one({'username': username})
        if user is None:
            return False
        return User(**user)
    except InvalidTokenError:
        return False
