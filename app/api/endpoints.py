from fastapi import APIRouter, HTTPException, UploadFile, File, BackgroundTasks
from pydantic import BaseModel
import os
import uuid
import logging
import fitz  # PyMuPDF
import pyttsx3
import threading
from typing import Dict, Optional

# Setup logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Global TTS engine and control
tts_engine = None
tts_thread = None
stop_reading = False

class ChatRequest(BaseModel):
    file_id: str
    message: str

class ChatResponse(BaseModel):
    answer: str
    file_id: str

# Store uploaded files info
uploaded_files: Dict[str, Dict] = {}

def initialize_tts():
    """Initialize TTS engine"""
    global tts_engine
    try:
        tts_engine = pyttsx3.init()
        tts_engine.setProperty('rate', 150)  # Speed
        tts_engine.setProperty('volume', 0.8)  # Volume
        logger.info("TTS engine initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize TTS: {e}")

def extract_pdf_text(file_path: str) -> str:
    """Extract text from PDF file"""
    try:
        doc = fitz.open(file_path)
        text = ""
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        raise HTTPException(500, f"Failed to process PDF: {str(e)}")

def read_text_aloud(text: str):
    """Read text using TTS in background"""
    global tts_engine, stop_reading
    try:
        if tts_engine is None:
            initialize_tts()
        
        if tts_engine:
            # Split text into chunks to allow stopping
            words = text.split()
            chunk_size = 50  # Read 50 words at a time
            
            for i in range(0, len(words), chunk_size):
                if stop_reading:
                    break
                
                chunk = " ".join(words[i:i + chunk_size])
                tts_engine.say(chunk)
                tts_engine.runAndWait()
                
        logger.info("TTS reading completed")
    except Exception as e:
        logger.error(f"TTS error: {e}")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "PDF Reader API is running"}

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload and process PDF file"""
    try:
        # Validate file
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(400, "Only PDF files are allowed")
        
        if file.size and file.size > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(400, "File too large (max 10MB)")
        
        # Generate unique file ID
        file_id = str(uuid.uuid4())
        
        # Create uploads directory if it doesn't exist
        os.makedirs("uploads", exist_ok=True)
        
        # Save file
        file_path = f"uploads/{file_id}.pdf"
        content = await file.read()
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Extract text
        text = extract_pdf_text(file_path)
        
        # Store file info
        uploaded_files[file_id] = {
            "original_name": file.filename,
            "file_path": file_path,
            "text": text,
            "preview": text[:500] + "..." if len(text) > 500 else text
        }
        
        logger.info(f"PDF uploaded successfully: {file.filename} -> {file_id}")
        
        return {
            "file_id": file_id,
            "message": "PDF uploaded and processed successfully",
            "preview": uploaded_files[file_id]["preview"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(500, f"Upload failed: {str(e)}")

@router.post("/read/start/{file_id}")
async def start_reading(file_id: str, background_tasks: BackgroundTasks):
    """Start reading PDF aloud"""
    global tts_thread, stop_reading
    
    try:
        if file_id not in uploaded_files:
            raise HTTPException(404, "File not found")
        
        # Stop any current reading
        stop_reading = True
        if tts_thread and tts_thread.is_alive():
            tts_thread.join(timeout=1)
        
        # Reset stop flag and start new reading
        stop_reading = False
        text = uploaded_files[file_id]["text"]
        
        # Start TTS in background thread
        tts_thread = threading.Thread(target=read_text_aloud, args=(text,))
        tts_thread.daemon = True
        tts_thread.start()
        
        logger.info(f"Started reading PDF: {file_id}")
        return {"message": "Started reading PDF", "file_id": file_id}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Reading start error: {e}")
        raise HTTPException(500, f"Failed to start reading: {str(e)}")

@router.post("/read/stop")
async def stop_reading_endpoint():
    """Stop current TTS reading"""
    global stop_reading, tts_engine
    
    try:
        stop_reading = True
        
        # Stop TTS engine
        if tts_engine:
            try:
                tts_engine.stop()
            except:
                pass
        
        logger.info("Stopped TTS reading")
        return {"message": "Reading stopped"}
        
    except Exception as e:
        logger.error(f"Stop reading error: {e}")
        raise HTTPException(500, f"Failed to stop reading: {str(e)}")

@router.post("/speak")
async def speak_text(text: str):
    """Speak given text"""
    global tts_engine, stop_reading
    
    try:
        # Stop current reading first
        stop_reading = True
        
        if tts_engine is None:
            initialize_tts()
        
        if tts_engine:
            # Start new speech in background
            def speak():
                tts_engine.say(text)
                tts_engine.runAndWait()
            
            thread = threading.Thread(target=speak)
            thread.daemon = True
            thread.start()
        
        return {"message": "Speaking text"}
        
    except Exception as e:
        logger.error(f"Speak error: {e}")
        raise HTTPException(500, f"Failed to speak text: {str(e)}")

@router.post("/chat", response_model=ChatResponse)
async def chat_with_pdf(request: ChatRequest):
    """Ask questions about uploaded PDF"""
    try:
        if request.file_id not in uploaded_files:
            raise HTTPException(404, "File not found")
        
        text = uploaded_files[request.file_id]["text"]
        question = request.message.lower()
        
        # Simple keyword-based Q&A (you can enhance this with AI)
        answer = simple_qa(text, question)
        
        logger.info(f"Chat query processed for file: {request.file_id}")
        
        return ChatResponse(
            answer=answer,
            file_id=request.file_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(500, f"Chat failed: {str(e)}")

def simple_qa(text: str, question: str) -> str:
    """Simple keyword-based question answering"""
    text_lower = text.lower()
    question_lower = question.lower()
    
    # Extract relevant sentences based on keywords
    sentences = text.split('.')
    relevant_sentences = []
    
    # Extract keywords from question
    question_words = question_lower.split()
    important_words = [word for word in question_words if len(word) > 3]
    
    # Find sentences containing question keywords
    for sentence in sentences:
        sentence_lower = sentence.lower()
        if any(word in sentence_lower for word in important_words):
            relevant_sentences.append(sentence.strip())
            if len(relevant_sentences) >= 3:  # Limit to 3 relevant sentences
                break
    
    if relevant_sentences:
        answer = ". ".join(relevant_sentences)
        return f"Based on the document: {answer}"
    else:
        return "I couldn't find specific information about that question in the document. Please try rephrasing your question or ask about different topics covered in the PDF."

# Initialize TTS on startup
initialize_tts()