from typing import Literal

from sqlalchemy import ForeignKey

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from .user import User
from .link import Link