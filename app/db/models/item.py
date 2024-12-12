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
    image: Mapped[bytes]
    author: Mapped[str]
    author_id: Mapped[int]




#sigma, skibidi, rizz, goofy, bingus, floppa, chad, sus, yeet, cringe, bazinga, drip, brokey, slay, uwu, oof, pog, zoomer, vibes, sussy, baka, noob, pro, slatt, flex, gucci, vibecheck, dripcheck, wombo, skrtt, plop, swaggy, dab, lit, savage