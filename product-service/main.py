from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(title="Product Service", version="1.0.0")

# In-memory database (in production, use Azure Cosmos DB or SQL)
products_db = {
    "1": {"id": "1", "name": "Laptop", "price": 999.99, "category": "Electronics"},
    "2": {"id": "2", "name": "Mouse", "price": 29.99, "category": "Electronics"},
    "3": {"id": "3", "name": "Keyboard", "price": 79.99, "category": "Electronics"}
}

class Product(BaseModel):
    id: str
    name: str
    price: float
    category: str

class ProductCreate(BaseModel):
    name: str
    price: float
    category: str

@app.get("/health")
async def health_check():
    """Health check endpoint for Azure monitoring"""
    return {"status": "healthy", "service": "product-service"}

@app.get("/products", response_model=List[Product])
async def get_products(category: Optional[str] = None):
    """Get all products, optionally filtered by category"""
    products = list(products_db.values())
    if category:
        products = [p for p in products if p["category"] == category]
    return products

@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    """Get a specific product by ID"""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    return products_db[product_id]

@app.post("/products", response_model=Product, status_code=201)
async def create_product(product: ProductCreate):
    """Create a new product"""
    product_id = str(len(products_db) + 1)
    new_product = Product(id=product_id, **product.dict())
    products_db[product_id] = new_product.dict()
    return new_product

@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: str, product: ProductCreate):
    """Update an existing product"""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    
    updated_product = Product(id=product_id, **product.dict())
    products_db[product_id] = updated_product.dict()
    return updated_product

@app.delete("/products/{product_id}")
async def delete_product(product_id: str):
    """Delete a product"""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    
    del products_db[product_id]
    return {"message": "Product deleted successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)