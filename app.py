from src.pipeline import ProductPipeline

def main():
    pipeline = ProductPipeline()
    sample_product = {
        "id": "1",
        "name": "Sample Shirt",
        "category": "Clothing",
        "price": 29.99
    }
    
    pipeline.add_product("sample_image.jpg", sample_product)
    result = pipeline.match_product("test_image.jpg")
    if result:
        print(f"Found match: {result['metadata']['name']}")
    else:
        print("No match found")

if __name__ == "__main__":
    main()