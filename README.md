# E-Commerce Platform - Containerized Microservices

Containerized e-commerce application demonstrating multi-tier architecture with Docker and PostgreSQL.

## Technical Overview

**Backend**: Flask REST API with SQLAlchemy ORM  
**Database**: PostgreSQL 15  
**Frontend**: Vanilla JavaScript  
**Infrastructure**: Docker containers with custom networking  

## Architecture
```
Frontend (HTML/JS) → Backend API (Flask) → PostgreSQL Database
                     ↓
              Docker Network
```

- Backend and database run in separate Docker containers
- Containers communicate via Docker bridge network
- API serves JSON data from PostgreSQL
- Frontend fetches products dynamically via REST endpoints

## Stack

- Python 3.10, Flask 2.3, SQLAlchemy 2.0
- PostgreSQL 15
- Docker & Docker Networks
- Gunicorn (production WSGI server)

## Setup

**Requirements**: Docker Desktop, Git

**Run locally**:
```bash
# Clone repo
git clone https://github.com/amna-hashim-tech/ecommerce-devops-project.git
cd ecommerce-devops-project

# Create network
docker network create ecommerce-network

# Start database
docker run -d --name postgres-db --network ecommerce-network \
  -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=ecommerce \
  -p 5432:5432 postgres:15

# Build and run backend
cd backend
docker build -t ecommerce-backend .
docker run -d -p 5000:5000 --name backend-container \
  --network ecommerce-network \
  -e DATABASE_URL=postgresql://postgres:postgres@postgres-db:5432/ecommerce \
  ecommerce-backend

# Open frontend
cd ../frontend
open index.html
```

API runs on `http://localhost:5000`

## API Endpoints

- `GET /products` - List all products
- `GET /products/<id>` - Get single product
- `GET /health` - Health check

## Project Structure
```
├── backend/
│   ├── app.py              # Flask application
│   ├── Dockerfile          # Backend container config
│   └── requirements.txt    # Python dependencies
├── frontend/
│   └── index.html          # Product catalog UI
└── README.md
```

## Next Steps

- Docker Compose for orchestration
- Deploy to Azure Kubernetes Service
- CI/CD pipeline with Azure DevOps
- Add Redis caching layer
- Implement monitoring (Prometheus/Grafana)

