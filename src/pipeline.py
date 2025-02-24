import numpy as np
from src.database import Database
from src.logger import setup_logger
from src.config import Config
import requests
import os

MODEL_SERVER_URL = os.getenv("MODEL_SERVER_URL", "http://localhost:8001/infer")

class ProductPipeline:
    def __init__(self):
        self.logger = setup_logger()
        self.db = Database()
        self.model_server_url = MODEL_SERVER_URL

    def add_product(self, image_path, metadata):
        try:
            with open(image_path, "rb") as f:
                triton_response = requests.post(
                    self.model_server_url,
                    files={"image": f},
                    data={"text": f"{metadata['name']} {metadata['category']}"}
                )
                triton_response.raise_for_status()
                response_data = triton_response.json()
                image_embedding = np.array(response_data["image_embeds"])
                text_embedding = np.array(response_data["text_embeds"])
            
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
            
            files = {}
            data = {}
            if image_path:
                with open(image_path, "rb") as f:
                    files = {"image": ("image.jpg", f.read())}
                self.logger.info(f"Sending image_path: {image_path}")
            if text:
                data = {"text": text}
                self.logger.info(f"Sending text: {text}")
            
            self.logger.info(f"Requesting {self.model_server_url} with files={list(files.keys())}, data={data}")

            triton_response = requests.post(
                self.model_server_url,
                files=files,
                data=data,
                timeout=10
            )
            self.logger.info(f"Response status: {triton_response.status_code}, content: {triton_response.text}")
            triton_response.raise_for_status()
            response_data = triton_response.json()
            
            image_embedding = response_data.get("image_embeds")
            text_embedding = response_data.get("text_embeds")
            
            result = self.db.query_vector(image_embedding=np.array(image_embedding, dtype=np.float32) if image_embedding is not None else None, 
                                          text_embedding=np.array(text_embedding, dtype=np.float32) if text_embedding is not None else None)
            
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
            print('Error Comes here in Pipeline,', e)
            self.db.log_error(e)
            return None