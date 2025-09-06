from . import (
    BaseModel
)


class RegisterUserModel(BaseModel):
    name: str
    password: str


class LoginUserModel(BaseModel):
    name: str
    password: str 