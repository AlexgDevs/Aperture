from . import (
    APIRouter,
    status,
    HTTPException,
    Depends,
    RedirectResponse)

from ..schemas import (
    CreateLinkModel,
    LinkResponse
)

from ..db import (
    db_manager,
    AsyncSession,
    Link,
    User,
    select,
    joinedload,
    DBHelper
    )


from ..utils import(
    auth_required,
    create_short_link,
)

link_app = APIRouter(prefix='/links', tags=['Links'])


@link_app.post('/',
            status_code=status.HTTP_201_CREATED,
            summary='create short link',
            description='enpoind for creating short link')
async def short_link(
    orig_link: CreateLinkModel, 
    session: AsyncSession = Depends(db_manager.get_session_begin),
    user: dict = Depends(auth_required)):

    link_data = orig_link.model_dump()
    link_data['short_link'] = await create_short_link()
    link_data['user_id'] = user.get('id')

    session.add(Link(**link_data))
    return {'status': 'created', 
            'short_link': f"http://127.0.0.1:8000/links/{link_data.get('short_link')}",
            'fast_short_link': f"http://127.0.0.1:8000/links/fast/{link_data.get('short_link')}"
            }


@link_app.get('/{short}',
        response_model=LinkResponse,
        summary='get orig link by short',
        description='enpoind for getting orig link by short')
async def get_short_link(
    short: str,
    user: dict = Depends(auth_required),
    session: AsyncSession = Depends(db_manager.get_session)):

    link = await DBHelper.get_link(user.get('id'), short, session)
    return link


@link_app.get('/fast/{short}',
        summary='redicrect by orig link',
        description='enpoind for redicrect orig link by short')
async def get_short_link(
    short: str,
    user: dict = Depends(auth_required),
    session: AsyncSession = Depends(db_manager.get_session)):

    link = await DBHelper.get_link(user.get('id'), short, session)
    return RedirectResponse(
        url=link.original_link,
        status_code=status.HTTP_302_FOUND
    )
