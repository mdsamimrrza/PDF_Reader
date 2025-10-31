"""File handling utilities"""

import os
from pathlib import Path


def ensure_directory(directory_path: str) -> str:
    """Ensure directory exists, create if not"""
    path = Path(directory_path)
    path.mkdir(parents=True, exist_ok=True)
    return str(path)


def get_file_size(file_path: str) -> int:
    """Get file size in bytes"""
    if os.path.exists(file_path):
        return os.path.getsize(file_path)
    return 0


def is_pdf_file(filename: str) -> bool:
    """Check if file is PDF"""
    return filename.lower().endswith('.pdf')


def get_file_info(file_path: str) -> dict:
    """Get file information"""
    if not os.path.exists(file_path):
        return {}
    
    return {
        'name': os.path.basename(file_path),
        'size': os.path.getsize(file_path),
        'path': file_path,
        'exists': True
    }
