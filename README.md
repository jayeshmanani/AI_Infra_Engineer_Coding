# AI_Infra_Engineer_Coding

# Product Matching System

This project implements an end-to-end product matching system using a CLIP model, ChromaDB for vector storage, MongoDB Atlas for metadata and logging and fastAPI to use the final application. It supports flexible product search with image, text, or both, served via a FastAPI web interface.

## Features
- **Vector Database**: ChromaDB stores visual and textual embeddings for efficient nearest neighbor search.
- **Metadata Storage**: MongoDB Atlas stores product metadata (name, category, price, filename).
- **Matching Pipeline**: Supports image-only, text-only, or combined searches with weighted scoring.
- **Logging**: Errors and execution results logged to MongoDB Atlas and a local file.
- **Web Interface**: FastAPI with Jinja2 templates for adding and searching products.

## Prerequisites
- **Operating System**: Windows, macOS, or Linux.
- **Python**: Version 3.9 or higher.
- **MongoDB Atlas**: A free-tier cluster for metadata and logging (no local MongoDB needed).
- **Internet**: Required for MongoDB Atlas connectivity.


# Run the Application
## Start the FastAPI server with Uvicorn:
'''uvicorn app:app --host 0.0.0.0 --port 8000'''