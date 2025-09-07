from typing import (
    Literal, 
    List)

from fastapi import (
    HTTPException,
    status
)

from pydantic import (
    BaseModel, 
    field_validator)

from .user import (
    RegisterUserModel,
    LoginUserModel
)

from .link import (
    CreateLinkModel,
    LinkResponse
)