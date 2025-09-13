from passlib.context import CryptContext

from fastapi import (
    status,
    HTTPException
)

from . import (
    BaseModel,
    field_validator,
    Field
)

from ..db import (
    User, 
    db_manager, 
    select
)


class RegisterUserModel(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=8, max_length=255)


class LoginUserModel(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=3, max_length=255)