from fastapi import FastAPI
from routers import user

from . import models
from .db_helper import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
app.include_router(user.router)


@app.get("/")
async def index():
    return {"message": "Hello World"}
