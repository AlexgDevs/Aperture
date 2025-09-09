from faker import Faker

from ..db import (
    select,
    AsyncSession,
    Link,
    User
)

faq = Faker()

async def create_short_link(session: AsyncSession, l: int = 5):
    new_link_name = "".join(faq.random_choices(length=l))
    link = await session.scalar(
        select(Link)
        .where(Link.short_link == new_link_name)
    )

    if not link:
        return new_link_name

    return await create_short_link(session)