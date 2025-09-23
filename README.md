# FastAPI MongoDB Server with Beanie ODM

A modern FastAPI application with MongoDB integration using Beanie ODM, containerized with Docker and Docker Compose.

## Features

- **FastAPI** web framework with automatic OpenAPI documentation
- **Beanie ODM** - Modern async Python ODM for MongoDB based on Pydantic
- **MongoDB** database with MongoDB Express web UI
- **Docker** containerization for easy deployment
- Complete **CRUD operations** for items with advanced features:
  - Create, Read, Update, Delete operations
  - Search functionality (by name or description)
  - Filtering by name, price range
  - Pagination support
  - Database statistics
- Health check endpoints
- Input validation with Pydantic
- Async/await support throughout
- Proper error handling

## Quick Start

### Prerequisites

- Docker and Docker Compose installed on your machine

### Running the Application

1. Clone or navigate to this directory
2. Start all services with Docker Compose:

```bash
docker-compose up --build
```

This will start three services:
- **FastAPI application** on http://localhost:8000
- **MongoDB** on localhost:27017
- **MongoDB Express** (web UI) on http://localhost:8081

### API Endpoints

#### Core Endpoints
- **GET /** - Welcome message
- **GET /health** - Health check endpoint with database connection status
- **GET /stats** - Database statistics (total items, average price)

#### Item Management (CRUD)
- **POST /items/** - Create a new item
- **GET /items/** - List all items with optional filters:
  - `skip` & `limit` - Pagination
  - `name` - Filter by name (case-insensitive search)
  - `min_price` & `max_price` - Filter by price range
- **GET /items/{item_id}** - Get a specific item by ID
- **PUT /items/{item_id}** - Update an item (partial updates supported)
- **DELETE /items/{item_id}** - Delete an item by ID

#### Search & Discovery
- **GET /items/search/{search_term}** - Search items by name or description

### API Documentation

Once the application is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### MongoDB Web Interface

Access MongoDB Express at http://localhost:8081
- Username: `webadmin`
- Password: `webpass123`

## Development

### Local Development Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start only MongoDB with Docker:
```bash
docker-compose up mongodb -d
```

4. Run the FastAPI application locally:
```bash
uvicorn main:app --reload
```

### Environment Variables

The following environment variables can be configured:

- `MONGO_URL`: MongoDB connection string (default: `mongodb://mongodb:27017`)
- `DATABASE_NAME`: MongoDB database name (default: `fastapi_db`)

### Example API Usage

#### Create an Item
```bash
curl -X POST "http://localhost:8000/items/" \
     -H "Content-Type: application/json" \
     -d '{"name": "Sample Item", "description": "This is a sample item", "price": 29.99}'
```

#### Get All Items (with Pagination)
```bash
curl -X GET "http://localhost:8000/items/?skip=0&limit=10"
```

#### Filter Items by Name
```bash
curl -X GET "http://localhost:8000/items/?name=sample"
```

#### Filter Items by Price Range
```bash
curl -X GET "http://localhost:8000/items/?min_price=20&max_price=50"
```

#### Search Items
```bash
curl -X GET "http://localhost:8000/items/search/sample"
```

#### Get Database Statistics
```bash
curl -X GET "http://localhost:8000/stats"
```

#### Get Specific Item
```bash
curl -X GET "http://localhost:8000/items/{item_id}"
```

#### Update an Item (Partial Update)
```bash
curl -X PUT "http://localhost:8000/items/{item_id}" \
     -H "Content-Type: application/json" \
     -d '{"name": "Updated Item", "price": 39.99}'
```

#### Delete an Item
```bash
curl -X DELETE "http://localhost:8000/items/{item_id}"
```

## Project Structure

```
.
├── main.py              # FastAPI application with Beanie ODM models and endpoints
├── requirements.txt     # Python dependencies (FastAPI, Beanie, etc.)
├── Dockerfile          # Docker configuration for FastAPI
├── docker-compose.yml  # Docker Compose configuration
├── .dockerignore       # Docker ignore file
├── .env                # Environment variables
└── README.md           # This file
```

## Key Technologies

- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern Python web framework for APIs
- **[Beanie](https://beanie-odm.dev/)** - Async Python ODM for MongoDB, based on Pydantic
- **[MongoDB](https://www.mongodb.com/)** - NoSQL document database
- **[Pydantic](https://pydantic.dev/)** - Data validation using Python type hints
- **[Docker](https://www.docker.com/)** - Containerization platform

## Stopping the Application

To stop all services:

```bash
docker-compose down
```

To stop and remove all data:

```bash
docker-compose down -v
```

## Troubleshooting

1. **Port conflicts**: If ports 8000, 8081, or 27017 are already in use, modify the port mappings in `docker-compose.yml`

2. **Permission issues**: On Linux/Mac, you might need to run Docker commands with `sudo`

3. **Database connection issues**: Check that MongoDB is running and accessible. Use the health check endpoint at `/health` to verify connectivity

4. **Container build issues**: Try rebuilding without cache:
   ```bash
   docker-compose build --no-cache
   ```