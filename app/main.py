import time

import psycopg2 as ps
from dotenv import dotenv_values
from fastapi import FastAPI, Response, status
from psycopg2.extras import RealDictCursor

from .schemas import Registration

app = FastAPI()


class Database:
    connection = None
    cursor = None

    def setup_db(self):
        while True:
            try:
                env = dotenv_values()
                Database.connection = ps.connect(
                    host=env["HOST"],
                    database=env["DATABASE"],
                    user=env["USER"],
                    password=env["PASSWORD"],
                    cursor_factory=RealDictCursor,
                )
                Database.cursor = Database.connection.cursor()
                print("Connected to Dora")
                return Database.cursor
            except Exception as e:
                print("Could not connect to database. Retrying in 2 seconds...")
                time.sleep(2)
                print(e)


Database().setup_db()


@app.get("/")
async def index():
    return {"message": "Hello World"}


@app.post("/register")
async def register(item: Registration, response: Response):
    query = """
        INSERT INTO users (first_name, last_name, email, username, password)
        VALUES (%s, %s, %s, %s, %s) RETURNING *;
    """
    cursor = Database.cursor
    if not cursor:
        return {"message": "Could not connect to database"}
    cursor.execute(
        query,
        (item.first_name, item.last_name, item.email, item.username, item.password),
    )
    user = cursor.fetchone()
    Database.connection.commit()
    if user:
        response.status_code = status.HTTP_201_CREATED
        return user
