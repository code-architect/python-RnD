from IDatabase import InterfaceDatabase
from typing import Any
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
import json
import os
from pprint import pprint


from dotenv import load_dotenv


class DatabaseText(InterfaceDatabase):
    def __init__(self, config_path: str = "config.env") -> None:
        load_dotenv(config_path)

        self.file_path = Path(os.getenv("TEXT_DB_FILE", "calculations.md"))
        self.connected = False

    def connect(self) -> None:
        """
        Creates the text file if it does not exist.
        """
        if self.connected:
            return

        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.file_path.touch(exist_ok=True)

        self.connected = True

    def insert_calculation(
        self,
        first_value: float | int | Decimal,
        second_value: float | int | Decimal,
        operation: str,
        answer: float | int | Decimal
    ) -> int:
        self.connect()

        rows = self._read_rows()
        calculation_id = self._get_next_id(rows)

        row = {
            "id": calculation_id,
            "first_value": str(Decimal(str(first_value))),
            "second_value": str(Decimal(str(second_value))),
            "operation": operation,
            "answer": str(Decimal(str(answer))),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        rows.append(row)
        self._write_rows(rows)

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

        rows = self._read_rows()

        for row in rows:
            if int(row["id"]) == calculation_id:
                row["first_value"] = str(Decimal(str(first_value)))
                row["second_value"] = str(Decimal(str(second_value)))
                row["operation"] = operation
                row["answer"] = str(Decimal(str(answer)))
                row["timestamp"] = datetime.now(timezone.utc).isoformat()

                self._write_rows(rows)
                return True

        return False

    def delete_calculation(self, calculation_id: int) -> bool:
        self.connect()

        rows = self._read_rows()
        original_count = len(rows)

        rows = [
            row for row in rows
            if int(row["id"]) != calculation_id
        ]

        if len(rows) == original_count:
            return False

        self._write_rows(rows)
        return True

    def get_calculation_by_id(self, calculation_id: int) -> dict | None:
        self.connect()

        rows = self._read_rows()

        for row in rows:
            if int(row["id"]) == calculation_id:
                return self._convert_row(row)

        return None

    def get_all_calculations(self) -> list[dict]:
        self.connect()

        rows = self._read_rows()
        converted_rows = [self._convert_row(row) for row in rows]

        converted_rows.sort(
            key=lambda row: row["id"],
            reverse=True
        )

        return converted_rows

    def execute(self, query: str) -> list[dict]:
        """
        Required by InterfaceDatabase.

        Since this is a text file, query is treated as a command.

        Supported:
        - "get_all"
        - "clear_all"
        """
        self.connect()

        if query == "get_all":
            return self.get_all_calculations()

        if query == "clear_all":
            self._write_rows([])
            return []

        raise ValueError(f"Unsupported text-file execute query: {query}")

    def getData(self, query: str) -> list[dict]:
        """
        Required by InterfaceDatabase.

        Supported:
        - "get_all"
        """
        self.connect()

        if query == "get_all":
            return self.get_all_calculations()

        raise ValueError(f"Unsupported text-file getData query: {query}")

    def close(self) -> None:
        """
        Nothing to close for a text file.
        Exists only so the class behaves like the others.
        """
        self.connected = False

    def _read_rows(self) -> list[dict]:
        self.connect()

        rows = []

        with self.file_path.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if line:
                    rows.append(json.loads(line))

        return rows

    def _write_rows(self, rows: list[dict]) -> None:
        self.connect()

        with self.file_path.open("w", encoding="utf-8") as file:
            for row in rows:
                file.write(json.dumps(row) + "\n")

    def _get_next_id(self, rows: list[dict]) -> int:
        if not rows:
            return 1

        return max(int(row["id"]) for row in rows) + 1

    def _convert_row(self, row: dict[str, Any]) -> dict:
        return {
            "id": int(row["id"]),
            "first_value": Decimal(row["first_value"]),
            "second_value": Decimal(row["second_value"]),
            "operation": row["operation"],
            "answer": Decimal(row["answer"]),
            "timestamp": row["timestamp"]
        }









"""
db = DatabaseTextFile("config.env")

# INSERT
new_id = db.insert_calculation(
    first_value=25,
    second_value=5,
    operation="/",
    answer=5
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





