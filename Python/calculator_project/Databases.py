"""
project/
│
├── clients/
│   ├── mysql_client.py
│   ├── mongo_client.py
│   ├── redis_client.py
│   └── logger.py
│
├── protocols/
│   └── interfaces.py
│
├── services/
│   └── user_service.py
│
├── container.py

from typing import Protocol, Any
"""


"""
Basic connection example.
import redis

r = redis.Redis(
    host='collegial-spirited-blooming-17391.db.redis.io',
    port=13239,
    decode_responses=True,
    username="default",
    password="wiR0tPJYnhkdyNDhGmxqmtkluTXb8gb4",
)

success = r.set('foo', 'bar')
# True

result = r.get('foo')
print(result)
# >>> bar
"""



# from Databases.Drivers.DatabaseText import DatabaseText
# from calculator import Calculator


# selected_db = "text"
# db = DatabaseText("config.env")
# calculator = Calculator()

