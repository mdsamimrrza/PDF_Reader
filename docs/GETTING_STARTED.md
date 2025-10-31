# PDF Q&A Assistant - Getting Started

## Quick Start

### 1. Install Dependencies
```bash
install.bat
```

### 2. Run Application
```bash
run.bat
```

### 3. Open Browser
```
http://localhost:8000
```

### 4. Upload PDF and Ask Questions
- Click upload area or drag & drop PDF
- Type your question
- Get AI-powered answers with sources

---

## Features

✅ **Upload PDFs** - Extract and process documents
✅ **Ask Questions** - Natural language queries
✅ **Get Answers** - AI-powered responses with sources
✅ **Manage Documents** - Upload, view, delete
✅ **Beautiful UI** - Modern, responsive interface

---

## Project Structure

```
python/
├── main.py                 # FastAPI application
├── config.py              # Configuration
├── requirements.txt       # Dependencies
│
├── models/                # ML/AI modules
│   ├── pdf_processor.py  # PDF extraction
│   └── qa_engine.py      # Question answering
│
├── utils/                 # Utilities
│   ├── file_handler.py   # File operations
│   └── logger.py         # Logging
│
├── docs/                  # Documentation
│   ├── README.md
│   ├── STRUCTURE.md
│   └── GETTING_STARTED.md
│
└── venv/                  # Virtual environment
```

---

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

---

## Configuration

Edit `.env` file:
```
PORT=8000
CHUNK_SIZE=500
TOP_K_RESULTS=3
USE_GPU=True
```

---

## Models

- **Embeddings**: all-MiniLM-L6-v2 (~80MB)
- **QA**: distilbert-base-cased-distilled-squad (~250MB)

---

## Performance

- Upload: 1-5s
- Search: 0.5-2s
- Answer: 1-3s
- First run: 2-5 min (model download)

---

## Troubleshooting

### Port already in use
```bash
venv\Scripts\uvicorn main:app --port 8001
```

### Models not downloading
Check internet connection. Models cache in `~/.cache/huggingface/`

### Out of memory
Close other applications or use smaller PDFs

---

## Support

For more information:
- Check `docs/README.md` for full documentation
- Check `docs/STRUCTURE.md` for architecture details
- Review code comments in source files

---

**Ready to use!** 🚀
