import uvicorn
import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from router import blogs, users
from auth import authentication
from settings import API_HOST, API_PORT, ROOT
from db.database import engine
from db import models

app = FastAPI()
app.include_router(blogs.router)
app.include_router(users.router)
app.include_router(authentication.router)

models.Base.metadata.create_all(engine)

if __name__ == "__main__":
    uvicorn.run(app, host=API_HOST, port=API_PORT)
