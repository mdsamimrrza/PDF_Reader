# Project Structure

## Directory Layout

```
python/
├── main.py                    # FastAPI application entry point
├── config.py                  # Configuration management
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
│
├── models/                    # Core ML modules
│   ├── __init__.py           # Package initialization
│   ├── pdf_processor.py      # PDF extraction and chunking
│   └── qa_engine.py          # Embeddings and QA logic
│
├── utils/                     # Utility modules
│   ├── __init__.py           # Package initialization
│   ├── file_handler.py       # File operations
│   └── logger.py             # Logging utilities
│
├── docs/                      # Documentation
│   ├── README.md             # Main documentation
│   ├── STRUCTURE.md          # This file
│   ├── API.md                # API documentation
│   └── SETUP.md              # Setup guide
│
├── venv/                      # Python virtual environment
└── uploads/                   # Uploaded PDF files (created at runtime)
```

## Module Descriptions

### Core Application
- **main.py** (730 lines)
  - FastAPI application setup
  - API endpoints (7 total)
  - Web UI (HTML/CSS/JS)
  - CORS configuration
  - Request/response handling

- **config.py** (30 lines)
  - Environment variable management
  - Configuration defaults
  - Directory setup

### Models (ML/AI)
- **models/pdf_processor.py** (100 lines)
  - PDF text extraction
  - Text chunking with overlap
  - Document management
  - Text cleaning

- **models/qa_engine.py** (180 lines)
  - Embeddings computation
  - Semantic similarity search
  - Question answering
  - Answer enhancement
  - Query processing

### Utilities
- **utils/file_handler.py** (40 lines)
  - Directory creation
  - File operations
  - File validation
  - File information

- **utils/logger.py** (30 lines)
  - Logger setup
  - Logging configuration
  - Consistent formatting

## File Statistics

| Category | Files | Lines | Size |
|----------|-------|-------|------|
| Application | 1 | 730 | 24KB |
| Models | 2 | 280 | 8KB |
| Utils | 2 | 70 | 2KB |
| Config | 1 | 30 | 1KB |
| Total Code | 6 | 1,110 | 35KB |

## Dependencies

### Core
- FastAPI - Web framework
- Uvicorn - ASGI server
- Pydantic - Data validation

### ML/AI
- Hugging Face Transformers
- Sentence Transformers
- PyTorch
- NumPy

### Data Processing
- PyPDF2 - PDF extraction
- Scikit-learn - ML utilities

## Import Structure

```python
# Main application imports
from models import PDFProcessor, QAEngine
from utils import ensure_directory, setup_logger

# Internal imports
from models.pdf_processor import PDFProcessor
from models.qa_engine import QAEngine
from utils.file_handler import ensure_directory
from utils.logger import setup_logger
```

## Modularity Benefits

✅ **Separation of Concerns**
- Models: ML/AI logic
- Utils: Helper functions
- Main: API and UI

✅ **Reusability**
- Import models in other projects
- Use utils independently
- Easy to extend

✅ **Maintainability**
- Clear organization
- Easy to locate code
- Simple to update

✅ **Scalability**
- Add new models easily
- Extend utilities
- Create new modules

## Adding New Features

### Add New Model
1. Create file in `models/`
2. Add to `models/__init__.py`
3. Import in `main.py`

### Add New Utility
1. Create file in `utils/`
2. Add to `utils/__init__.py`
3. Import where needed

### Add New Endpoint
1. Add function to `main.py`
2. Use `@app.route()` decorator
3. Import required models/utils

## Configuration

Edit `config.py` to customize:
- Model names
- Chunk sizes
- Default parameters
- Directory paths

## Environment Variables

Create `.env` file:
```
PORT=8000
CHUNK_SIZE=500
TOP_K_RESULTS=3
USE_GPU=True
```

## Running the Application

```bash
# Activate environment
venv\Scripts\activate

# Run application
python main.py

# Or with Uvicorn
uvicorn main:app --reload
```

## Testing

```bash
# Run setup verification
python test_setup.py

# Create sample PDF
python create_sample_pdf.py
```

## Future Improvements

- [ ] Add database layer
- [ ] Create API versioning
- [ ] Add authentication
- [ ] Create CLI interface
- [ ] Add caching layer
- [ ] Create deployment configs
- [ ] Add unit tests
- [ ] Add integration tests
