"""
Main file for the Dora API.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .db_helper import engine
from .routers import alerts, auth, subscriber, user


def app_factory():
    """
    Factory function to create the FastAPI app.
    :return:
    """
    app_ = FastAPI()
    app_.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # include all routers
    models.Base.metadata.create_all(bind=engine)
    app_.include_router(user.DoraUser.router)
    app_.include_router(auth.DoraAuth.router)
    app_.include_router(alerts.DoraAlert.router)
    app_.include_router(subscriber.DoraSubscriber.router)

    return app_


app = app_factory()


@app.get("/")
async def index():
    return {"message": "Welcome to Dora!"}
