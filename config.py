"""Configuration settings for PDF Q&A Assistant"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Model Configuration
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
QA_MODEL = os.getenv("QA_MODEL", "distilbert-base-cased-distilled-squad")

# Processing Configuration
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))
TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", 5))

# File Upload Configuration
MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", 50))
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")

# Performance Configuration
USE_GPU = os.getenv("USE_GPU", "True").lower() == "true"
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 32))

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)
