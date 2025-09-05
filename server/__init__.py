from fastapi import FastAPI

from .routers import (
    link_app,
    auth_app
)


app = FastAPI()
app.include_router(link_app)
app.include_router(auth_app)