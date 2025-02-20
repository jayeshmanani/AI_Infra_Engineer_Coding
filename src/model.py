from transformers import CLIPProcessor, CLIPModel
import torch
from PIL import Image

class ProductModel:
    def __init__(self):
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    def get_embeddings(self, image_path):
        try:
            # Open and process the image
            image = Image.open(image_path).convert('RGB')
            inputs = self.processor(images=image, return_tensors="pt")

            # Extract image embeddings using the vision model
            with torch.no_grad():
                # Use only the vision model to get image embeddings
                vision_outputs = self.model.vision_model(pixel_values=inputs['pixel_values'])
                image_embeds = vision_outputs.pooler_output  # Pooled output from vision transformer
                image_embeds = self.model.visual_projection(image_embeds)  # Project to common space
            return image_embeds.numpy()
        except Exception as e:
            raise ValueError(f"Failed to get embeddings: {str(e)}")