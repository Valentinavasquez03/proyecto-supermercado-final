from pymongo import MongoClient

def dbConnection():
    try:
        # URI de conexión local para todo el equipo de desarrollo
        MONGO_URI = "mongodb://localhost:27017/"
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        
        # Nombre de la base de datos compartida del supermercado
        db = client['supermercado_db']
        
        # Test de seguridad para verificar el estado de la base de datos
        client.server_info()
        print(">>> [DATABASE] Conexión establecida con éxito a MongoDB Local.")
        return db
    except Exception as e:
        print(f">>>> [DATABASE] Error crítico al conectar a MongoDB: {e}")
        return None