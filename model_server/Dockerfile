FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY model_server/requirements.txt .
RUN apt-get update && apt-get install -y curl && pip install -r requirements.txt

# Pre-download CLIP model
RUN python -c "from transformers import CLIPModel, CLIPProcessor; CLIPModel.from_pretrained('openai/clip-vit-base-patch32'); CLIPProcessor.from_pretrained('openai/clip-vit-base-patch32')"

# Copy model server files
COPY model_server/model_server.py .
COPY model_server/model.py .

CMD ["uvicorn", "model_server:app", "--host", "0.0.0.0", "--port", "8001"]