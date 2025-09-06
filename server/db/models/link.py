from .. import Base

from . import (
    Mapped,
    mapped_column,
    relationship,
    Literal,
    ForeignKey
)


class Link(Base):
    __tablename__='links'
    original_link: Mapped[str]
    short_link: Mapped[str]

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship('User', back_populates='links', uselist=False)