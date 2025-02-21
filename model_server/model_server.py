from fastapi import FastAPI, File, UploadFile
from src.model import ProductModel
import numpy as np
from PIL import Image
import io
import os

app = FastAPI()
model = ProductModel()

@app.post("/infer")
async def infer(image: UploadFile = File(None), text: str = None):
    """Mock Triton inference endpoint for image and text embeddings."""
    try:
        if not image and not text:
            return {"error": "Provide image, text, or both for inference"}
        
        if image and text:
            image_content = await image.read()
            image_file = io.BytesIO(image_content)
            image_path = "temp_image.jpg"
            with open(image_path, "wb") as f:
                f.write(image_file.read())
            image_embeds = model.get_image_embeddings(image_path)
            text_embeds = model.get_text_embeddings(text)
            os.remove(image_path)
            return {"image_embeds": image_embeds.tolist(), "text_embeds": text_embeds.tolist()}
        elif image:
            image_content = await image.read()
            image_file = io.BytesIO(image_content)
            image_path = "temp_image.jpg"
            with open(image_path, "wb") as f:
                f.write(image_file.read())
            image_embeds = model.get_image_embeddings(image_path)
            os.remove(image_path)
            return {"image_embeds": image_embeds.tolist()}
        elif text:
            text_embeds = model.get_text_embeddings(text)
            return {"text_embeds": text_embeds.tolist()}
    except Exception as e:
        return {"error": str(e)}