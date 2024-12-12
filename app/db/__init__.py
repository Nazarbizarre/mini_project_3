from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped


class PublishedMixin:
    published_at: Mapped[datetime] = mapped_column(default=datetime.now())


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)


class AsyncDB:
    ENGINE = create_engine("sqlite:///users.db")
    SESSION = sessionmaker(bind=ENGINE)

    @classmethod
    def up(cls):
        Base.metadata.create_all(cls.ENGINE)

    @classmethod
    def down(cls):
        Base.metadata.drop_all(cls.ENGINE)

    @classmethod
    def migrate(cls):
        Base.metadata.drop_all(cls.ENGINE)
        Base.metadata.create_all(cls.ENGINE)


    @classmethod
    def get_session(cls):
        with cls.SESSION.begin() as session:
            yield session


from .models import User, Item
