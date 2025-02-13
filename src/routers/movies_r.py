from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from uuid import UUID
from typing import List, Dict, Any

from ..models.schemas import Movie, MovieCreate, User
from ..services.movie_s import MovieStore
from ..services.user import UserStore
from ..core.dependencies import get_current_user
from ..core.limiter import limiter
from ..services.tmdb_s import TMDBService

router = APIRouter(tags=["movies"])
tmdb_service = TMDBService()


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


@router.get("/movies/search")
@limiter.limit("10/minute")
async def search_movies(
    request: Request,
    query: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Search for movies using TMDB API
    """
    return await tmdb_service.search_movies(query, page)


@router.get("/movies/{movie_id}")
@limiter.limit("10/minute")
async def get_movie_details(
    request: Request,
    movie_id: int,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get detailed information about a specific movie
    """
    return await tmdb_service.get_movie_details(movie_id)


@router.post("/users/{user_id}/movies/{tmdb_movie_id}", response_model=Movie)
@limiter.limit("5/minute")
async def add_movie_to_collection(
    request: Request,
    user_id: UUID,
    tmdb_movie_id: int,
    current_user: User = Depends(get_current_user)
):
    """
    Add a movie from TMDB to user's personal collection
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to add movies for this user"
        )

    # Get movie details from TMDB
    movie_details = await tmdb_service.get_movie_details(tmdb_movie_id)

    # Convert TMDB movie to our MovieCreate format
    movie_create = MovieCreate(
        title=movie_details["title"],
        description=movie_details["overview"],
        # Convert from 0-10 to 0-100 scale
        rating=int(movie_details["vote_average"] * 10),
        release_date=movie_details["release_date"],
        tmdb_id=tmdb_movie_id  # We'll add this field to store TMDB reference
    )

    # Save to database
    return MovieStore.add_movie(movie_create, user_id)


@router.get("/users/{user_id}/movies", response_model=List[Movie])
@limiter.limit("5/minute")
async def get_user_movie_collection(
    request: Request,
    user_id: UUID,
    current_user: User = Depends(get_current_user)
):
    """
    Get all movies in user's personal collection
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to view movies for this user"
        )
    return MovieStore.get_movie_list(user_id)
