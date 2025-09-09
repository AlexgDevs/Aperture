from validators import url

from . import (
    BaseModel,
    field_validator,
    status,
    HTTPException
)


def custom_400_raise():
    raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='uncorrected link'
            )


class CreateLinkModel(BaseModel):
    original_link: str

    @field_validator('original_link', mode='after')
    def validate_link(cls, v):
        if not url(v):
            return custom_400_raise()
        return v


class LinkResponse(BaseModel):
    original_link: str
    short_link: str
    user_id: int
    unest_cache: bool | None = None

    class Config:
        from_attributes = True