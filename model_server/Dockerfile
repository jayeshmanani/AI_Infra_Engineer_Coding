FROM python:3.9-slim

WORKDIR /app
COPY model_server/requirements.txt .
RUN pip install -r requirements.txt

COPY model_server/model_server.py .
COPY src/model.py .

CMD ["uvicorn", "model_server:app", "--host", "0.0.0.0", "--port", "8001"]