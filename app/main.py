from fastapi import FastAPI, Response, status

from .db_helper import Database
from .queries import Query
from .schemas import Registration

app = FastAPI()
db = Database()


@app.get("/")
async def index():
    return {"message": "Hello World"}


@app.post("/register")
async def register(item: Registration, response: Response):
    pg_cursor = db.get_cursor()
    pg_cursor.execute(
        Query.register_user(),
        (item.first_name, item.last_name, item.email, item.username, item.password),
    )
    user = pg_cursor.fetchone()
    Database.connection.commit()
    if user:
        response.status_code = status.HTTP_201_CREATED
        return {"data": user}
