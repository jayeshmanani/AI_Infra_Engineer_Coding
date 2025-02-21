from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.api import router as api_router  # Import API routes from src/api.py

app = FastAPI()

# Mount the data/ folder for static images
app.mount("/data", StaticFiles(directory="data"), name="data")

# Include API routes from src/api.py
app.include_router(api_router)