"""
FastAPI MongoDB Server with Beanie ODM - Main Application.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_database, close_database
from app.routers import health, items, envs, views, getView


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    await init_database()
    print("Database initialized successfully!")
    yield
    # Shutdown (cleanup if needed)
    await close_database()
    print("Application shutdown complete.")


# Create FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION,
    lifespan=lifespan
)

# ✅ Add CORS middleware
origins = [
    "http://localhost:3000",  # React frontend
    "http://127.0.0.1:3000",
    "http://localhost:5173",  # Vite frontend
    "http://127.0.0.1:5173",
    "*"  # <-- allows all origins (not recommended for prod)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] for all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(items.router)
app.include_router(envs.router)
app.include_router(views.router)
app.include_router(getView.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=settings.DEBUG
    )