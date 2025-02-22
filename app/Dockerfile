FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY app/requirements.txt .
RUN pip install -r requirements.txt

# Copy app files
COPY app/app.py .
COPY src/ ./src/
COPY templates/ ./templates/

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]