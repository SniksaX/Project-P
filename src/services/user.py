from uuid import UUID
from typing import Optional, List
from core.database import DatabaseManager
from models.schemas import UserCreate, User, UserInDB
from core.security import get_password_hash, verify_password
from fastapi import HTTPException, status
import psycopg2
from psycopg2 import sql


class UserStore:
    @classmethod
    def add_user(cls, user_create: UserCreate) -> User:
        hashed_password = get_password_hash(user_create.password)
        new_user = User(**user_create.model_dump())
        query = sql.SQL("""
            INSERT INTO userinfo.users (name, email, password, id)
            VALUES (%s, %s, %s, %s)
        """)
        params = (new_user.name, new_user.email,
                  hashed_password, str(new_user.id))
        try:
            DatabaseManager.execute_query(query, params)
        except psycopg2.IntegrityError as e:
            if e.pgcode == '23505' and e.diag.constraint_name == 'users_email_key':
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User with this email already exists"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Database integrity error"
                )
        except psycopg2.Error as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed"
            )
        return new_user

    @classmethod
    def get_user_info(cls, user_id: UUID) -> User:
        query = sql.SQL(
            "SELECT name, email, id FROM userinfo.users WHERE id = %s")
        params = (str(user_id),)
        result = DatabaseManager.execute_query(query, params, fetch=True)
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        name, email, user_id = result[0]
        return User(id=UUID(user_id), name=name, email=email)

    @classmethod
    def get_user_by_email(cls, email: str) -> Optional[UserInDB]:
        query = sql.SQL(
            "SELECT name, email, id, password FROM userinfo.users WHERE email = %s")
        params = (email,)
        result = DatabaseManager.execute_query(query, params, fetch=True)
        if not result:
            return None
        name, email, user_id, hashed_password = result[0]
        return UserInDB(id=UUID(user_id), name=name, email=email, hashed_password=hashed_password)

    @classmethod
    def get_all_users(cls) -> List[User]:
        query = sql.SQL("SELECT name, email, id FROM userinfo.users")
        results = DatabaseManager.execute_query(query, fetch=True)
        return [User(id=UUID(user_id), name=name, email=email) for name, email, user_id in results]

    @classmethod
    def delete_user(cls, user_id: UUID) -> None:
        query = sql.SQL("DELETE FROM userinfo.users WHERE id = %s")
        params = (str(user_id),)
        DatabaseManager.execute_query(query, params)
