from abc import ABC, abstractmethod

class Storage(ABC):
    @abstractmethod
    def save(self, product_title: str, product_data: dict):
        pass

    @abstractmethod
    def get(self, product_title: str):
        pass

    @abstractmethod
    def update(self, product_title: str, product_data: dict):
        pass