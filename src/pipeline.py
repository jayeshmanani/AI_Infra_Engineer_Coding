import numpy as np
from src.model import ProductModel
from src.database import Database
from src.logger import setup_logger
from config import Config
from tritonclient.http import InferenceServerClient

class ProductPipeline:
    def __init__(self):
        self.logger = setup_logger()
        self.model = ProductModel()
        self.db = Database()
        self.triton_client = InferenceServerClient(url=Config.TRITON_URL)

    def add_product(self, image_path, metadata):
        try:
            # First we take out the embedding from the image
            image_embedding = self.model.get_image_embeddings(image_path)
            text_data = f"{metadata['name']} {metadata['category']}"
            text_embedding = self.model.get_text_embeddings(text_data)
            product_id = metadata.get("id", str(np.random.randint(10000)))
            self.db.add_product(image_embedding, text_embedding, metadata, product_id)
            self.logger.info(f"Added product: {product_id}")
            return True
        except Exception as e:
            self.logger.error(f"Add failed: {e}")
            self.db.log_error(e)
            return False

    def match_product(self, image_path=None, text=None):
        try:
            if not image_path and not text:
                raise ValueError("At least one of image or text must be provided")
            
            image_embedding = self.model.get_image_embeddings(image_path) if image_path is not None else None
            
            text_embedding = self.model.get_text_embeddings(text) if text is not None else None

            result = self.db.query_vector(image_embedding, text_embedding)
            match_id = result['ids'][0][0]
            metadata = self.db.find_product(match_id)

            self.logger.info(f"Match found: {match_id}")

            return {
                "product_id": match_id,
                "metadata": metadata,
                "distance": result["distances"][0][0] if result["distances"] else None
            }
        except Exception as e:
            self.logger.error(f"Match failed: {e}")
            print('Error Comes here,', e)
            self.db.log_error(e)
            return None