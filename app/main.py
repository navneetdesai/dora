from fastapi import FastAPI

from . import models
from .db_helper import engine
from .routers import auth, user

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def index():
    return {"message": "Hello World"}
