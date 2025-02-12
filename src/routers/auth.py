from fastapi import APIRouter, Body, HTTPException, status
from datetime import timedelta

from ..models.schemas import Token, TokenRequest, User, UserCreate
from ..core.security import verify_password
from ..core.security import create_access_token
from ..services.user import UserStore
from ..core.limiter import limiter

router = APIRouter(tags=["auth"])


@router.post("/token", response_model=Token)
async def login_for_access_token(token_request: TokenRequest = Body(...)):
    user_in_db = UserStore.get_user_by_email(token_request.email)
    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(token_request.password, user_in_db.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user_in_db.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/verify-email")
async def verify_email(token: str):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token"
        )

    verified = UserStore.verify_email(token)
    if not verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )

    return {"message": "Email verified successfully!"}


@router.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    return await UserStore.add_user(user)
