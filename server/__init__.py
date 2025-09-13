from fastapi import FastAPI

from .middlewares import (
    register_middlewares
)

from .routers import (
    link_app,
    auth_app
)

from .db import(
    db_manager
)

API_URL='http://localhost:8000'

app = FastAPI()

register_middlewares(app)

app.include_router(link_app)
app.include_router(auth_app)


from . import middlewares