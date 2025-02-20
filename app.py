import os
import numpy as np
from fastapi import FastAPI, File, UploadFile
from io import BytesIO
import chromadb
import pymongo

# Initialize  the FastAPI app
app = FastAPI()

# Chromadb setup
chroma_client = chromadb.PersistentClient(path='./chroma_db')
collection = chroma_client.get_or_create_collection(name='test_collection')

collection.add(
    ids=['1', '2', '3'],
    embeddings=np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
    metadatas=[{'name': 'A'}, {'name': 'B'}, {'name': 'C'}]
)

results = collection.query(
    query_embeddings=np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
    n_results=2
)

print("Results Are : ", results)





