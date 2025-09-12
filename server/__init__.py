from datetime import time

import logging

from fastapi import FastAPI, Request

from .db import db_manager

from .middlewares import (
    register_middlewares
)

from .routers import (
    link_app,
    auth_app
)

app = FastAPI()

register_middlewares(app)

app.include_router(link_app)
app.include_router(auth_app)

from . import middlewares