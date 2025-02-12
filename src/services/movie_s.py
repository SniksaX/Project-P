from uuid import UUID, uuid4
from datetime import datetime
from typing import List
from fastapi import HTTPException, status
import psycopg2
from psycopg2 import sql

from ..core.database import DatabaseManager
from ..models.schemas import MovieCreate, Movie


class MovieStore:
    @classmethod
    def add_movie(cls, movie_create: MovieCreate, user_id: UUID) -> Movie:
        new_movie = Movie(**movie_create.model_dump(),
                          user_id=user_id, id=uuid4(), created_at=datetime.now())
        query = sql.SQL("""
            INSERT INTO userinfo.movies (id, title, description, rating, release_date, user_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """)
        params = (
            str(new_movie.id),
            new_movie.title,
            new_movie.description,
            new_movie.rating,
            new_movie.release_date,
            str(user_id)
        )
        try:
            DatabaseManager.execute_query(query, params)
        except psycopg2.Error as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to add movie to database"
            )
        return new_movie

    @classmethod
    def get_movie_list(cls, user_id: UUID) -> List[Movie]:
        query = sql.SQL("""
            SELECT id, title, description, rating, release_date, user_id, created_at
            FROM userinfo.movies
            WHERE user_id = %s
        """)
        params = (str(user_id),)
        results = DatabaseManager.execute_query(query, params, fetch=True)
        return [
            Movie(
                id=UUID(result[0]),
                title=result[1],
                description=result[2],
                rating=result[3],
                release_date=result[4],
                user_id=UUID(result[5]),
                created_at=result[6]
            ) for result in results
        ]
