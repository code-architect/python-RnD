from IDatabase import InterfaceDatabase

from typing import Any
from datetime import datetime, timezone
from decimal import Decimal
import os

from dotenv import load_dotenv
from pymongo import MongoClient, ReturnDocument
from pymongo.collection import Collection
from pymongo.database import Database
from bson.decimal128 import Decimal128


class DatabaseMongoDB(InterfaceDatabase):
    def __init__(self, config_path: str = "config.env") -> None:
        load_dotenv(config_path)

        self.mongo_uri = os.getenv("MONGO_URI")
        self.database_name = os.getenv("MONGO_DATABASE")
        self.collection_name = os.getenv("MONGO_COLLECTION", "calculations")

        if not self.mongo_uri:
            raise ValueError("MONGO_URI is missing in config.env")

        if not self.database_name:
            raise ValueError("MONGO_DATABASE is missing in config.env")

        self.client: MongoClient | None = None
        self.database: Database | None = None
        self.collection: Collection | None = None
        self.counter_collection: Collection | None = None

    def connect(self) -> None:
        if self.client is not None:
            return

        self.client = MongoClient(self.mongo_uri)
        self.database = self.client[self.database_name]
        self.collection = self.database[self.collection_name]
        self.counter_collection = self.database["counters"]

        # Like PRIMARY KEY(id) in SQL
        self.collection.create_index("id", unique=True)

    def _get_next_id(self) -> int:
        self.connect()

        if self.counter_collection is None:
            raise RuntimeError("Counter collection is not connected.")

        counter = self.counter_collection.find_one_and_update(
            {"_id": self.collection_name},
            {"$inc": {"seq": 1}},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )

        return counter["seq"]

    def insert_calculation(
        self,
        first_value: float | Decimal,
        second_value: float | Decimal,
        operation: str,
        answer: float | Decimal
    ) -> int:
        self.connect()

        if self.collection is None:
            raise RuntimeError("MongoDB collection is not connected.")

        calculation_id = self._get_next_id()

        document = {
            "id": calculation_id,
            "first_value": Decimal128(str(first_value)),
            "second_value": Decimal128(str(second_value)),
            "operation": operation,
            "answer": Decimal128(str(answer)),
            "timestamp": datetime.now(timezone.utc)
        }

        self.collection.insert_one(document)

        return calculation_id

    def update_calculation(
        self,
        calculation_id: int,
        first_value: float | Decimal,
        second_value: float | Decimal,
        operation: str,
        answer: float | Decimal
    ) -> bool:
        self.connect()

        if self.collection is None:
            raise RuntimeError("MongoDB collection is not connected.")

        result = self.collection.update_one(
            {"id": calculation_id},
            {
                "$set": {
                    "first_value": Decimal128(str(first_value)),
                    "second_value": Decimal128(str(second_value)),
                    "operation": operation,
                    "answer": Decimal128(str(answer)),
                    "timestamp": datetime.now(timezone.utc)
                }
            }
        )

        return result.modified_count > 0

    def delete_calculation(self, calculation_id: int) -> bool:
        self.connect()

        if self.collection is None:
            raise RuntimeError("MongoDB collection is not connected.")

        result = self.collection.delete_one({"id": calculation_id})

        return result.deleted_count > 0

    def get_all_calculations(self) -> list[dict]:
        self.connect()

        if self.collection is None:
            raise RuntimeError("MongoDB collection is not connected.")

        rows = list(
            self.collection.find(
                {},
                {"_id": 0}
            ).sort("id", -1)
        )

        return self._convert_decimal128(rows)

    def get_calculation_by_id(self, calculation_id: int) -> dict | None:
        self.connect()

        if self.collection is None:
            raise RuntimeError("MongoDB collection is not connected.")

        row = self.collection.find_one(
            {"id": calculation_id},
            {"_id": 0}
        )

        if row is None:
            return None

        return self._convert_decimal128([row])[0]

    def execute(self, query: str) -> list[dict]:
        """
        Required by InterfaceDatabase.

        For MongoDB, query should be the operation name:
        - "get_all"
        """
        if query == "get_all":
            return self.get_all_calculations()

        raise ValueError(f"Unsupported MongoDB execute query: {query}")

    def getData(self, query: str) -> list[dict]:
        """
        Required by InterfaceDatabase.

        For MongoDB, query should be:
        - "get_all"
        """
        if query == "get_all":
            return self.get_all_calculations()

        raise ValueError(f"Unsupported MongoDB getData query: {query}")

    def close(self) -> None:
        if self.client is not None:
            self.client.close()
            self.client = None
            self.database = None
            self.collection = None
            self.counter_collection = None

    def _convert_decimal128(self, rows: list[dict]) -> list[dict]:
        converted_rows = []

        for row in rows:
            converted_row = {}

            for key, value in row.items():
                if isinstance(value, Decimal128):
                    converted_row[key] = float(value.to_decimal())
                else:
                    converted_row[key] = value

            converted_rows.append(converted_row)

        return converted_rows



"""
from pprint import pprint
from DatabaseMongoDB import DatabaseMongoDB


db = DatabaseMongoDB("config.env")

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
    first_value=20,
    second_value=4,
    operation="/",
    answer=5
)

print("Updated:", updated)

# SELECT ALL
rows = db.getData("get_all")
pprint(rows)

# SELECT ONE
single_row = db.get_calculation_by_id(new_id)
pprint(single_row)


# DELETE
deleted = db.delete_calculation(new_id)
print("Deleted:", deleted)

db.close()
"""






