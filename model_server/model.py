from transformers import CLIPProcessor, CLIPModel
import torch
from PIL import Image

class ProductModel:
    def __init__(self):
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

        print("Quantizing model components for CPU compatibility (mocking TensorRT)...")
        self.model.vision_model = torch.quantization.quantize_dynamic(
            self.model.vision_model, {torch.nn.Linear}, dtype=torch.qint8
        )
        self.model.text_model = torch.quantization.quantize_dynamic(
            self.model.text_model, {torch.nn.Linear}, dtype=torch.qint8
        )
        self.model.visual_projection = torch.quantization.quantize_dynamic(
            self.model.visual_projection, {torch.nn.Linear}, dtype=torch.qint8
        )
        self.model.text_projection = torch.quantization.quantize_dynamic(
            self.model.text_projection, {torch.nn.Linear}, dtype=torch.qint8
        )
        self.model.eval()

    def get_image_embeddings(self, image_path):
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
            raise ValueError(f"Failed to get Image embeddings: {str(e)}")
        

    def get_text_embeddings(self, text):
        try:
            inputs = self.processor(text=[text], return_tensors="pt", padding=True, truncation=True)
            with torch.no_grad():
                text_outputs = self.model.text_model(
                    input_ids=inputs['input_ids'],
                    attention_mask=inputs['attention_mask']
                )
                text_embeds = text_outputs.pooler_output
                text_embeds = self.model.text_projection(text_embeds)
            return text_embeds.numpy()
        except Exception as e:
            raise ValueError(f"Failed to get text embeddings: {str(e)}")