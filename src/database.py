from pymongo import MongoClient
import chromadb
from config import Config

class Database:
    def __init__(self):
        # MongoDB Atlas
        self.mongo_client = MongoClient(Config.MONGO_URI)
        self.db = self.mongo_client[Config.DB_NAME]
        self.products = self.db['products']
        self.logs = self.db['logs']
        
        # Local ChromaDB
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.chroma_client.create_collection(Config.CHROMA_COLLECTION, get_or_create=True)

    def add_product(self, embedding, metadata, product_id):
        try:
            self.collection.add(embeddings=embedding.tolist(), ids=[product_id])
            metadata["embedding_id"] = product_id
            self.products.insert_one(metadata)
            return True
        except Exception as e:
            self.logs.insert_one({"error": str(e)})
            return False

    def find_product(self, product_id):
        return self.products.find_one({"embedding_id": product_id})

    def query_vector(self, embedding):
        return self.collection.query(query_embeddings=embedding.tolist(), n_results=1)

    def log_error(self, error):
        self.logs.insert_one({"error": str(error)})