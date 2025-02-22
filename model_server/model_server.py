from fastapi import FastAPI, File, UploadFile, Form
from src.model import ProductModel
import numpy as np
from PIL import Image
import io
import os

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
model = ProductModel()

@app.post("/infer")
async def infer(image: UploadFile = File(None), text: str = Form(None)):
    logger.info(f"Received in infer: image={image.filename if image is not None else None}, text={text}")
    image_path = "temp_image.jpg"
    """Mock Triton inference endpoint for image and text embeddings."""
    try:
        print("Inference Start")
        print(f"Received: image={image}, text={text}")  # Debug print
        if image is None and text is None:
            return {"error": "Provide image, text, or both for inference"}
        
        if image is not None and text is not None:
            image_content = await image.read()
            image_file = io.BytesIO(image_content)
            
            with open(image_path, "wb") as f:
                f.write(image_file.read())
            image_embeds = model.get_image_embeddings(image_path)
            text_embeds = model.get_text_embeddings(text)
            return {"image_embeds": image_embeds.tolist(), "text_embeds": text_embeds.tolist()}
        elif image:
            image_content = await image.read()
            image_file = io.BytesIO(image_content)
            image_path = "temp_image.jpg"
            with open(image_path, "wb") as f:
                f.write(image_file.read())
            image_embeds = model.get_image_embeddings(image_path)
            return {"image_embeds": image_embeds.tolist()}
        elif text:
            text_embeds = model.get_text_embeddings(text)
            return {"text_embeds": text_embeds.tolist()}
    except Exception as e:
        print("Error Comes here in Model Server Infer", e)
        return {"error": str(e)}
    finally:
        if os.path.exists(image_path):
            os.remove(image_path)
