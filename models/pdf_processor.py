"""PDF Processing Module - Handles PDF extraction and text chunking"""

import PyPDF2
from typing import List
import os


class PDFProcessor:
    """Handles PDF file processing and text extraction"""
    
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        """Initialize PDF processor with configurable chunk parameters"""
        self.documents = {}
        self.text_chunks = []
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from a PDF file"""
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
            
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def chunk_text(self, text: str, chunk_size: int = None, overlap: int = None) -> List[str]:
        """Split text into overlapping chunks for better context"""
        chunk_size = chunk_size or self.chunk_size
        overlap = overlap or self.overlap
        
        chunks = []
        words = text.split()
        
        current_chunk = []
        for word in words:
            current_chunk.append(word)
            
            if len(current_chunk) >= chunk_size:
                chunks.append(" ".join(current_chunk))
                # Keep overlap words for context
                current_chunk = current_chunk[-overlap:]
        
        # Add remaining text
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks
    
    def process_pdf(self, file_path: str, doc_name: str = None) -> List[str]:
        """Process a PDF file and return text chunks"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        
        # Extract text
        text = self.extract_text_from_pdf(file_path)
        
        # Clean text
        text = self._clean_text(text)
        
        # Create chunks
        chunks = self.chunk_text(text)
        
        # Store document reference
        if doc_name is None:
            doc_name = os.path.basename(file_path)
        
        self.documents[doc_name] = {
            'path': file_path,
            'chunks': chunks,
            'full_text': text
        }
        
        self.text_chunks.extend(chunks)
        
        return chunks
    
    def _clean_text(self, text: str) -> str:
        """Clean extracted text"""
        # Remove extra whitespace
        text = " ".join(text.split())
        # Remove special characters but keep basic punctuation
        text = text.replace('\x00', '')
        return text
    
    def get_document_info(self) -> dict:
        """Get information about processed documents"""
        info = {}
        for doc_name, doc_data in self.documents.items():
            info[doc_name] = {
                'chunks': len(doc_data['chunks']),
                'text_length': len(doc_data['full_text'])
            }
        return info
    
    def clear_documents(self):
        """Clear all stored documents"""
        self.documents = {}
        self.text_chunks = []
