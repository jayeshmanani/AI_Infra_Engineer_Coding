import os
import numpy as np
from fastapi import FastAPI, File, UploadFile
from io import BytesIO
import chromadb
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from config import Config

# Initialize  the FastAPI app
app = FastAPI()

# Chromadb setup
chroma_client = chromadb.PersistentClient(path='./chroma_db')
collection = chroma_client.get_or_create_collection(name='test_collection')


# MongoDB setup
mongo_uri = f"mongodb+srv://{Config.MONGO_USERNAME}:{Config.MONGO_PASSWORD}@cluster0.hclcr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(mongo_uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

