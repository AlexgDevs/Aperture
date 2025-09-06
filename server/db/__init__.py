from .config import db_settings

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class DBManager:
    def __init__(self):
        self.db_url = db_settings.db_url
        self.echo = db_settings.echo
        self.engine = create_async_engine(
            url='sqlite+aiosqlite:///aperture.db',
            echo=True
        )
        self.Session = async_sessionmaker(
            self.engine
        )


    async def up(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


    async def drop(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


    async def migrate(self):
        await self.drop()
        await self.up()


    async def get_session(self):
        async with self.Session() as session:
            yield session


    async def get_session_begin(self):
            async with self.Session.begin() as session:
                yield session


db_manager = DBManager()

from .models import (
    User
)