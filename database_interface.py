from abc import ABC, abstractmethod

class Database(ABC):

    @abstractmethod
    def create(self, entity):
        pass

    @abstractmethod
    def read(self, entity_type, entity_id):
        pass

    @abstractmethod
    def update(self, entity):
        pass

    @abstractmethod
    def delete(self, entity_type, entity_id):
        pass