from os import getenv

from functools import wraps

from datetime import (
    datetime, 
    timezone, 
    timedelta
)

from dotenv import load_dotenv

from . import (
    jwt,
    JWTError,
    Depends,
    OAuth2PasswordBearer,
    HTTPException,
    status
)


load_dotenv()


ACCESS_EXPIRE = getenv('ACCESS_EXPIRE', 7)
REFRESH_EXPIRE = getenv('REFRESH_EXPIRE', 30)
ALGORITHM = getenv('ALGORITHM', 'SH256')
JWT_SECRET_KEY = getenv('JWT_SECRET_KEY')


outh2_scheme = OAuth2PasswordBearer(tokenUrl='/token')


async def create_access_token(user_data: dict) -> str:
    exp = datetime.now(timezone.utc) + timedelta(ACCESS_EXPIRE)
    return jwt.encode(
        {
            'sub': user_data.get('id'),
            'exp': exp,
            'user_data': user_data,
            'type': 'access'
        },
        JWT_SECRET_KEY,
        algorithm=ALGORITHM
    )


async def create_refresh_token(user_data: dict) -> str:
    exp = datetime.now(timezone.utc) + timedelta(REFRESH_EXPIRE)
    return jwt.encode(
        {
            'sub': user_data.get('id'),
            'exp': exp,
            'user_data': user_data,
            'type': 'refresh'
        },
        JWT_SECRET_KEY,
        algorithm=ALGORITHM
    )


async def refresh_access_token(token: str = Depends(outh2_scheme)):
    try:
        if token:
            if token.get('type') != 'refresh':
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='invalid token type'
                )

            payload = jwt.decode(
                token,
                JWT_SECRET_KEY,
                algorithms=[ALGORITHM]
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