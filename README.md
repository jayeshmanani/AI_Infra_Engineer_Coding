# AI_Infra_Engineer_Coding

# Product Matching System

This project implements an end-to-end product matching system using a CLIP model, ChromaDB for vector storage, MongoDB Atlas for metadata and logging and fastAPI to use the final application. It supports flexible product search with image, text, or both, served via a FastAPI web interface.

## Features
- **Vector Database**: ChromaDB stores visual and textual embeddings for efficient nearest neighbor search.
- **Metadata Storage**: MongoDB Atlas stores product metadata (name, category, price, filename).
- **Model Quantization**: CLIP model quantized with PyTorch for CPU compatibility (TensorRT mocked due to no GPU).
- **Mock Triton using the Model Server**: FastAPI endpoint simulates Triton Inference Server for embedding extraction.
- **Matching Pipeline**: Supports image-only, text-only, or combined searches with weighted scoring.
- **Logging**: Errors and execution results logged to MongoDB Atlas and a local file.
- **Web Interface**: FastAPI with Jinja2 templates for adding and searching products.

## Prerequisites
- **Operating System**: Windows, macOS, or Linux.
- **Python**: Version 3.9 or higher.
- **MongoDB Atlas**: A free-tier cluster for metadata and logging (no local MongoDB needed).
- **Internet**: Required for MongoDB Atlas connectivity.
- **No GPU Required**: Runs on CPU with PyTorch quantization.

# Before Start working on Project
## Pre-Requisite 
1. Docker Installation on the System

    One can follow this URL for docker system installation based on their system (Mac, Win, Linux)

    https://docs.docker.com/get-started/


2. Mongo Atlas account setup - Can follow this url for detailed process

    https://www.mongodb.com/docs/guides/atlas/connection-string/

    Once you get the Connection String, you can put it in the Config.py file of the project.


# Steps to Setup the whole application

1. Clone this Project from Github to your local system
2. Start Docker
3. Run Docker Compose from home directory of this project as follows

    ``docker-compose up --build``


4. After successful build of the application and creation of the container, you will be able to use the Application at http://localhost:8000/

Where you can upload few images, and can then use the match function to match the data by proving image or text or both as input to the fields given in the app.


The serving model is being deployed in different container then the actual app which is using the model server. So, there will be two different docker containers will be up and running after the successfull setup.

# Remove Evething from System and Clean the memory

You can go through this steps mentioned in this article which is in very details

https://medium.com/@aleksej.gudkov/how-to-clean-up-all-docker-caches-a-complete-guide-0d44d9333fa7



