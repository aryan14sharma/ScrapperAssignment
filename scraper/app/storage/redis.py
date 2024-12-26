import json
import redis
from storage.storage import Storage

class RedisStorage(Storage):
    def __init__(self, host="localhost", port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db)

    def save(self, product_title: str, product_data: dict):
        if not self.client.exists(product_title):
            self.client.set(product_title, json.dumps(product_data))

    def get(self, product_title: str):
        data = self.client.get(product_title)
        return json.loads(data) if data else None

    def update(self, product_title: str, product_data: dict):
        self.client.set(product_title, json.dumps(product_data))
