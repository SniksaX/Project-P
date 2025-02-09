# src/classes/user_models.py
from pydantic import BaseModel
from uuid import uuid4, UUID
from collections import defaultdict
from typing import List

# Global in-memory storage for users
user_registry = defaultdict(dict)


class UserDetails(BaseModel):
    id: UUID = None
    username: str
    email: str
    password: str

    @classmethod
    def create_user(cls, username: str, email: str, password: str) -> 'UserDetails':
        for user in user_registry.values():
            if user.email == email:
                raise ValueError("User with this email already exists.")

        user_id = uuid4()
        user = cls(id=user_id, username=username,
                   email=email, password=password)
        user_registry[user_id] = user
        return user

    @classmethod
    def get_user(cls, user_id: UUID) -> 'UserDetails':
        user = user_registry.get(user_id)
        if not user:
            raise ValueError(f"userId: {user_id} not found")
        return user

    @classmethod
    def get_all_users(cls) -> List["UserDetails"]:
        return list(user_registry.values())

    @classmethod
    def delete_user(cls, user_id: UUID) -> str:
        if user_id in user_registry:
            del user_registry[user_id]
            return f"User {user_id} deleted successfully."
        raise ValueError(f"User {user_id} not found.")
