# Azure Microservices - Production Deployment

A production-ready microservices architecture built with FastAPI, Docker, and deployed to Render. Originally designed for Azure Container Apps, adapted for multi-cloud deployment.

## 🚀 Live Deployment

- **Product Service**: [Your Render URL]/docs
- **Order Service**: [Your Render URL]/docs
- **Architecture**: Microservices with REST API communication

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│         Client / Browser            │
└──────────────┬──────────────────────┘
               │
    ┌──────────▼──────────┐
    │   Order Service     │
    │   (Port 8002)       │
    └──────────┬──────────┘
               │ HTTP Request
               │ (validates products)
               │
    ┌──────────▼──────────┐
    │  Product Service    │
    │   (Port 8001)       │
    └─────────────────────┘
```

**Communication Flow:**

1. Client creates an order via Order Service
2. Order Service calls Product Service to validate products exist
3. Order Service calculates total based on product prices
4. Order is created and returned to client

## 📁 Project Structure

```
azure-microservices-demo/
├── product-service/
│   ├── main.py              # FastAPI product CRUD endpoints
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile          # Container configuration
├── order-service/
│   ├── main.py              # FastAPI order creation with validation
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile          # Container configuration
├── docker-compose.yml       # Local development orchestration
├── render.yaml             # Render deployment configuration
└── README.md               # This file
```

## 🛠️ Tech Stack

- **Framework**: FastAPI (async Python web framework)
- **Language**: Python 3.11
- **Containerization**: Docker
- **Orchestration (Local)**: Docker Compose
- **Deployment**: Render (cloud platform)
- **API Communication**: REST with httpx (async HTTP client)
- **Validation**: Pydantic schemas

## 🔧 Local Development

### Prerequisites

- Docker Desktop installed and running
- Python 3.11+ (for local development without Docker)

### Run Locally with Docker Compose

```bash
# Clone repository
git clone https://github.com/SummerJyl/azure-microservices-demo.git
cd azure-microservices-demo

# Start both services
docker-compose up --build

# Services available at:
# Product Service: http://localhost:8001
# Order Service: http://localhost:8002
```

### Run Locally without Docker

**Terminal 1 - Product Service:**

```bash
cd product-service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

**Terminal 2 - Order Service:**

```bash
cd order-service
source ../product-service/venv/bin/activate
pip install -r requirements.txt

# Set environment variable for service communication
export PRODUCT_SERVICE_URL=http://localhost:8001

python main.py
```

## 🚢 Deployment to Render

### Step 1: Prepare Repository

```bash
# Ensure all changes are committed
git add .
git commit -m "Ready for deployment"

# Push to GitHub
git push origin main
```

### Step 2: Deploy Product Service

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `product-service`
   - **Root Directory**: `product-service`
   - **Environment**: Docker
   - **Plan**: Free
5. Click **"Create Web Service"**
6. Wait for deployment (2-5 minutes)
7. Copy the service URL (e.g., `https://product-service-xxxx.onrender.com`)

### Step 3: Deploy Order Service

1. Click **"New +"** → **"Web Service"**
2. Connect same GitHub repository
3. Configure:
   - **Name**: `order-service`
   - **Root Directory**: `order-service`
   - **Environment**: Docker
   - **Plan**: Free
4. **Add Environment Variable**:
   - Key: `PRODUCT_SERVICE_URL`
   - Value: `https://product-service-xxxx.onrender.com` (your Product Service URL)
5. Click **"Create Web Service"**

### Step 4: Test Deployment

**Product Service:**

```bash
# Health check
curl https://product-service-xxxx.onrender.com/health

# Get all products
curl https://product-service-xxxx.onrender.com/products

# Interactive API docs
# Visit: https://product-service-xxxx.onrender.com/docs
```

**Order Service:**

```bash
# Health check
curl https://order-service-xxxx.onrender.com/health

# Create order
curl -X POST https://order-service-xxxx.onrender.com/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "customer123",
    "items": [
      {"product_id": "1", "quantity": 2},
      {"product_id": "2", "quantity": 1}
    ]
  }'
```

## 🐛 Bugs Fixed & Debugging Journey

### Git & Deployment Issues

#### Issue 1: Dockerfile Not Found

**Error:**

```
error: failed to solve: failed to read dockerfile: open Dockerfile: no such file or directory
```

**Root Cause**: Render couldn't find Dockerfile because Root Directory wasn't set.

**Fix**: Set **Root Directory** to `product-service` (or `order-service`) in Render settings.

**Lesson**: When deploying from a monorepo, always specify which subdirectory contains the service.

---

#### Issue 2: Code Not on GitHub

**Error:**

```
Root directory "product-service" does not exist
```

**Root Cause**: Local changes were committed but not pushed to GitHub. Render was looking at 3-month-old code.

**Debugging Steps:**

```bash
git status                    # Showed "ahead by 2 commits"
git remote -v                 # Verified correct remote
git push origin master:main   # Failed - conflicts!
```

**Fix**:

```bash
git pull origin main --rebase  # Got merge conflicts
git rebase --abort             # Aborted conflicts
git push origin master:main --force  # Force pushed local version
```

**Lesson**: Always verify code is pushed to GitHub before deploying. Use `git status` and check GitHub web interface.

---

#### Issue 3: Branch Mismatch (master vs main)

**Error:**

```
! [rejected] master -> main (fetch first)
```

**Root Cause**: Local branch was `master`, GitHub default was `main`.

**Fix**: Push local `master` to remote `main`:

```bash
git push origin master:main --force
```

**Alternative**: Rename local branch to match:

```bash
git branch -M main
git push -u origin main
```

**Lesson**: GitHub changed default branch from `master` to `main` in 2020. Always check which branch you're on and where you're pushing.

---

### Python/FastAPI Issues

#### Issue 4: Service Communication Failed (localhost in Docker)

**Error:**

```json
{
  "detail": "Product Service unavailable: All connection attempts failed"
}
```

**Root Cause**: Order Service was using `http://localhost:8001` to call Product Service, which doesn't work in separate Docker containers.

**Fix**: Change `PRODUCT_SERVICE_URL` in `order-service/main.py`:

```python
# Wrong (works locally, fails in Docker)
PRODUCT_SERVICE_URL = "http://localhost:8001"

# Correct (Docker network)
PRODUCT_SERVICE_URL = "http://product-service:8001"
```

**For Render deployment**: Use full URL as environment variable:

```
PRODUCT_SERVICE_URL=https://product-service-xxxx.onrender.com
```

**Lesson**: `localhost` only works within the same container. Use service names in Docker Compose, full URLs in cloud deployments.

---

#### Issue 5: HTTPException Typos

**Error:**

```
NameError: name 'HTTPExeception' is not defined
```

**Root Cause**: Multiple typos in error handling code:

- `HTTPExeception` (should be `HTTPException`)
- `HTTPExceptiion` (three i's instead of two)

**Fix**: Used Find & Replace to fix all instances:

```python
# Correct spelling
from fastapi import HTTPException

raise HTTPException(status_code=404, detail="Product not found")
```

**Lesson**: TypeScript would catch these at compile time, but Python only catches them at runtime. Use linters (pylint, mypy) to catch issues earlier.

---

#### Issue 6: Pydantic .dict() Deprecation

**Warning:**

```
PydanticDeprecatedSince20: The `dict` method is deprecated; use `model_dump` instead
```

**Root Cause**: Using Pydantic v2 with v1 syntax.

**Fix**:

```python
# Old (Pydantic v1)
new_order.dict()

# New (Pydantic v2)
new_order.model_dump()
```

**Lesson**: Check migration guides when upgrading major versions. Pydantic v2 introduced breaking changes.

---

### Docker Issues

#### Issue 7: Port Conflicts

**Error:**

```
Error: port is already allocated
```

**Root Cause**: Another service already using port 8001 or 8002.

**Fix**:

```bash
# Find process using port
lsof -i :8001

# Kill the process
kill -9 <PID>

# Or use different ports in docker-compose.yml
```

**Lesson**: Always check if ports are available before starting services.

---

#### Issue 8: Container Not Updating After Code Changes

**Issue**: Made code changes but container still running old code.

**Root Cause**: Docker was using cached image.

**Fix**:

```bash
# Stop containers
docker-compose down

# Rebuild without cache
docker-compose up --build

# Or force rebuild specific service
docker-compose build --no-cache product-service
```

**Lesson**: Use `--build` flag when restarting after code changes.

---

### Render-Specific Issues

#### Issue 9: Free Tier Spin-Down

**Behavior**: Service takes 30-60 seconds to respond after inactivity.

**Root Cause**: Render free tier spins down services after 15 minutes of inactivity.

**Impact**:

- First request after inactivity is slow
- Subsequent requests are fast

**Workaround**:

- Upgrade to paid tier ($7/month) for always-on
- Accept the delay for free tier
- Use external uptime monitor to keep service warm

**Lesson**: Understand limitations of free tiers. Document expected behavior for users.

---

#### Issue 10: Environment Variables Not Set

**Error:**

```
Order Service trying to reach localhost:8001
```

**Root Cause**: Forgot to set `PRODUCT_SERVICE_URL` environment variable in Render.

**Fix**:

1. Go to Order Service in Render
2. Click **"Environment"** tab
3. Add:
   - Key: `PRODUCT_SERVICE_URL`
   - Value: `https://product-service-xxxx.onrender.com`
4. Redeploy service

**Lesson**: Always set environment variables before first deployment, not after.

---

## 🎓 Key Learnings

### Microservices Patterns

- **Service Discovery**: Services need to know each other's URLs
- **Error Handling**: Graceful degradation when dependent services are down
- **Health Checks**: Essential for container orchestration
- **Service Communication**: Sync (REST) vs Async (message queues)

### Docker Best Practices

- Use multi-stage builds to reduce image size
- Don't use `localhost` for inter-service communication
- Always specify Python version in Dockerfile
- Use `.dockerignore` to exclude unnecessary files

### Git Workflow

- Commit often, push regularly
- Verify code is on GitHub before deploying
- Use `git status` to check for uncommitted changes
- Understand `master` vs `main` branch naming

### Deployment Strategy

- Deploy services in dependency order (Product before Order)
- Set environment variables before deploying
- Test each service individually before testing together
- Monitor logs during deployment

### Debugging Techniques

- Read error messages carefully - they're usually specific
- Check logs at each layer (code, Docker, platform)
- Use health check endpoints to verify services are running
- Test API endpoints with curl before building frontend

## 📊 API Documentation

### Product Service Endpoints

**Health Check**

```
GET /health
Response: {"status": "healthy", "service": "product-service"}
```

**Get All Products**

```
GET /products
Response: [
  {
    "id": "1",
    "name": "Laptop",
    "price": 999.99,
    "category": "Electronics"
  },
  ...
]
```

**Get Single Product**

```
GET /products/{product_id}
Response: {
  "id": "1",
  "name": "Laptop",
  "price": 999.99,
  "category": "Electronics"
}
```

**Create Product**

```
POST /products
Body: {
  "name": "New Product",
  "price": 49.99,
  "category": "Category"
}
Response: Product object with generated ID
```

### Order Service Endpoints

**Health Check**

```
GET /health
Response: {"status": "healthy", "service": "order-service"}
```

**Create Order**

```
POST /orders
Body: {
  "customer_id": "customer123",
  "items": [
    {"product_id": "1", "quantity": 2},
    {"product_id": "2", "quantity": 1}
  ]
}
Response: {
  "id": "1",
  "customer_id": "customer123",
  "items": [...],
  "total": 2029.97,
  "status": "pending",
  "created_at": "2026-01-04T12:00:00"
}
```

**Get Order**

```
GET /orders/{order_id}
Response: Order object
```

**Get All Orders**

```
GET /orders?customer_id=customer123
Response: Array of Order objects
```

## 🎯 Interview Talking Points

**Q: "Tell me about a microservices project you've deployed to production."**

*"I built and deployed an e-commerce microservices system with FastAPI and Docker. The architecture consists of a Product Service for catalog management and an Order Service that validates products and calculates totals by making HTTP requests to the Product Service. I containerized both services with Docker and deployed them to Render's cloud platform. During deployment, I debugged several issues including Docker networking (localhost doesn't work between containers), Git branch mismatches, and environment variable configuration. The services are now live and handle RESTful API requests with proper error handling for scenarios like invalid products or when dependent services are unavailable. The project demonstrates service-to-service communication, proper HTTP status codes, and production-ready error handling."*

**Q: "How do you debug deployment issues?"**

*"I follow a systematic approach. First, I verify the code is actually on GitHub since deployment platforms pull from there - I once debugged for 30 minutes only to realize my latest commits weren't pushed. Second, I check the build logs carefully for specific error messages rather than just seeing 'failed'. Third, I test each layer independently - does it work locally? In Docker? With Docker Compose? Then finally in production. For the microservices project, I encountered a 'Dockerfile not found' error which was actually a Root Directory configuration issue, and a service communication failure that was due to using localhost URLs instead of service URLs. Reading error messages carefully and testing incrementally helped me fix issues quickly."*

**Q: "What's your approach to service-to-service communication?"**

*"I use synchronous REST calls for operations requiring immediate responses, like validating products before creating an order. I implement proper error handling with timeouts and fallbacks - if the Product Service is down, the Order Service returns a 503 Service Unavailable instead of crashing. For production, I'd add circuit breakers and retry logic with exponential backoff. For non-critical operations, I'd use asynchronous communication with message queues like Azure Service Bus or RabbitMQ - for example, publishing an 'order.created' event that the Inventory Service subscribes to for stock updates. This decouples services and improves resilience. The key is understanding when to use sync vs async based on business requirements and consistency needs."*

## 🚀 Future Enhancements

- [ ] Add database persistence (PostgreSQL on Render)
- [ ] Implement API Gateway with authentication
- [ ] Add Redis caching layer
- [ ] Implement distributed tracing (OpenTelemetry)
- [ ] Add CI/CD pipeline (GitHub Actions)
- [ ] Implement circuit breaker pattern (resilience)
- [ ] Add message queue (RabbitMQ or Redis)
- [ ] Create monitoring dashboard (Grafana)
- [ ] Add rate limiting per customer
- [ ] Implement saga pattern for distributed transactions
- [ ] Add comprehensive test suite (pytest)
- [ ] Create load testing scenarios (Locust)

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Render Documentation](https://render.com/docs)
- [Microservices Patterns](https://microservices.io/patterns/)
- [REST API Best Practices](https://restfulapi.net/)

## 👨‍💻 Author

**Jylian Summers**
Senior Full Stack Engineer

Built as part of structured skill maintenance program focusing on microservices architecture, containerization, and cloud deployment.

## 📄 License

This project is open source and available for educational purposes.

---

**Deployed Live:** January 4, 2026
**Platform:** Render (cloud deployment)
**Status:** Production-ready microservices architecture
