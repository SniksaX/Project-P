from fastapi import APIRouter, Depends, Request, HTTPException, status
from typing import List
from models.schemas import User, UserCreate
from services.user import UserStore
from pydantic import ValidationError
from core.dependencies import get_current_user, get_current_active_user
from core.limiter import limiter
from uuid import UUID

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[User])
@limiter.limit("10/minute")
def get_all_users_endpoint(request: Request, current_user: User = Depends(get_current_active_user)):
    return UserStore.get_all_users()


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
@limiter.limit("3/minute")
async def create_user(request: Request):
    try:
        user_create = UserCreate.model_validate(await request.json())
        return UserStore.add_user(user_create)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("2/minute")
def delete_user(request: Request, user_id: UUID, current_user: User = Depends(get_current_user)):
    try:
        UserStore.delete_user(user_id)
    except HTTPException as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail="User not found")
        raise


@router.get("/{user_id}", response_model=User)
@limiter.limit("2/minute")
def get_user(request: Request, user_id: UUID, current_user: User = Depends(get_current_user)):
    return UserStore.get_user_info(user_id)
