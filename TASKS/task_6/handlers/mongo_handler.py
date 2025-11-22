from typing import Any, Dict, Optional

from pymongo import MongoClient

from TASKS.utils.design import Color, Message


class MongoHandler:
    def __init__(self, uri: str = "mongodb://localhost:27017/", db_name: str = "test_db"):
        self.uri = uri
        self.db_name = db_name
        self.client: Optional[MongoClient] = None
        self.db = None

    def connect(self):
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
            Message.print_message(
                f"Connected to MongoDB at {self.uri}, DB: {self.db_name}",
                Color.GREEN,
                Color.LIGHT_WHITE,
            )
        except Exception as e:
            Message.print_message(f"MongoDB connection error: {e}", Color.RED, Color.LIGHT_WHITE)
            self.client = None

    def insert_one(self, collection: str, data: Dict[str, Any]):
        if self.db is None:
            Message.print_message(
                "No DB connection. Call connect() first", Color.RED, Color.LIGHT_WHITE
            )
            return None
        try:
            result = self.db[collection].insert_one(data)
            Message.print_message(
                f"✅ Inserted document ID: {result.inserted_id}", Color.BLUE, Color.LIGHT_WHITE
            )
            return result.inserted_id
        except Exception as e:
            Message.print_message(f"❌ Insert error: {e}", Color.RED, Color.LIGHT_WHITE)
            return None

    def find_one(self, collection: str, query: Dict[str, Any]):
        if self.db is None:
            print("⚠️ No DB connection. Call connect() first.")
            return None

        try:
            result = self.db[collection].find_one(query)
            print(f"🔎 Found document: {result}")
            return result
        except Exception as e:
            print(f"❌ Find error: {e}")
            return None

    def insert_many(self, collection: str, data: list[Dict[str, Any]]):
        """
        Вставка нескольких документов
        """
        if self.db is None:
            Message.print_message(
                "No DB connection. Call connect() first", Color.RED, Color.LIGHT_WHITE
            )
            return None

        try:
            result = self.db[collection].insert_many(data)
            Message.print_message(
                f"✅ Inserted {len(result.inserted_ids)} documents.", Color.BLUE, Color.LIGHT_WHITE
            )
            return result.inserted_ids
        except Exception as e:
            Message.print_message(f"❌ Insert many error: {e}", Color.RED, Color.LIGHT_WHITE)
            return None


if __name__ == "__main__":
    client = MongoHandler()
    client.connect()
