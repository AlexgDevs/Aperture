from . import (
    BaseModel
)


class RegisterUserModel(BaseModel):
    name: str
    email: str
    password: str


class LoginUserModel(BaseModel):
    name: str
    password: str 