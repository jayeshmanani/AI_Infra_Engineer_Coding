from fastapi import FastAPI, File, UploadFile, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.pipeline import ProductPipeline
import os
import json

router = APIRouter()
pipeline = ProductPipeline()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    # Fetch all products from MongoDB
    products = list(pipeline.db.products.find())
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "products": products}
    )

@router.post("/add_product")
async def add_product(
    request: Request,
    name: str = Form(...),
    category: str = Form(...),
    price: float = Form(...),
    file: UploadFile = File(...)
):
    try:
        # Save uploaded file in data/
        os.makedirs("data", exist_ok=True)
        temp_path = f"data/{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(await file.read())
        
        metadata = {
            "name": name,
            "category": category,
            "price": price,
            "filename": file.filename  # Store filename for display
        }
        print("Temp Path", temp_path, "Metadata", metadata) 
        success = pipeline.add_product(temp_path, metadata)
        if not success:
            raise Exception("Failed to add product")
        
        # Redirect to homepage
        products = list(pipeline.db.products.find())
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "products": products, "message": "Product added successfully"}
        )
    except Exception as e:
        products = list(pipeline.db.products.find())
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "products": products, "error": str(e)}
        )

@router.post("/match_product")
async def match_product(request: Request, file: UploadFile = File(...)):
    try:
        # Save uploaded file temporarily in data/
        os.makedirs("data", exist_ok=True)
        temp_path = f"data/temp_{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(await file.read())
        
        result = pipeline.match_product(temp_path)
        os.remove(temp_path)  # Clean up temp file
        
        products = list(pipeline.db.products.find())
        if result:
            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "products": products,
                    "match": result["metadata"],
                    "distance": result["distance"]
                }
            )
        else:
            return templates.TemplateResponse(
                "index.html",
                {"request": request, "products": products, "error": "No match found"}
            )
    except Exception as e:
        products = list(pipeline.db.products.find())
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "products": products, "error": str(e)}
        )