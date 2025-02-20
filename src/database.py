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
        self.image_collection = self.chroma_client.create_collection(Config.IMAGE_COLLECTION, get_or_create=True)
        self.text_collection = self.chroma_client.create_collection(Config.TEXT_COLLECTION, get_or_create=True)

    def add_product(self, image_embedding, text_embedding, metadata, product_id):
        try:
            self.image_collection.add(embeddings=image_embedding.tolist(), ids=[product_id])
            self.text_collection.add(embeddings=text_embedding.tolist(), ids=[product_id])
            metadata["embedding_id"] = product_id
            self.products.insert_one(metadata)
            return True
        except Exception as e:
            self.logs.insert_one({"error": str(e)})
            return False

    def find_product(self, product_id):
        return self.products.find_one({"embedding_id": product_id})

    def query_vector(self, image_embedding=None, text_embedding=None):
        print(image_embedding is None)
        print(text_embedding is None)

        if image_embedding is None and text_embedding is None:
            raise ValueError("At least one embedding must be provided in Query Vector Search")
        
        if image_embedding is not None and text_embedding is not None:
            image_result = self.image_collection.query(query_embeddings=image_embedding.tolist(), n_results=1)
            text_result = self.text_collection.query(query_embeddings=text_embedding.tolist(), n_results=1)
            combined_distance = (image_result['distances'][0][0] + text_result['distances'][0][0]) / 2
            return {
                'ids': image_result['ids'],  # Assuming same order; could refine with more logic
                'distances': [[combined_distance]]
            }
        elif image_embedding is not None:
            return self.image_collection.query(query_embeddings=image_embedding.tolist(), n_results=1)
        elif text_embedding is not None:
            return self.text_collection.query(query_embeddings=text_embedding.tolist(), n_results=1)

    def log_error(self, error):
        self.logs.insert_one({"error": str(error)})