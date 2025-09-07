from typing import (
    Literal, 
    List)

from pydantic import (
    BaseModel, 
    field_validator)

from .user import (
    RegisterUserModel,
    LoginUserModel
)