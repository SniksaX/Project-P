from uuid import UUID, uuid4
from typing import Optional, List
from fastapi import HTTPException, status
import psycopg2
from psycopg2 import sql

from ..core.database import DatabaseManager
from ..models.schemas import UserCreate, User, UserInDB
from ..core.security import get_password_hash, verify_password
from ..services.email_s import EmailService


class UserStore:
    @classmethod
    async def add_user(cls, user_create: UserCreate) -> User:
        hashed_password = get_password_hash(user_create.password)
        verification_token = str(uuid4())
        new_user = User(
            **user_create.model_dump(),
            is_verified=False,
            verification_token=verification_token
        )

        query = sql.SQL("""
            INSERT INTO userinfo.users (name, email, password, id, is_verified, verification_token)
            VALUES (%s, %s, %s, %s, %s, %s)
        """)
        params = (
            new_user.name,
            new_user.email,
            hashed_password,
            str(new_user.id),
            False,
            verification_token
        )

        try:
            DatabaseManager.execute_query(query, params)
            # Send verification email
            await EmailService.send_verification_email(new_user.email, verification_token)
            return new_user
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

    @classmethod
    def verify_email(cls, token: str) -> bool:
        query = sql.SQL("""
            UPDATE userinfo.users 
            SET is_verified = true, verification_token = NULL 
            WHERE verification_token = %s 
            RETURNING id
        """)
        result = DatabaseManager.execute_query(query, (token,), fetch=True)
        return bool(result)

    @classmethod
    def authenticate_user(cls, email: str, password: str):
        user = cls.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        if not user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Please verify your email before logging in"
            )
        return user
