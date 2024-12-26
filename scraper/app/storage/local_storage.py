import json
from storage.storage import Storage

class LocalStorage(Storage):
    def __init__(self, filepath="products.json"):
        self.filepath = filepath
        try:
            with open(self.filepath, "r") as file:
                self.data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = {}
            self._write_to_file()

    def save(self, product_title: str, product_data: dict):
        if product_title not in self.data:
            self.data[product_title] = product_data
            self._write_to_file()

    def get(self, product_title: str):
        return self.data.get(product_title)

    def update(self, product_title: str, product_data: dict):
        self.data[product_title] = product_data
        self._write_to_file()

    def _write_to_file(self):
        with open(self.filepath, "w") as file:
            json.dump(self.data, file, indent=4)
