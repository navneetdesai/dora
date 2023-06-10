"""
This file contains all the queries that are used in the application.
"""


class Query:
    """
    This class contains all the queries that are used in the application.
    """

    @staticmethod
    def register_user():
        """
        This method returns the query to register a user into the users table.
        The query should be formatted with the user's first name, last name,
        email, username, and password.

        :return:
        """

        return """
        INSERT INTO users (first_name, last_name, email, username, password)
        VALUES (%s, %s, %s, %s, %s) RETURNING *;
        """
