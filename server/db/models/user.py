from typing import List

from .. import Base

from . import (
    Mapped,
    mapped_column,
    relationship,
    Literal
)

class User(Base):
    __tablename__='users'
    name: Mapped[str] = mapped_column(default='guest')
    role: Mapped[Literal['guest', 'admin', 'moderator']] = mapped_column(default='guest')
    password: Mapped[str]

    links: Mapped[List['Link']] = relationship('Link', back_populates='user')