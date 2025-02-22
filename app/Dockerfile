FROM python:3.9-slim

WORKDIR /app
COPY app/requirements.txt .
RUN pip install -r requirements.txt

# Only copy static files initially; volumes will override source code
COPY app/app.py .
COPY src/ ./src/
COPY templates/ ./templates/

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]