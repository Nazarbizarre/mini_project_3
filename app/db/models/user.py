from sqlalchemy.orm import Mapped

from .. import Base 


class User(Base):
    __tablename__ = "users"
    
    name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
