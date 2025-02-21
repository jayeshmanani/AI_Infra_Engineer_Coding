# AI_Infra_Engineer_Coding

# Product Matching System

This project implements an end-to-end product matching system using a CLIP model, ChromaDB for vector storage, MongoDB Atlas for metadata and logging and fastAPI to use the final application. It supports flexible product search with image, text, or both, served via a FastAPI web interface.

## Features
- **Vector Database**: ChromaDB stores visual and textual embeddings for efficient nearest neighbor search.
- **Metadata Storage**: MongoDB Atlas stores product metadata (name, category, price, filename).
<!-- - **Model Quantization**: CLIP model quantized with PyTorch for CPU compatibility (TensorRT mocked due to no GPU). -->
<!-- - **Mock Triton**: FastAPI endpoint simulates Triton Inference Server for embedding extraction. -->
- **Matching Pipeline**: Supports image-only, text-only, or combined searches with weighted scoring.
- **Logging**: Errors and execution results logged to MongoDB Atlas and a local file.
- **Web Interface**: FastAPI with Jinja2 templates for adding and searching products.

## Prerequisites
- **Operating System**: Windows, macOS, or Linux.
- **Python**: Version 3.9 or higher.
- **MongoDB Atlas**: A free-tier cluster for metadata and logging (no local MongoDB needed).
- **Internet**: Required for MongoDB Atlas connectivity.
<!-- - **No GPU Required**: Runs on CPU with PyTorch quantization. -->


# Steps to Setup the whole application


## Start the FastAPI server with Uvicorn:
'''uvicorn app:app --host 0.0.0.0 --port 8000'''