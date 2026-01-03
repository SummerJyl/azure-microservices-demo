# Azure Microservices Demo

A production-ready microservices architecture built with FastAPI, Docker, and designed for Azure deployment. This project demonstrates service-to-service communication, error handling, and containerization best practices.

## 🏗️ Architecture

```
┌─────────────────┐
│   API Gateway   │  (Future: Azure API Management)
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼────┐ ┌──▼─────┐
│Product │ │ Order  │
│Service │◄┤Service │
└────────┘ └────────┘
```

**Product Service**: Manages product catalog, pricing, and inventory
**Order Service**: Creates orders, validates products, calculates totals

## 🚀 Tech Stack

- **Framework**: FastAPI (Python 3.11)
- **Containerization**: Docker & Docker Compose
- **API Testing**: Postman
- **Cloud Platform**: Azure (Container Apps, Container Registry)
- **Communication**: REST APIs with async/await
- **Validation**: Pydantic schemas

## ✨ Features

- ✅ **Service-to-Service Communication**: Order Service calls Product Service via HTTP
- ✅ **Data Validation**: Pydantic schemas ensure type safety and validation
- ✅ **Error Handling**: Graceful handling of service failures and invalid data
- ✅ **Health Checks**: Monitoring endpoints for container orchestration
- ✅ **Auto-Generated API Docs**: Swagger UI at `/docs`
- ✅ **Async Support**: Non-blocking I/O for better performance
- ✅ **Docker Networking**: Services communicate via container names

## 📁 Project Structure

```
azure-microservices-demo/
├── docker-compose.yml
├── product-service/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
└── order-service/
    ├── main.py
    ├── requirements.txt
    └── Dockerfile
```

## 🏃‍♂️ Running Locally

### Prerequisites
- Docker Desktop installed and running
- Python 3.11+ (for local development)
- Postman (optional, for API testing)

### Quick Start with Docker

```bash
# Clone the repository
cd azure-microservices-demo

# Start both services
docker-compose up --build

# Services will be available at:
# Product Service: http://localhost:8001
# Order Service: http://localhost:8002
```

### Run Without Docker (Development)

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
python main.py
```

## 🧪 Testing the APIs

### Using Browser
- Product Service Docs: http://localhost:8001/docs
- Order Service Docs: http://localhost:8002/docs

### Using Postman

**1. Health Checks**
```
GET http://localhost:8001/health
GET http://localhost:8002/health
```

**2. Get All Products**
```
GET http://localhost:8001/products
```

**3. Get Single Product**
```
GET http://localhost:8001/products/1
```

**4. Create an Order**
```
POST http://localhost:8002/orders
Content-Type: application/json

{
  "customer_id": "customer123",
  "items": [
    {
      "product_id": "1",
      "quantity": 2
    },
    {
      "product_id": "2",
      "quantity": 1
    }
  ]
}
```

**Expected Response:**
```json
{
  "id": "1",
  "customer_id": "customer123",
  "items": [...],
  "total": 2029.97,
  "status": "pending",
  "created_at": "2025-12-30T01:28:39.875500"
}
```

## 🎯 Key Learning Points

### Microservices Communication
- Order Service validates products by calling Product Service
- Uses `httpx` for async HTTP requests
- Implements timeout and retry logic

### Error Handling
- **404**: Product not found
- **422**: Invalid request data
- **503**: Product Service unavailable

### Docker Networking
- Services communicate using service names (`http://product-service:8001`)
- Bridge network isolates services
- Health checks ensure container readiness

## 🔮 Future Enhancements

- [ ] Add Azure Service Bus for event-driven architecture
- [ ] Implement API Gateway with Azure API Management
- [ ] Add authentication with Azure AD
- [ ] Deploy to Azure Container Apps
- [ ] Add monitoring with Application Insights
- [ ] Implement distributed tracing with correlation IDs
- [ ] Add database persistence (Azure Cosmos DB / PostgreSQL)
- [ ] Implement circuit breaker pattern
- [ ] Add rate limiting
- [ ] Create Kubernetes manifests for AKS

## 📊 Interview Talking Points

**Q: "Tell me about a microservices project you've built."**

*"I built an e-commerce microservices system with FastAPI and Docker. The Product Service manages the catalog, while the Order Service handles order creation and validation. When creating an order, the Order Service asynchronously calls the Product Service to validate products and calculate totals. I implemented proper error handling for scenarios like invalid products or when the Product Service is unavailable, returning appropriate HTTP status codes. Everything is containerized with Docker Compose and designed for deployment to Azure Container Apps."*

**Q: "How do your microservices communicate?"**

*"I use synchronous REST API calls for operations that need immediate responses, like validating products exist before creating an order. For future enhancements, I'd add Azure Service Bus for asynchronous communication - for example, publishing an 'order.created' event that the Inventory Service would subscribe to for stock updates. This decouples services and improves resilience."*

**Q: "How do you handle failures between services?"**

*"I implement proper error handling with httpx. If the Product Service is unreachable, the Order Service returns a 503 Service Unavailable with a clear error message instead of crashing. I also use timeouts to prevent requests from hanging indefinitely. In production, I'd add circuit breakers and retry logic with exponential backoff."*

## 🛠️ Technologies & Patterns

**Design Patterns:**
- Microservices Architecture
- Service-to-Service Communication
- Health Check Pattern
- API Gateway Pattern (planned)
- Event-Driven Architecture (planned)

**Best Practices:**
- Schema validation with Pydantic
- Async/await for I/O operations
- Docker multi-stage builds
- Environment-based configuration
- Proper HTTP status codes
- Auto-generated API documentation

## 📝 Development Log

**Day 1: Core Services**
- ✅ Built Product Service with CRUD operations
- ✅ Built Order Service with product validation
- ✅ Implemented service-to-service communication
- ✅ Added comprehensive error handling

**Day 2: Containerization**
- ✅ Dockerized both services
- ✅ Created Docker Compose configuration
- ✅ Tested inter-service communication in containers
- ✅ Validated health checks

**Next Steps:**
- Azure deployment with Container Apps
- Add Azure Service Bus for event-driven architecture
- Implement monitoring and logging

## 👨‍💻 Author

**Jylian Summers**
- Portfolio: [Your Portfolio URL]
- LinkedIn: [Your LinkedIn]
- GitHub: [Your GitHub]

## 📄 License

This project is open source and available for educational purposes.

---

Built with ❤️ as part of Azure microservices learning journey.