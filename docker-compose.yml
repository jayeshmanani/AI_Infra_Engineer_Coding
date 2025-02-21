version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: app/Dockerfile
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    depends_on:
      - model-server
    environment:
      - PYTHONUNBUFFERED=1
    tty: true
    stdin_open: true

  model-server:
    build:
      context: .
      dockerfile: model_server/Dockerfile
    ports:
      - "8001:8001"
    environment:
      - PYTHONUNBUFFERED=1
    tty: true
    stdin_open: true