from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError

class Database:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="wildcard"):
        try:
            self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            self.client.admin.command('ping')  # Verifica la conexión
            self.db = self.client[db_name]
            print("✅ Conectado a MongoDB correctamente.")
        except ConnectionFailure:
            print("❌ Error: No se pudo conectar a MongoDB.")
            self.client = None

    def get_collection(self, collection_name):
        """Obtiene una colección de la base de datos."""
        if self.client:
            return self.db[collection_name]
        return None

    def insert_one(self, collection_name, data):
        """Inserta un documento en la colección especificada."""
        try:
            collection = self.get_collection(collection_name)
            if collection and isinstance(data, dict):
                result = collection.insert_one(data)
                return result.inserted_id
            print("❌ Error: Datos inválidos o colección no encontrada.")
        except PyMongoError as e:
            print(f"❌ Error al insertar en {collection_name}: {e}")

    def find_one(self, collection_name, query):
        """Busca un documento en la colección."""
        try:
            collection = self.get_collection(collection_name)
            return collection.find_one(query) if collection else None
        except PyMongoError as e:
            print(f"❌ Error al buscar en {collection_name}: {e}")

    def update_one(self, collection_name, query, update_values):
        """Actualiza un documento en la colección."""
        try:
            collection = self.get_collection(collection_name)
            if collection:
                result = collection.update_one(query, {"$set": update_values})
                return result.modified_count
        except PyMongoError as e:
            print(f"❌ Error al actualizar en {collection_name}: {e}")

    def delete_one(self, collection_name, query):
        """Elimina un documento en la colección."""
        try:
            collection = self.get_collection(collection_name)
            if collection:
                result = collection.delete_one(query)
                return result.deleted_count
        except PyMongoError as e:
            print(f"❌ Error al eliminar en {collection_name}: {e}")

    def close_connection(self):
        """Cierra la conexión con MongoDB."""
        if self.client:
            self.client.close()
            print("🔌 Conexión con MongoDB cerrada.")

# Pruebas de uso
if __name__ == "__main__":
    db = Database()

    # Insertar un jugador de prueba
    player_data = {"name": "Jack", "chips": 100, "level": 1}
    player_id = db.insert_one("players", player_data)
    print(f"🃏 Jugador insertado con ID: {player_id}")

    # Buscar el jugador
    found_player = db.find_one("players", {"name": "Jack"})
    print("👤 Jugador encontrado:", found_player)

    # Actualizar fichas del jugador
    db.update_one("players", {"name": "Jack"}, {"chips": 200})

    # Eliminar jugador
    db.delete_one("players", {"name": "Jack"})

    # Cerrar conexión
    db.close_connection()
