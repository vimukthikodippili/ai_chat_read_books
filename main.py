# main.py

"""
Main Application Entry
----------------------
Bootstraps the FastAPI server and integrates the TTS and PDF upload API.
"""

from fastapi import FastAPI
from app.api.endpoints import router
import uvicorn

app = FastAPI(
    title="Real-Time PDF Reader with TTS",
    description="Upload a book, then listen to it read aloud in real time.",
    version="1.0.0"
)

# Include the API routes
app.include_router(router, prefix="/api")

# Run server when executed directly
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)