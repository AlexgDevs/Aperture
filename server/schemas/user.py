from passlib.context import CryptContext

from fastapi import (
    status,
    HTTPException
)

from . import (
    BaseModel,
    field_validator
)

from ..db import (
    User, 
    db_manager, 
    select
)


class RegisterUserModel(BaseModel):
    name: str
    password: str


class LoginUserModel(BaseModel):
    name: str
    password: str