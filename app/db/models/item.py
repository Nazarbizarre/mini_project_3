from datetime import datetime

from sqlalchemy.orm import Mapped

from .. import Base


class Item(Base):
    __tablename__ = "items"

    price: Mapped[int]
    title: Mapped[str]
    description: Mapped[str]
    published_at: Mapped[datetime]
    category: Mapped[str]
    photo: Mapped[bytes]
    author: Mapped[str]
    author_id: Mapped[int]
