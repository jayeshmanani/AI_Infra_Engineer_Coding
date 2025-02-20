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
            
            embedding = self.model.get_embeddings(image_path)
            # print('Embedding:', embedding)
            product_id = metadata.get("id", str(np.random.randint(10000)))
            print("product id is:", product_id)
            self.db.add_product(embedding, metadata, product_id)
            print('Now Worked')
            self.logger.info(f"Added product: {product_id}")
            return True
        except Exception as e:
            self.logger.error(f"Add failed: {e}")
            self.db.log_error(e)
            return False

    def match_product(self, image_path):
        try:
            print('Now Working in Match Product', image_path)
            embedding = self.model.get_embeddings(image_path)
            result = self.db.query_vector(embedding)
            match_id = result['ids'][0][0]
            metadata = self.db.find_product(match_id)
            self.logger.info(f"Match found: {match_id}")
            return {
                "product_id": match_id,
                "metadata": metadata,
                "distance": result['distances'][0][0]
            }
        except Exception as e:
            self.logger.error(f"Match failed: {e}")
            self.db.log_error(e)
            return None