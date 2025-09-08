from fastapi import (
    APIRouter,
    status,
    HTTPException,
    Response,
    Depends,
    Request,
)

from fastapi.responses import RedirectResponse

from .links import link_app
from .auth import auth_app