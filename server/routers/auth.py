from passlib.context import CryptContext

from . import (
    APIRouter,
    status,
    HTTPException,
    Response,
    Depends,
    Request
)

from ..schemas import (
    RegisterUserModel,
    LoginUserModel
)

from ..utils import (
    create_refresh_token,
    create_access_token,
    refresh_access_token,
    custom_set_cookie,
)

from ..db import (
    db_manager,
    AsyncSession,
    User,
    select
)

auth_app = APIRouter(prefix='/auth', tags=['Auth'])
crypt_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


@auth_app.post('/register',
            status_code=status.HTTP_201_CREATED,
            summary='register user',
            description='endoint for creating tokens and registered user')
async def register(
        response: Response,
        user: RegisterUserModel,
        session: AsyncSession = Depends(db_manager.get_session_begin)):

    user_data = user.model_dump()
    user_data['password'] = crypt_pwd.hash(user.password)

    new_user = User(**user_data)
    session.add(new_user)
    await session.flush()

    sub_data = {
        'id': new_user.id,
        'name': new_user.name,
        'role': new_user.role
    }

    access_token = await create_access_token(sub_data)
    refresh_token = await create_refresh_token(sub_data)

    await custom_set_cookie(
        response,
        access_token,
        refresh_token
    )

    return {
        'tokens': {
            'access': access_token,
            'refresh': refresh_token
        }
    }


@auth_app.post('/token',
            summary='getting tokens',
            description='enpoind for getting tokens by the belligerent account')
async def login(
        response: Response,
        user: LoginUserModel,
        session: AsyncSession = Depends(db_manager.get_session)):

    user_obj = await session.scalar(
        select(User)
        .where(User.name == user.name)
    )

    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user not found'
        )

    if not crypt_pwd.verify(user.password, user_obj.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='password invalid'
        )

    sub_data = {
        'id': user_obj.id,
        'name': user_obj.name,
        'role': user_obj.role
    }

    access_token = await create_access_token(sub_data)
    refresh_token = await create_refresh_token(sub_data)

    await custom_set_cookie(
        response,
        access_token,
        refresh_token
    )

    return {
        'tokens': {
            'access': access_token,
            'refresh': refresh_token
        }
    }


@auth_app.post('/refresh',
            summary='refresh access token',
            description='enpoind for refreshing access token by refresh')
async def refresh(requset: Request, response: Response):
    token = requset.cookies.get('refresh_token')
    new_access_token = await refresh_access_token(token)
    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=3600,
        path="/",
    )

    return {'tokens': {
        'access': new_access_token
    }}


@auth_app.delete('/logout',
                summary='logout user',
                description='endpoint for clearing authentication cookies')
async def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        path="/"
    )
    
    response.delete_cookie(
        key="refresh_token",
        path="/"
    )

    return {'status': 'tokens deleted'}