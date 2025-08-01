from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create uploads directory if it doesn't exist
os.makedirs("uploads", exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("PDF Reader API Server starting up...")
    yield
    # Shutdown
    logger.info("PDF Reader API Server shutting down...")

# Create FastAPI app with modern lifespan
app = FastAPI(
    title="PDF Reader API",
    description="API for PDF reading with TTS and Q&A",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routes (create these endpoints)
from app.api import endpoints
app.include_router(endpoints.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "PDF Reader API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

if __name__ == "__main__":
    logger.info("Starting PDF Reader API Server...")
    uvicorn.run(
        "backend:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
    logger.info("PDF Reader API Server started successfully!")