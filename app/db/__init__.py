from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


class PublishedMixin:
    published_at: Mapped[datetime] = mapped_column(default=datetime.now())


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class AsyncDB:
    ENGINE = create_async_engine("sqlite+aiosqlite:///users.db")
    SESSION = sessionmaker(bind=ENGINE, class_=AsyncSession)

    @classmethod
    async def up(cls):
        async with cls.ENGINE.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @classmethod
    async def down(cls):
        async with cls.ENGINE.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    @classmethod
    async def migrate(cls):
        async with cls.ENGINE.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @classmethod
    async def get_session(cls):
        async with cls.SESSION.begin() as session:
            yield session


from .models import User, Item
