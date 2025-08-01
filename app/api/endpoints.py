# app/api/endpoints.py

"""
API Endpoints
-------------
Defines routes for uploading PDF files and controlling real-time TTS reading.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import uuid
import os

from app.services.pdf_reader import PDFReaderService
from app.services.tts_engine import tts_engine

router = APIRouter()
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Store extracted text in-memory (can be expanded to database later)
book_text_store = {}


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Uploads a PDF file and extracts its text.
    Returns a file_id to use in future read requests.
    """
    file_id = str(uuid.uuid4())
    filename = f"{file_id}.pdf"
    file_path = UPLOAD_DIR / filename

    with open(file_path, "wb") as f:
        f.write(await file.read())

    try:
        extracted_text = PDFReaderService.extract_text(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract text: {str(e)}")

    book_text_store[file_id] = extracted_text
    return {
        "message": "PDF uploaded and processed",
        "file_id": file_id,
        "preview": extracted_text[:300]
    }


@router.post("/read/start/{file_id}")
def start_reading(file_id: str):
    """
    Starts reading the text aloud for a given file_id.
    """
    if file_id not in book_text_store:
        raise HTTPException(status_code=404, detail="Invalid file_id")

    if tts_engine.is_reading():
        return {"status": "already_reading"}

    tts_engine.start_reading(book_text_store[file_id])
    return {"status": "started_reading"}


@router.post("/read/stop")
def stop_reading():
    """
    Stops the current TTS playback.
    """
    if not tts_engine.is_reading():
        return {"status": "not_reading"}
    
    tts_engine.stop_reading()
    return {"status": "stopped_reading"}