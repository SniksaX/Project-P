from fastapi import Depends, HTTPException, status
from jose import JWTError
from uuid import UUID
from core.security import oauth2_scheme
from core.config import settings
from models.schemas import TokenData, User
from services.user import UserStore
from jose import jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        user_id = UUID(user_id_str)
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    user = UserStore.get_user_info(token_data.user_id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user
