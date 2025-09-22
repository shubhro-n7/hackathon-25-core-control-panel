# FastAPI MongoDB Server

A complete FastAPI application with MongoDB integration, containerized with Docker and Docker Compose.

## Features

- FastAPI web framework with automatic OpenAPI documentation
- MongoDB database with MongoDB Express web UI
- Docker containerization for easy deployment
- Complete CRUD operations for items
- Health check endpoints
- Input validation with Pydantic
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

- **GET /** - Welcome message
- **GET /health** - Health check endpoint
- **POST /items/** - Create a new item
- **GET /items/** - List all items (with pagination)
- **GET /items/{item_id}** - Get a specific item
- **PUT /items/{item_id}** - Update an item
- **DELETE /items/{item_id}** - Delete an item

### API Documentation

Once the application is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### MongoDB Web Interface

Access MongoDB Express at http://localhost:8081
- Username: `admin`
- Password: `admin`

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

#### Get All Items
```bash
curl -X GET "http://localhost:8000/items/"
```

#### Get Specific Item
```bash
curl -X GET "http://localhost:8000/items/{item_id}"
```

#### Update an Item
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
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration for FastAPI
├── docker-compose.yml  # Docker Compose configuration
├── .dockerignore       # Docker ignore file
├── .env                # Environment variables
└── README.md           # This file
```

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