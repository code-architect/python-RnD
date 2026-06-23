from Databases.Drivers.DatabaseMongoDB import DatabaseMongoDB
from Databases.Drivers.DatabaseMySQL import DatabaseMySQL
from Databases.Drivers.DatabaseRedisDB import DatabaseRedis
from Databases.Drivers.DatabaseText import DatabaseText
from Databases.Drivers.IDatabase import InterfaceDatabase

class DatabaseFactory:
    @staticmethod
    def create(db_type: str) -> InterfaceDatabase:
        if db_type == "mysql":
            return DatabaseMySQL()
        elif db_type == "mongo":
            return DatabaseMongoDB()
        elif db_type == "redis":
            return DatabaseRedis()
        elif db_type == "text":
            return DatabaseText()
        else:
            raise ValueError(f"Unsupported database type: {db_type}")