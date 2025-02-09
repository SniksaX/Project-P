# src/routes/routes.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from uuid import UUID
from src.classes.user_models import UserDetails

router = APIRouter()


@router.get('/getUser/{user_id}', response_model=UserDetails)
async def get_user_endpoint(user_id: UUID):
    try:
        return UserDetails.get_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get('/getAllUsers', response_model=List[UserDetails])
async def get_all_users_endpoint():
    return UserDetails.get_all_users()


@router.post('/createUser', response_model=UserDetails)
async def create_user_endpoint(user_data: UserDetails):
    try:
        new_user = UserDetails.create_user(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password
        )
        return new_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete('/deleteUser/{user_id}')
async def delete_user_endpoint(user_id: UUID):
    try:
        message = UserDetails.delete_user(user_id)
        return JSONResponse(content={"message": message})
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
