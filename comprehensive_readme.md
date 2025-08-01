# 📚 PDF Chat + Real-Time Reader (TTS)

A modern FastAPI + Streamlit application that allows users to upload PDF files, read them aloud using text-to-speech, and ask questions about the content with intelligent responses.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🚀 Features

✅ **PDF Upload & Processing** - Upload PDF files and extract text content  
✅ **Text-to-Speech Reading** - Listen to entire PDF read aloud  
✅ **Stop/Start Controls** - Control TTS playback anytime  
✅ **Intelligent Q&A** - Ask questions about PDF content  
✅ **Answer Audio** - Hear answers spoken aloud  
✅ **Real-time Backend** - Modern FastAPI with proper error handling  
✅ **User-friendly UI** - Clean Streamlit interface with status indicators

## 🎯 Core Functionality

| Feature | Description | Status |
|---------|-------------|--------|
| 📄 **PDF Upload** | Upload and process PDF files up to 10MB | ✅ Working |
| 🗣️ **Read Aloud** | Text-to-speech for entire document | ✅ Working |
| ⏹️ **Stop Reading** | Stop TTS playback instantly | ✅ Working |
| 💬 **Ask Questions** | Query PDF content with intelligent responses | ✅ Working |
| 🔊 **Hear Answers** | Listen to Q&A responses via TTS | ✅ Working |

## 🧱 Tech Stack

- **Backend Framework**: FastAPI 0.104+
- **Frontend**: Streamlit 1.28+
- **PDF Processing**: PyMuPDF (fitz)
- **Text-to-Speech**: pyttsx3
- **HTTP Client**: requests
- **Data Validation**: Pydantic 2.5+
- **ASGI Server**: Uvicorn

## 📁 Project Structure

```
pdf_tts_reader/
│
├── app/
│   ├── __init__.py              # Package initialization
│   └── api/
│       ├── __init__.py          # API package initialization
│       └── endpoints.py         # FastAPI route handlers
│
├── uploads/                     # PDF file storage (auto-created)
│
├── backend.py                   # FastAPI application entry point
├── main.py                      # Streamlit frontend application
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Audio output device (for TTS functionality)

### Step 1: Clone & Navigate
```bash
git clone <your-repo-url>
cd pdf_tts_reader
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Create Required Directories
The `uploads/` directory will be created automatically when you first upload a PDF.

### Step 4: Platform-Specific TTS Setup

**Windows:**
```bash
pip install pywin32
```

**macOS:**
TTS works out of the box with built-in speech synthesis.

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install espeak espeak-data
```

## 🚀 Running the Application

### Method 1: Separate Terminals (Recommended)

**Terminal 1 - Start Backend:**
```bash
python backend.py
```
Wait for: `"PDF Reader API Server started successfully!"`

**Terminal 2 - Start Frontend:**
```bash
streamlit run main.py
```

### Method 2: Background Process
```bash
# Start backend in background
python backend.py &

# Start frontend
streamlit run main.py
```

## 🌐 Access URLs

- **Streamlit App**: http://localhost:8501
- **FastAPI Backend**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000/health

## 📖 How to Use

### 1. Upload PDF
1. Open the Streamlit app in your browser
2. Click "Choose a PDF file" and select your document
3. Click "Upload PDF" button
4. Wait for processing confirmation

### 2. Text-to-Speech Reading
1. After uploading, click "▶️ Start Reading Whole PDF"
2. Adjust your system volume as needed
3. Use "⏹️ Stop Reading" to halt playback anytime

### 3. Ask Questions
1. Type your question in the chat input box
2. Press Enter to submit
3. Wait for the AI-generated response
4. Click "🔊 Speak Answer" to hear the response aloud

### 4. Managing Sessions
- Upload new PDFs anytime to replace the current document
- Use "🗑️ Clear Chat History" to reset conversation
- Backend connection status shown in sidebar

## 🔧 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/api/upload` | Upload PDF file |
| `POST` | `/api/read/start/{file_id}` | Start TTS reading |
| `POST` | `/api/read/stop` | Stop TTS reading |
| `POST` | `/api/speak` | Speak custom text |
| `POST` | `/api/chat` | Ask questions about PDF |

## ⚙️ Configuration

### File Upload Limits
- **Maximum file size**: 10MB
- **Supported formats**: PDF only
- **Storage location**: `uploads/` directory

### TTS Settings
- **Reading speed**: 150 WPM (words per minute)
- **Volume**: 80%
- **Chunk size**: 50 words per segment (for stop functionality)

### Backend Settings
- **Host**: 127.0.0.1
- **Port**: 8000
- **Auto-reload**: Enabled in development
- **CORS**: Enabled for all origins

## 🐛 Troubleshooting

### Common Issues

**Backend won't start:**
```bash
# Check if port 8000 is in use
netstat -an | grep 8000

# Kill process using port 8000 (if needed)
# Windows: taskkill /F /PID <process_id>
# Mac/Linux: kill -9 $(lsof -ti:8000)
```

**Import errors:**
```bash
# Ensure you're in the project root directory
pwd
ls -la  # Should see backend.py and main.py

# Check Python path
python -c "import sys; print(sys.path)"
```

**TTS not working:**
- **Windows**: Ensure Windows Speech Platform is installed
- **Mac**: Check System Preferences > Accessibility > Speech
- **Linux**: Verify espeak installation: `espeak "test"`

**PDF upload fails:**
- Check file size (must be < 10MB)
- Ensure file is a valid PDF
- Verify uploads directory permissions

### Error Messages

| Error | Solution |
|-------|----------|
| `"Backend server is not running!"` | Start backend with `python backend.py` |
| `"Only PDF files are allowed"` | Upload .pdf files only |
| `"File too large (max 10MB)"` | Reduce file size or split PDF |
| `"Failed to process PDF"` | Check if PDF is corrupted |

## 🧪 Testing

### Manual Testing Checklist

- [ ] PDF uploads successfully
- [ ] Text extraction works
- [ ] TTS starts and plays audio
- [ ] TTS stops when requested
- [ ] Questions receive relevant answers
- [ ] Answer TTS functionality works
- [ ] Backend health check responds
- [ ] Error handling works properly

### API Testing with curl

```bash
# Health check
curl http://localhost:8000/health

# Upload PDF
curl -X POST "http://localhost:8000/api/upload" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_document.pdf"
```

## 🔒 Security Considerations

- File uploads are validated for type and size
- File paths are sanitized to prevent directory traversal
- Error messages don't expose internal system details
- CORS is configured for development (adjust for production)

## 🚀 Production Deployment

### Environment Variables
Create a `.env` file:
```env
FASTAPI_ENV=production
MAX_FILE_SIZE=10485760
UPLOAD_DIR=uploads
TTS_RATE=150
TTS_VOLUME=0.8
```

### Docker Deployment (Optional)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000 8501

CMD ["python", "backend.py"]
```

## 📈 Future Enhancements

- [ ] **AI Integration**: OpenAI GPT for better Q&A responses
- [ ] **Voice Selection**: Multiple TTS voice options
- [ ] **User Authentication**: Multi-user support with sessions
- [ ] **Cloud Storage**: AWS S3 or Google Cloud integration
- [ ] **Chapter Navigation**: Jump to specific PDF sections
- [ ] **Bookmarks**: Save favorite sections
- [ ] **Export Features**: Download chat history
- [ ] **Mobile Responsive**: Better mobile interface

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Follow the coding standards in the project
4. Commit changes (`git commit -m 'Add amazing feature'`)
5. Push to branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI** - Modern web framework for building APIs
- **Streamlit** - Rapid web app development
- **PyMuPDF** - PDF processing capabilities
- **pyttsx3** - Cross-platform text-to-speech library

## 📞 Support

If you encounter issues:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review error logs in terminal output
3. Ensure all dependencies are properly installed
4. Create an issue in the repository with:
   - Error message details
   - Steps to reproduce
   - Your operating system and Python version

---

**Built with ❤️ for seamless PDF interaction and accessibility**