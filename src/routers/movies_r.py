from fastapi import APIRouter, Depends, HTTPException, status, Request
from uuid import UUID
from typing import List

from ..models.schemas import Movie, MovieCreate
from ..services.movie_s import MovieStore
from ..services.user import UserStore, User
from ..core.dependencies import get_current_user
from ..core.limiter import limiter

router = APIRouter(prefix="/users/{user_id}/movies", tags=["movies"])


@router.post("/", response_model=Movie, status_code=status.HTTP_201_CREATED)
@limiter.limit("3/minute")
def create_movie_for_user(request: Request, user_id: UUID, movie_create: MovieCreate, current_user: User = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to create movies for this user.")
    try:
        UserStore.get_user_info(user_id)
        return MovieStore.add_movie(movie_create, user_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Could not create movie")


@router.get("/", response_model=List[Movie])
@limiter.limit("5/minute")
def get_movies_for_user(request: Request, user_id: UUID, current_user: User = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to view movies for this user.")
    return MovieStore.get_movie_list(user_id)
