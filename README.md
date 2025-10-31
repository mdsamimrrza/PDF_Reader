# 📄 PDF Q&A Assistant

An AI-powered tool to process and query PDF documents using embeddings and context-driven answers.

[![Deploy static content to Pages](https://github.com/mdsamimrrza/PDF_Reader/actions/workflows/static.yml/badge.svg)](https://github.com/mdsamimrrza/PDF_Reader/actions/workflows/static.yml)

## ⚠️ Important Note

This is a **backend FastAPI application** that requires a Python server to run. It **cannot be used directly through GitHub Pages** (which only serves static content). Please follow the setup instructions below to run it on your local machine or deploy it to a platform that supports Python applications (e.g., Heroku, Railway, Render, AWS, etc.).

**GitHub Pages URL**: The [GitHub Pages site](https://mdsamimrrza.github.io/PDF_Reader/) provides setup instructions.

## ✨ Features

- 📤 **Upload PDF documents** - Drag and drop or click to upload
- 🤖 **Ask questions about PDFs** - Get AI-powered answers (500+ words)
- 📚 **View relevant sources** - See 3 most relevant text chunks
- 🗂️ **Manage documents** - View, delete, and clear documents
- ✅ **Input validation** - Rejects invalid queries

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/mdsamimrrza/PDF_Reader.git
   cd PDF_Reader
   ```

2. **Install dependencies**
   
   On Windows:
   ```bash
   install.bat
   ```
   
   Or manually:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   
   On Windows:
   ```bash
   run.bat
   ```
   
   Or manually:
   ```bash
   python main.py
   ```

4. **Open in browser**
   ```
   http://localhost:8000
   ```

## 📖 Usage

1. **Upload PDF**
   - Click the upload area or drag and drop a PDF file
   - Wait for the processing to complete

2. **Ask Questions**
   - Type your question in the input field
   - Click "Ask" or press Enter
   - Get a comprehensive answer with source references

3. **Manage Documents**
   - View the list of uploaded documents
   - Delete individual documents or clear all

## 🛠️ Technology Stack

- **Backend**: FastAPI + Uvicorn
- **AI/ML**: Hugging Face Transformers, Sentence Transformers, PyTorch
- **PDF Processing**: PyPDF2
- **Frontend**: HTML5/CSS3/Vanilla JavaScript
- **Data Processing**: NumPy, Scikit-learn

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web interface |
| POST | `/upload` | Upload PDF file |
| POST | `/ask` | Ask question about PDFs |
| GET | `/documents` | List uploaded documents |
| DELETE | `/documents/{name}` | Delete specific document |
| DELETE | `/clear` | Clear all documents |
| GET | `/health` | Health check |

## 📂 Project Structure

```
PDF_Reader/
├── main.py                 # FastAPI application
├── config.py              # Configuration
├── requirements.txt       # Dependencies
├── models/                # ML/AI modules
│   ├── pdf_processor.py
│   └── qa_engine.py
├── utils/                 # Utilities
│   ├── file_handler.py
│   └── logger.py
├── docs/                  # Documentation
│   ├── README.md
│   ├── GETTING_STARTED.md
│   └── ...
└── uploads/               # PDF storage (created at runtime)
```

## ⚡ Performance

- **Upload**: 1-5 seconds per document
- **Search**: 0.5-2 seconds
- **Answer Generation**: 1-3 seconds
- **First Run**: 2-5 minutes (downloads AI models)
- **Memory**: ~2-3GB with models loaded
- **Disk**: ~330MB for AI models

## 🚢 Deployment Options

Since this is a backend application, you can deploy it to:

- **Heroku**: Follow their Python deployment guide
- **Railway**: Simple deployment for Python apps
- **Render**: Free tier available for Python apps
- **AWS EC2/Lambda**: For production deployments
- **Google Cloud Run**: Containerized deployment
- **DigitalOcean App Platform**: Python app support

**Note**: GitHub Pages is **not suitable** for this application as it only supports static content.

## 📝 Documentation

For detailed documentation, see the `docs/` directory:

- [README.md](docs/README.md) - Main documentation
- [GETTING_STARTED.md](docs/GETTING_STARTED.md) - Quick start guide
- [INPUT_VALIDATION.md](docs/INPUT_VALIDATION.md) - Input validation details
- [STRUCTURE.md](docs/STRUCTURE.md) - Project architecture
- [MIGRATION_GUIDE.md](docs/MIGRATION_GUIDE.md) - Migration information
- [PROJECT_SUMMARY.md](docs/PROJECT_SUMMARY.md) - Complete overview

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

**mdsamimrrza**

- GitHub: [@mdsamimrrza](https://github.com/mdsamimrrza)

## 🙏 Acknowledgments

- Hugging Face for the transformer models
- FastAPI for the excellent web framework
- PyPDF2 for PDF processing capabilities

---

**Ready to use!** 🚀

For issues or questions, visit the [GitHub Issues](https://github.com/mdsamimrrza/PDF_Reader/issues) page.
