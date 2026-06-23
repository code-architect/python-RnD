from IDatabase import InterfaceDatabase
from typing import Any
import pymysql
from pymysql.cursors import DictCursor
from pprint import pprint



class DatabaseMySQL(InterfaceDatabase):
    def __init__(
        self,
        host: str,
        user: str,
        password: str,
        database: str,
        port: int,
        charset: str = "utf8mb4",
    ) -> None:
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.charset = charset
        self.connection: pymysql.connections.Connection | None = None

    def connect(self) -> None:
        if self.connection is not None and self.connection.open:
            return

        self.connection = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
            charset=self.charset,
            cursorclass=DictCursor,
            autocommit=False,
        )

    def execute(self, query: str) -> list[dict]:
        """
        Runs any SQL.
        - For SELECT, returns list[dict]
        - For INSERT/UPDATE/DELETE, commits and returns []
        """
        self.connect()

        if self.connection is None:
            raise RuntimeError("MySQL connection could not be established.")

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)

                # If query returns rows, fetch them
                if cursor.description is not None:
                    return cursor.fetchall()

                # Non-select query
                self.connection.commit()
                return []

        except Exception:
            self.connection.rollback()
            raise

    def getData(self, query: str) -> list[dict]:
        """
        Use this for SELECT queries only.
        """
        self.connect()

        if self.connection is None:
            raise RuntimeError("MySQL connection could not be established.")

        with self.connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def close(self) -> None:
        if self.connection is not None and self.connection.open:
            self.connection.close()
            self.connection = None







db = DatabaseMySQL(
    host="sql12.freesqldatabase.com",
    user="sql12831138",
    password="Xr1rxcCGBi",
    database="sql12831138",
    port=3306
)

# SELECT
rows = db.getData("SELECT id, name, email FROM users")
pprint(rows)

# INSERT
# db.execute("INSERT INTO users (name, email) VALUES ('John', 'john@test.com')")

# UPDATE
# db.execute("UPDATE users SET name = 'Johnny' WHERE id = 1")

# DELETE
#db.execute("DELETE FROM users WHERE id = 1")

#db.close()


"""

https://www.freesqldatabase.com/account/
https://cloud.mongodb.com/v2/5ff8bffc13a8102676800b1a#/clusters



CREATE TABLE calculations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_value DECIMAL(10, 2) NOT NULL,
    second_value DECIMAL(10, 2) NOT NULL,
    operation VARCHAR(20) NOT NULL,
    answer DECIMAL(10, 2) NOT NULL,
    `timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


# INSERT
db.execute(
INSERT INTO calculations (
    first_value,
    second_value,
    operation,
    answer
)
VALUES (
    10,
    5,
    '+',
    15
)
)

# UPDATE
db.execute(
UPDATE calculations
SET
    first_value = 20,
    second_value = 4,
    operation = '/',
    answer = 5,
    `timestamp` = CURRENT_TIMESTAMP
WHERE id = 1
)

# DELETE
db.execute(
DELETE FROM calculations
WHERE id = 1
)

# SELECT
rows = db.getData(
SELECT
    id,
    first_value,
    second_value,
    operation,
    answer,
    `timestamp`
FROM calculations
)

pprint(rows)
================================

"""


















