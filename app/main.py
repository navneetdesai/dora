from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .db_helper import engine
from .routers import auth, user

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def index():
    return {"message": "Hello World"}
