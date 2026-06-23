from IDatabase import InterfaceDatabase


from pprint import pprint
from typing import Any
from datetime import datetime, timezone
from decimal import Decimal
import os

from dotenv import load_dotenv
import redis


class DatabaseRedis(InterfaceDatabase):
    def __init__(self, config_path: str = "config.env") -> None:
        load_dotenv(config_path)

        self.host = os.getenv("REDIS_HOST")
        self.port = int(os.getenv("REDIS_PORT", "6379"))
        self.username = os.getenv("REDIS_USERNAME", "default")
        self.password = os.getenv("REDIS_PASSWORD")
        self.decode_responses = os.getenv("REDIS_DECODE_RESPONSES", "True") == "True"
        self.ssl = os.getenv("REDIS_SSL", "False") == "True"

        if not self.host:
            raise ValueError("REDIS_HOST is missing in config.env")

        if not self.password:
            raise ValueError("REDIS_PASSWORD is missing in config.env")

        self.connection: redis.Redis | None = None

        self.id_counter_key = "calculations:id_counter"
        self.calculation_key_prefix = "calculation:"
        self.calculation_ids_key = "calculations:ids"

    def connect(self) -> None:
        if self.connection is not None:
            return

        self.connection = redis.Redis(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            decode_responses=self.decode_responses,
            ssl=self.ssl
        )

        self.connection.ping()

    def insert_calculation(
        self,
        first_value: float | int | Decimal,
        second_value: float | int | Decimal,
        operation: str,
        answer: float | int | Decimal
    ) -> int:
        self.connect()

        if self.connection is None:
            raise RuntimeError("Redis connection could not be established.")

        calculation_id = self.connection.incr(self.id_counter_key)

        key = f"{self.calculation_key_prefix}{calculation_id}"

        data = {
            "id": calculation_id,
            "first_value": str(Decimal(str(first_value))),
            "second_value": str(Decimal(str(second_value))),
            "operation": operation,
            "answer": str(Decimal(str(answer))),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        self.connection.hset(key, mapping=data)

        # Keep track of all calculation IDs
        self.connection.sadd(self.calculation_ids_key, calculation_id)

        return calculation_id

    def update_calculation(
        self,
        calculation_id: int,
        first_value: float | int | Decimal,
        second_value: float | int | Decimal,
        operation: str,
        answer: float | int | Decimal
    ) -> bool:
        self.connect()

        if self.connection is None:
            raise RuntimeError("Redis connection could not be established.")

        key = f"{self.calculation_key_prefix}{calculation_id}"

        if not self.connection.exists(key):
            return False

        data = {
            "first_value": str(Decimal(str(first_value))),
            "second_value": str(Decimal(str(second_value))),
            "operation": operation,
            "answer": str(Decimal(str(answer))),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        self.connection.hset(key, mapping=data)

        return True

    def delete_calculation(self, calculation_id: int) -> bool:
        self.connect()

        if self.connection is None:
            raise RuntimeError("Redis connection could not be established.")

        key = f"{self.calculation_key_prefix}{calculation_id}"

        deleted_count = self.connection.delete(key)

        if deleted_count > 0:
            self.connection.srem(self.calculation_ids_key, calculation_id)
            return True

        return False

    def get_calculation_by_id(self, calculation_id: int) -> dict | None:
        self.connect()

        if self.connection is None:
            raise RuntimeError("Redis connection could not be established.")

        key = f"{self.calculation_key_prefix}{calculation_id}"

        data = self.connection.hgetall(key)

        if not data:
            return None

        return self._convert_calculation(data)

    def get_all_calculations(self) -> list[dict]:
        self.connect()

        if self.connection is None:
            raise RuntimeError("Redis connection could not be established.")

        ids = self.connection.smembers(self.calculation_ids_key)

        calculations = []

        for calculation_id in ids:
            key = f"{self.calculation_key_prefix}{calculation_id}"
            data = self.connection.hgetall(key)

            if data:
                calculations.append(self._convert_calculation(data))

        calculations.sort(key=lambda item: item["id"], reverse=True)

        return calculations

    def execute(self, query: str) -> list[dict]:
        """
        Required by InterfaceDatabase.

        Redis is not SQL, so query is treated as a command name.

        Supported:
        - "get_all"
        """
        if query == "get_all":
            return self.get_all_calculations()

        raise ValueError(f"Unsupported Redis execute query: {query}")

    def getData(self, query: str) -> list[dict]:
        """
        Required by InterfaceDatabase.

        Supported:
        - "get_all"
        """
        if query == "get_all":
            return self.get_all_calculations()

        raise ValueError(f"Unsupported Redis getData query: {query}")

    def close(self) -> None:
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def _convert_calculation(self, data: dict[str, Any]) -> dict:
        return {
            "id": int(data["id"]),
            "first_value": Decimal(data["first_value"]),
            "second_value": Decimal(data["second_value"]),
            "operation": data["operation"],
            "answer": Decimal(data["answer"]),
            "timestamp": data["timestamp"]
        }






"""
db = DatabaseRedis("config.env")

# INSERT
new_id = db.insert_calculation(
    first_value=10,
    second_value=5,
    operation="+",
    answer=15
)

print("Inserted ID:", new_id)

# UPDATE
updated = db.update_calculation(
    calculation_id=new_id,
    first_value=25,
    second_value=5,
    operation="/",
    answer=5
)

print("Updated:", updated)

# SELECT ONE
row = db.get_calculation_by_id(new_id)
pprint(row)

# SELECT ALL
rows = db.getData("get_all")
pprint(rows)


# DELETE
deleted = db.delete_calculation(new_id)
print("Deleted:", deleted)

db.close()
"""






