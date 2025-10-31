# PDF Q&A Assistant - Documentation

## Overview
AI-powered PDF Question & Answer system using FastAPI, Hugging Face Transformers, and Sentence Transformers.

## Quick Start
```bash
# Install dependencies
install.bat

# Run application
run.bat

# Open browser
http://localhost:8000
```

## Features
- 📄 Upload and process PDF documents
- 🔍 Semantic search using embeddings
- 🤖 AI-powered question answering
- 💾 Document management
- 🎨 Beautiful responsive web UI

## Project Structure
```
python/
├── main.py                 # FastAPI application
├── models/                 # Core ML modules
│   ├── pdf_processor.py   # PDF extraction
│   └── qa_engine.py       # QA logic
├── utils/                  # Utility modules
│   ├── file_handler.py    # File operations
│   └── logger.py          # Logging
├── config.py              # Configuration
├── requirements.txt       # Dependencies
└── docs/                  # Documentation
```

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Web interface |
| POST | `/upload` | Upload PDF |
| POST | `/ask` | Ask question |
| GET | `/documents` | List documents |
| DELETE | `/documents/{name}` | Delete document |
| DELETE | `/clear` | Clear all |
| GET | `/health` | Health check |

## Configuration
Edit `.env` file to customize:
- `PORT`: Server port (default: 8000)
- `CHUNK_SIZE`: Text chunk size (default: 500)
- `TOP_K_RESULTS`: Search results (default: 3)

## Models
- **Embeddings**: all-MiniLM-L6-v2 (~80MB)
- **QA**: distilbert-base-cased-distilled-squad (~250MB)

## Performance
- Upload: 1-5s
- Search: 0.5-2s
- Answer: 1-3s

## Troubleshooting

### Port already in use
```bash
venv\Scripts\uvicorn main:app --port 8001
```

### Models not downloading
Check internet connection. Models cache in `~/.cache/huggingface/`

### Out of memory
Close other applications or use smaller PDFs

## Support
For issues, check the documentation or review code comments.
