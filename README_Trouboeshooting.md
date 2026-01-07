# Order Service - Setup & Troubleshooting

## Quick Start

### Running the Service

```bash
# Navigate to the order-service directory
cd order-service

# Activate virtual environment (if not already activated)
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows

# Run the service
python main.py
```

The service will start on `http://0.0.0.0:8002`

## Common Issues & Solutions

### Issue 1: Import Errors in VSCode

**Symptoms:**

```
Import "fastapi" could not be resolved
Import "pydantic" could not be resolved
Import "httpx" could not be resolved
Import "uvicorn" could not be resolved
"app" is not defined
```

**Root Cause:** VSCode is not using the correct Python interpreter, or packages are not installed in the active environment.

**Solution:**

1. **Select Python Interpreter:**
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type "Python: Select Interpreter"
   - Select your virtual environment (`./venv/bin/python`)

2. **Install Required Packages:**

   ```bash
   pip install fastapi uvicorn httpx pydantic python-multipart
   ```

3. **Reload VSCode:**
   - Press `Ctrl+Shift+P` → "Developer: Reload Window"

### Issue 2: "can't open file 'main.py': No such file or directory"

**Error Message:**

```
/Library/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python: can't open file '/Users/username/azure-microservices-demo/main.py': [Errno 2] No such file or directory
```

**Root Cause:** Running `python main.py` from the wrong directory. The `main.py` file is located in the `order-service/` subdirectory, not the root project directory.

**Solution:**

```bash
# Option 1: Navigate to the correct directory
cd order-service
python main.py

# Option 2: Run from root directory with path
python order-service/main.py
```

**Why This Happens:** The project structure has separate service directories:

```
azure-microservices-demo/
├── order-service/
│   └── main.py        ← Your file is here
├── product-service/
│   └── main.py
└── README.md
```

### Issue 3: Code Errors in main.py

**Common Typos Fixed:**

1. **Line 96:** Path parameter syntax

   ```python
   # ❌ Wrong
   @app.get("/orders/[order_id}")
   
   # ✅ Correct
   @app.get("/orders/{order_id}")
   ```

2. **Line 108:** Typo in field name

   ```python
   # ❌ Wrong
   o["cutomer_id"]
   
   # ✅ Correct
   o["customer_id"]
   ```

3. **Line 117:** Typo in variable name

   ```python
   # ❌ Wrong
   if status not in valiid_statuses:
   
   # ✅ Correct
   if status not in valid_statuses:
   ```

4. **CORS Middleware Placement:**

   ```python
   # ✅ Correct order
   app = FastAPI(title="Order Service", version="1.0.0")
   
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

   **Note:** Middleware must be added AFTER creating the `app` instance.

## Testing with Postman

### Health Check

```
GET http://localhost:8002/health
```

**Expected Response:**

```json
{
  "status": "healthy",
  "service": "order-service"
}
```

### Create Order

```
POST http://localhost:8002/orders
Content-Type: application/json

{
  "customer_id": "customer_123",
  "items": [
    {
      "product_id": "1",
      "quantity": 2
    }
  ]
}
```

### Get Order by ID

```
GET http://localhost:8002/orders/{order_id}
```

### Get All Orders

```
GET http://localhost:8002/orders
```

### Get Orders by Customer

```
GET http://localhost:8002/orders?customer_id=customer_123
```

### Update Order Status

```
PATCH http://localhost:8002/orders/{order_id}/status?status=confirmed
```

Valid statuses: `pending`, `confirmed`, `shipped`, `delivered`, `canceled`

## Dependencies

```txt
fastapi==0.109.0
uvicorn==0.27.0
httpx==0.26.0
pydantic==2.5.0
python-multipart==0.0.6
```

## Environment Variables

- `PRODUCT_SERVICE_URL`: URL of the Product Service (default: `http://localhost:8001`)

## Notes

- The service runs on port `8002`
- Product validation requires the Product Service to be running on port `8001`
- Orders are stored in-memory (will reset on restart)
