import httpx
from fastapi import HTTPException
from typing import List, Dict, Any
from ..core.config import settings


class TMDBService:
    BASE_URL = "https://api.themoviedb.org/3"

    def __init__(self):
        self.api_key = settings.TMDB_API_KEY
        self.headers = {
            "Authorization": f"Bearer {settings.TMDB_API_KEY_V4}",
            "accept": "application/json"
        }

    async def search_movies(self, query: str, page: int = 1) -> Dict[str, Any]:
        """Search for movies using TMDB API"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.BASE_URL}/search/movie",
                    params={"query": query, "page": page},
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to fetch movies from TMDB: {str(e)}"
                )

    async def get_movie_details(self, movie_id: int) -> Dict[str, Any]:
        """Get detailed information about a specific movie"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.BASE_URL}/movie/{movie_id}",
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to fetch movie details from TMDB: {str(e)}"
                )
