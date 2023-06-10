import time

import psycopg2 as ps
from dotenv import dotenv_values
from psycopg2.extras import RealDictCursor


class Database:
    connection: ps.extensions.connection = None
    cursor: RealDictCursor = None
    retries: int = 3

    def __init__(self, retries=3):
        """
        Setup the database connection
        """
        self.retries = retries
        self.setup_db()

    def setup_db(self):
        """
        Setup the database connection
        :return: None
        """
        while self.retries > 0:
            try:
                env = dotenv_values()
                Database.connection = ps.connect(
                    host=env["HOST"],
                    database=env["DATABASE"],
                    user=env["USER"],
                    password=env["PASSWORD"],
                    cursor_factory=RealDictCursor,
                )
                self.cursor = self.connection.cursor()
                print("Connected to Dora")
                break
            except Exception as e:
                print(e)
                print("Could not connect to database. Retrying in 2 seconds...")
                time.sleep(2)
                self.retries -= 1

    def get_cursor(self):
        """
        Get the database cursor
        :return:
        """
        return self.cursor
