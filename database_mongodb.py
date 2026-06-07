from pymongo import MongoClient

class DatabaseMongo():
    def __init__(self):
        self.client = MongoClient("mongodb://mongodb:27017/")
        self.db = self.client["night_city"]

    def create(self, entity_type, entity):
        """Insere um documento na collection correspondente ao tipo da entidade."""
        self.db[entity_type].insert_one(entity)

    def read(self, entity_type, entity_id):
        """Busca um documento pelo campo 'pk' na collection do tipo da entidade."""
        collection = self.db[entity_type]
        returnal = collection.find_one({"pk": entity_id})
        return returnal

    def read_all(self, entity_type):
        """Retorna todos os documentos de uma collection."""
        collection = self.db[entity_type]
        return list(collection.find({}, {"_id": 0}))

    def update(self, entity_type, entity_id, updated_fields):
        """Atualiza campos de um documento identificado pelo 'pk'."""
        collection = self.db[entity_type]
        collection.update_one({"pk": entity_id}, {"$set": updated_fields})

    def delete(self, entity_type, entity_id):
        """Remove um documento identificado pelo 'pk'."""
        collection = self.db[entity_type]
        collection.delete_one({"pk": entity_id})

    def drop_all(self):
        self.client.drop_database("night_city")
        self.db = self.client["night_city"]