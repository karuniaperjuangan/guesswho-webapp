

from typing import Annotated
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from auth.auth import create_access_token, get_password_hash, verify_password
from database.mongo import authenticate_user, get_user_collection, get_current_user
from pymongo.collection import Collection
from models.user import User, UserCreate, Token
router= APIRouter()

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    collection: Annotated[dict, Depends(get_user_collection)]
) -> Token:
    user = authenticate_user(form_data.username, form_data.password,collection)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@router.post("/register", response_model=User)
async def register_user(user: UserCreate, collection: Annotated[Collection, Depends(get_user_collection)]):
    """
    Registers a new user in the database.

    Args:
        user (UserCreate): The user information to create.
        collection (Collection): The MongoDB collection where users are stored

    Raises:
        HTTPException: If the username is already registered.

    Returns:
        User: The created user.
    """
    db_user = collection.find_one({'username': user.username})
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    # Create a new user document
    new_user = {**user.model_dump(), "password": hashed_password}
    result = collection.insert_one(new_user)
    # Return the newly created user with hashed password
    return User(**new_user)

@router.get("/user", response_model=User)
def get_user(user: Annotated[User, Depends(get_current_user)]):
    return user