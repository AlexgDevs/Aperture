from os import getenv

import json

from dotenv import load_dotenv

from redis.asyncio import from_url

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

load_dotenv()

link_app = APIRouter(prefix='/links', tags=['Links'])
redis = from_url(getenv('REDIS_URL'), decode_responses=True)


@link_app.post('/',
            status_code=status.HTTP_201_CREATED,
            summary='create short link',
            description='enpoind for creating short link')
async def short_link(
    orig_link: CreateLinkModel, 
    session: AsyncSession = Depends(db_manager.get_session_begin),
    user: dict = Depends(auth_required)):

    cache_link = await redis.get(f'orig:{orig_link}')
    if cache_link:
        cache_link_data = json.loads(cache_link)
        return {
            'status': 'handle cahce',
            'short_link': cache_link_data.get('short_link'),
            'fast_short_link': cache_link_data.get('fast_short_link')
        }

    link_data = orig_link.model_dump()
    link_data['short_link'] = await create_short_link(session)
    link_data['user_id'] = user.get('id')

    new_link = Link(**link_data)
    session.add(new_link)
    
    short_link = f'http://127.0.0.1:8000/links/{new_link.short_link}'
    fast_short_link = f'http://127.0.0.1:8000/links/f/{new_link.short_link}'
    await session.flush()

    link_data_for_cache = {
        'short_link': short_link,
        'fast_short_link': fast_short_link
    }

    await redis.setex(f'orig:{new_link.original_link}', 86400, json.dumps(link_data_for_cache))

    return {'status': 'created', 
            'short_link': short_link,
            'fast_short_link': fast_short_link
            }


@link_app.get('/{short}',
        response_model=LinkResponse,
        summary='get orig link by short',
        description='enpoind for getting orig link by short')
async def get_short_link(
    short: str,
    session: AsyncSession = Depends(db_manager.get_session)):

    cache_link = await redis.get(f'short:{short}')
    if cache_link:
        cache_link_data = json.loads(cache_link)
        cache_link_data['unest_cache'] = True
        return LinkResponse.model_validate(cache_link_data)

    link = await DBHelper.get_link(short, session)
    link_data_for_cahce = {
        'original_link': link.original_link,
        'short_link': link.short_link,
        'user_id': link.user_id
    }

    await redis.setex(f'short:{short}', 86400, json.dumps(link_data_for_cahce))
    return link


@link_app.get('/f/{short}',
        summary='redicrect by orig link',
        description='enpoind for redicrect orig link by short')
async def get_short_link(
    short: str,
    session: AsyncSession = Depends(db_manager.get_session)):

    cache_link = await redis.get(f'fast_link:{short}')
    if cache_link:
        return RedirectResponse(
            url=cache_link,
            status_code=status.HTTP_302_FOUND
        )

    link = await DBHelper.get_link(short, session)
    await redis.setex(f'fast_link:{short}', 86400, link.original_link)
    return RedirectResponse(
        url=link.original_link,
        status_code=status.HTTP_302_FOUND
    )
