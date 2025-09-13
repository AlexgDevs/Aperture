from os import getenv
from functools import wraps
from dotenv import load_dotenv

from datetime import (
    datetime,
    timezone,
    timedelta
)

from fastapi import (
    Response,
    Request
)

from . import (
    jwt,
    JWTError,
    Depends,
    OAuth2PasswordBearer,
    HTTPException,
    status
)

load_dotenv()

ACCESS_EXPIRE = getenv('ACCESS_EXPIRE', 1)
REFRESH_EXPIRE = getenv('REFRESH_EXPIRE', 7)
ALGORITHM = getenv('ALGORITHM', 'HS256')
JWT_SECRET_KEY = getenv('JWT_SECRET_KEY')


outh2_scheme = OAuth2PasswordBearer(tokenUrl='/token')


async def create_access_token(user_data: dict) -> str:
    exp = datetime.now(timezone.utc) + timedelta(hours=int(ACCESS_EXPIRE))
    return jwt.encode(
        {
            'sub': str(user_data.get('id')),
            'exp': exp,
            'user_data': user_data,
            'type': 'access'
        },
        JWT_SECRET_KEY,
        algorithm=ALGORITHM
    )


async def create_refresh_token(user_data: dict) -> str:
    exp = datetime.now(timezone.utc) + timedelta(days=int(REFRESH_EXPIRE))
    return jwt.encode(
        {
            'sub': str(user_data.get('id')),
            'exp': exp,
            'user_data': user_data,
            'type': 'refresh'
        },
        JWT_SECRET_KEY,
        algorithm=ALGORITHM
    )


async def refresh_access_token(refresh: str):
    try:
        if refresh:
            payload = jwt.decode(
                refresh,
                JWT_SECRET_KEY,
                algorithms=[ALGORITHM]
            )

            if payload.get('type') != 'refresh':
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='invalid token type'
                )

            return await create_access_token(payload.get('user_data'))

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='token not found'
        )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid token'
        )


async def custom_set_cookie(
        response: Response,
        access_token: str,
        refresh_token: str) -> None:

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=3600,
        path="/",
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=604800,
        path='/'
    )


async def get_current_user(request: Request):
    try:
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )

        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        if payload.get('type') != 'access':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )

        return payload.get('user_data')

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


async def auth_required(request: Request):
    return await get_current_user(request)
