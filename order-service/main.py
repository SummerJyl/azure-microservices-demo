from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime
import httpx
import uvicorn
import os

app = FastAPI(title="Order Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Configuration for service communication
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://localhost:8001")
print(f"🔍 DEBUG: PRODUCT_SERVICE_URL = {PRODUCT_SERVICE_URL}")

orders_db = {}
order_counter = 1

class OrderItem(BaseModel):
    product_id: str
    quantity: int

class Order(BaseModel):
    id: str
    customer_id: str
    items: List[OrderItem]
    total: float
    status: str
    created_at: str

class OrderCreate(BaseModel):
    customer_id: str
    items: List[OrderItem]

@app.get("/health")
async def health_check():
    """Health Check endpoint"""
    return {"status": "healthy", "service": "order-service"}
    
@app.post("/orders", response_model=Order, status_code=201)
async def create_order(order: OrderCreate):
    """ 
    Create a new order

    Steps:
    1. Validate products exist (call Product Service)
    2. Calculate total price
    3. Create order
    """
    global order_counter
    
    #Step 1 & 2: Validate products and calculate total
    total = 0.0
    async with httpx.AsyncClient(verify=False) as client:
        for item in order.items:
            try:
                # Call Product Service to get product details
                response = await client.get(
                    f"{PRODUCT_SERVICE_URL}/products/{item.product_id}",
                    timeout=5.0
                )
                if response.status_code == 200:
                    product = response.json()
                    total += product["price"] * item.quantity
                elif response.status_code == 404:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Product {item.product_id} not found"
                    )
                else:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Error fetching product {item.product_id}"
                    )

            except httpx.RequestError as e:
                    # Product Service is down or unreachable
                    raise HTTPException(
                        status_code=503,
                        detail=f"Product Service unavailable: {str(e)}"
                    )   
    # Step 3: Create order
    order_id = str(order_counter)
    order_counter += 1

    new_order = Order(
        id=order_id,
        customer_id=order.customer_id,
        items=order.items,
        total=round(total, 2),
        status="pending",
        created_at=datetime.utcnow().isoformat()
    )             

    orders_db[order_id] = new_order.dict()

    return new_order

@app.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: str):
    """Get order by ID"""
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders_db[order_id]

@app.get("/orders", response_model=List[Order])
async def get_orders(customer_id: str = None):
    """Get all orders, optionally filtered by customer"""
    orders = list(orders_db.values())
    if customer_id:
        orders = [o for o in orders if o["customer_id"] == customer_id]
    return orders

@app.patch("/orders/{order_id}/status")
async def update_order_status(order_id: str, status: str):
    """Update order status"""
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")

    valid_statuses = ["pending", "confirmed", "shipped", "delivered", "canceled"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of {valid_statuses}"
        )
        
    orders_db[order_id]["status"] = status
    return {"message": f"Order {order_id} status updated to {status}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)


