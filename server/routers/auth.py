from . import (
    APIRouter,
    status,
    HTTPException,
    Response
)

from ..schemas import (
    RegisterUserModel,
    LoginUserModel
)

from ..utils import (
    create_refresh_token,
    create_access_token,
    refresh_access_token
)


auth_app = APIRouter(prefix='/auth', tags=['Auth'])


@auth_app.post('/register',
            status_code=status.HTTP_201_CREATED,
            summary='register user',
            description='endoint for creating tokens and registered user')
async def register(response: Response, user: RegisterUserModel):
    #db soon

    access_token = await create_access_token()
    refresh_token = await create_refresh_token()

    response.set_cookie(
        access_token,
    )

    response.set_cookie(
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
async def login(response: Response, user: LoginUserModel):
    #db soon

    access_token = await create_access_token()
    refresh_token = await create_refresh_token()

    response.set_cookie(
        access_token,
    )

    response.set_cookie(
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
async def refresh(response: Response):
    token = response.get('refresh_token')
    return await refresh_access_token(token)