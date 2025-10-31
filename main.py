from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil

from models import PDFProcessor, QAEngine
from utils import ensure_directory

# Initialize FastAPI app
app = FastAPI(
    title="PDF Q&A Assistant",
    description="An AI-powered tool to process and query PDFs using embeddings and context-driven answers",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
pdf_processor = PDFProcessor()
qa_engine = QAEngine()

# Create uploads directory
UPLOAD_DIR = ensure_directory("uploads")

# Pydantic models
class QuestionRequest(BaseModel):
    question: str
    top_k: int = 3

class DocumentInfo(BaseModel):
    name: str
    chunks: int
    text_length: int

# Routes
@app.get("/", response_class=HTMLResponse)
async def get_home():
    """Serve the frontend HTML"""
    return get_frontend_html()

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload and process a PDF file"""
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Save uploaded file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process PDF
        chunks = pdf_processor.process_pdf(file_path, doc_name=file.filename)
        
        # Add chunks to QA engine
        qa_engine.add_documents(chunks)
        
        return {
            "status": "success",
            "message": f"PDF '{file.filename}' uploaded and processed successfully",
            "filename": file.filename,
            "chunks": len(chunks),
            "total_documents": len(pdf_processor.documents)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    """Ask a question about the uploaded PDFs"""
    try:
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        # Validate question has actual words (not just symbols)
        import re
        words = re.findall(r'[a-zA-Z]+', request.question)
        if len(words) == 0:
            raise HTTPException(status_code=400, detail="Question must contain actual words, not just symbols")
        
        result = qa_engine.process_query(request.question, top_k=request.top_k)
        
        return {
            "status": "success",
            "data": result
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

@app.get("/documents")
async def get_documents():
    """Get information about uploaded documents"""
    try:
        doc_info = pdf_processor.get_document_info()
        
        documents = []
        for name, info in doc_info.items():
            documents.append({
                "name": name,
                "chunks": info['chunks'],
                "text_length": info['text_length']
            })
        
        return {
            "status": "success",
            "total_documents": len(documents),
            "documents": documents
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving documents: {str(e)}")

@app.delete("/documents/{doc_name}")
async def delete_document(doc_name: str):
    """Delete a specific document"""
    try:
        if doc_name not in pdf_processor.documents:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Remove from processor
        del pdf_processor.documents[doc_name]
        
        # Recompute embeddings
        all_chunks = []
        for doc_data in pdf_processor.documents.values():
            all_chunks.extend(doc_data['chunks'])
        
        qa_engine.text_chunks = all_chunks
        if all_chunks:
            qa_engine._compute_embeddings()
        else:
            qa_engine.embeddings = None
        
        # Delete file
        file_path = os.path.join(UPLOAD_DIR, doc_name)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        return {
            "status": "success",
            "message": f"Document '{doc_name}' deleted successfully"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting document: {str(e)}")

@app.delete("/clear")
async def clear_all():
    """Clear all documents and reset the system"""
    try:
        pdf_processor.documents = {}
        pdf_processor.text_chunks = []
        qa_engine.clear_documents()
        
        # Clear uploads directory
        if os.path.exists(UPLOAD_DIR):
            shutil.rmtree(UPLOAD_DIR)
            os.makedirs(UPLOAD_DIR)
        
        return {
            "status": "success",
            "message": "All documents cleared successfully"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing documents: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "documents_loaded": len(pdf_processor.documents),
        "chunks_indexed": len(qa_engine.text_chunks)
    }

def get_frontend_html():
    """Return the frontend HTML"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PDF Q&A Assistant</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            
            header {
                text-align: center;
                color: white;
                margin-bottom: 40px;
            }
            
            header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            
            header p {
                font-size: 1.1em;
                opacity: 0.9;
            }
            
            .main-content {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 30px;
                margin-bottom: 30px;
            }
            
            .card {
                background: white;
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            
            .card:hover {
                transform: translateY(-5px);
                box-shadow: 0 15px 50px rgba(0,0,0,0.3);
            }
            
            .card h2 {
                color: #667eea;
                margin-bottom: 20px;
                font-size: 1.5em;
            }
            
            .upload-area {
                border: 3px dashed #667eea;
                border-radius: 10px;
                padding: 40px;
                text-align: center;
                cursor: pointer;
                transition: all 0.3s ease;
                background: #f8f9ff;
            }
            
            .upload-area:hover {
                background: #f0f2ff;
                border-color: #764ba2;
            }
            
            .upload-area.dragover {
                background: #e8ebff;
                border-color: #764ba2;
                transform: scale(1.02);
            }
            
            .upload-area p {
                color: #666;
                margin-bottom: 10px;
            }
            
            .upload-area .icon {
                font-size: 3em;
                margin-bottom: 10px;
            }
            
            #fileInput {
                display: none;
            }
            
            .question-input {
                display: flex;
                gap: 10px;
                margin-bottom: 20px;
            }
            
            input[type="text"] {
                flex: 1;
                padding: 12px 15px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 1em;
                transition: border-color 0.3s ease;
            }
            
            input[type="text"]:focus {
                outline: none;
                border-color: #667eea;
            }
            
            button {
                padding: 12px 30px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 1em;
                cursor: pointer;
                transition: all 0.3s ease;
                font-weight: 600;
            }
            
            button:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
            }
            
            button:active {
                transform: translateY(0);
            }
            
            .documents-list {
                margin-top: 20px;
            }
            
            .document-item {
                background: #f8f9ff;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 10px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .document-item .info {
                flex: 1;
            }
            
            .document-item .name {
                font-weight: 600;
                color: #333;
                margin-bottom: 5px;
            }
            
            .document-item .stats {
                font-size: 0.9em;
                color: #666;
            }
            
            .document-item button {
                padding: 8px 15px;
                font-size: 0.9em;
                background: #ff6b6b;
            }
            
            .answer-section {
                margin-top: 20px;
            }
            
            .answer-box {
                background: #f8f9ff;
                padding: 20px;
                border-radius: 8px;
                border-left: 4px solid #667eea;
                margin-bottom: 20px;
            }
            
            .answer-box h3 {
                color: #667eea;
                margin-bottom: 10px;
            }
            
            .answer-box .answer-text {
                color: #333;
                line-height: 1.8;
                margin-bottom: 20px;
                font-size: 1.05em;
                white-space: pre-wrap;
                word-wrap: break-word;
                padding: 15px;
                background: #f5f7ff;
                border-radius: 8px;
                border-left: 4px solid #667eea;
            }
            
            .answer-box .confidence {
                font-size: 0.95em;
                color: #667eea;
                font-weight: 600;
                margin-bottom: 15px;
            }
            
            .relevant-chunks {
                margin-top: 15px;
            }
            
            .relevant-chunks h4 {
                color: #764ba2;
                margin-bottom: 10px;
                font-size: 0.95em;
            }
            
            .chunk-item {
                background: white;
                padding: 12px;
                border-radius: 6px;
                margin-bottom: 8px;
                border-left: 3px solid #764ba2;
                font-size: 0.9em;
                color: #555;
                line-height: 1.5;
            }
            
            .loading {
                text-align: center;
                color: #667eea;
                font-weight: 600;
            }
            
            .error {
                background: #ffe0e0;
                color: #d32f2f;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 15px;
                border-left: 4px solid #d32f2f;
            }
            
            .success {
                background: #e0ffe0;
                color: #2e7d32;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 15px;
                border-left: 4px solid #2e7d32;
            }
            
            .full-width {
                grid-column: 1 / -1;
            }
            
            .controls {
                display: flex;
                gap: 10px;
                margin-top: 20px;
            }
            
            .controls button {
                flex: 1;
            }
            
            @media (max-width: 768px) {
                .main-content {
                    grid-template-columns: 1fr;
                }
                
                header h1 {
                    font-size: 1.8em;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>📄 PDF Q&A Assistant</h1>
                <p>Upload PDFs and ask questions using AI-powered embeddings</p>
            </header>
            
            <div class="main-content">
                <!-- Upload Section -->
                <div class="card">
                    <h2>Upload PDF</h2>
                    <div class="upload-area" id="uploadArea">
                        <div class="icon">📤</div>
                        <p><strong>Click to upload or drag and drop</strong></p>
                        <p style="font-size: 0.9em; color: #999;">PDF files only</p>
                    </div>
                    <input type="file" id="fileInput" accept=".pdf" />
                    
                    <div class="documents-list">
                        <h3 style="color: #333; margin-bottom: 15px;">Uploaded Documents</h3>
                        <div id="documentsList">
                            <p style="color: #999; text-align: center;">No documents uploaded yet</p>
                        </div>
                    </div>
                    
                    <div class="controls">
                        <button onclick="clearAll()" style="background: #ff6b6b;">Clear All</button>
                    </div>
                </div>
                
                <!-- Q&A Section -->
                <div class="card">
                    <h2>Ask Questions</h2>
                    <div id="messageArea"></div>
                    
                    <div class="question-input">
                        <input 
                            type="text" 
                            id="questionInput" 
                            placeholder="Ask a question about your PDFs..."
                            onkeypress="if(event.key === 'Enter') askQuestion()"
                        />
                        <button onclick="askQuestion()">Ask</button>
                    </div>
                    
                    <div class="answer-section" id="answerSection" style="display: none;">
                        <div class="answer-box">
                            <h3>Answer</h3>
                            <div class="answer-text" id="answerText"></div>
                            <div class="confidence" id="confidenceText"></div>
                            <div class="relevant-chunks" id="relevantChunks"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            const uploadArea = document.getElementById('uploadArea');
            const fileInput = document.getElementById('fileInput');
            const questionInput = document.getElementById('questionInput');
            const answerSection = document.getElementById('answerSection');
            const messageArea = document.getElementById('messageArea');
            
            // Upload area drag and drop
            uploadArea.addEventListener('click', () => fileInput.click());
            
            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.classList.add('dragover');
            });
            
            uploadArea.addEventListener('dragleave', () => {
                uploadArea.classList.remove('dragover');
            });
            
            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('dragover');
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    fileInput.files = files;
                    uploadFile();
                }
            });
            
            fileInput.addEventListener('change', uploadFile);
            
            async function uploadFile() {
                const file = fileInput.files[0];
                if (!file) return;
                
                const formData = new FormData();
                formData.append('file', file);
                
                showMessage('Uploading and processing PDF...', 'loading');
                
                try {
                    const response = await fetch('/upload', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        showMessage(`✓ ${data.message}`, 'success');
                        fileInput.value = '';
                        loadDocuments();
                    } else {
                        showMessage(`✗ Error: ${data.detail}`, 'error');
                    }
                } catch (error) {
                    showMessage(`✗ Error uploading file: ${error.message}`, 'error');
                }
            }
            
            async function askQuestion() {
                const question = questionInput.value.trim();
                if (!question) {
                    showMessage('Please enter a question', 'error');
                    return;
                }
                
                showMessage('Processing your question...', 'loading');
                answerSection.style.display = 'none';
                
                try {
                    const response = await fetch('/ask', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            question: question,
                            top_k: 3
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        messageArea.innerHTML = '';
                        displayAnswer(data.data);
                    } else {
                        showMessage(`✗ Error: ${data.detail}`, 'error');
                    }
                } catch (error) {
                    showMessage(`✗ Error: ${error.message}`, 'error');
                }
            }
            
            function displayAnswer(result) {
                // Format answer with better text wrapping
                const answerText = result.answer.trim();
                document.getElementById('answerText').textContent = answerText;
                
                // Display confidence with better formatting
                document.getElementById('confidenceText').innerHTML = 
                    `<strong>✓ Confidence:</strong> ${(result.confidence * 100).toFixed(1)}%`;
                
                // Format sources with better styling
                const chunksHtml = result.relevant_chunks.map((chunk, idx) => {
                    const relevance = (chunk.similarity * 100).toFixed(1);
                    const sourceText = chunk.text.substring(0, 350);
                    return `
                        <div class="chunk-item">
                            <strong>📄 Source ${idx + 1}</strong> 
                            <span style="color: #667eea; font-weight: 600;">Relevance: ${relevance}%</span><br/>
                            <div style="margin-top: 8px; color: #555; line-height: 1.6;">
                                "${sourceText}${chunk.text.length > 350 ? '...' : ''}"
                            </div>
                        </div>
                    `;
                }).join('');
                
                document.getElementById('relevantChunks').innerHTML = `
                    <h4>📚 Relevant Sources (${result.relevant_chunks.length} of 3)</h4>
                    ${chunksHtml}
                `;
                
                answerSection.style.display = 'block';
            }
            
            function showMessage(message, type) {
                if (type === 'loading') {
                    messageArea.innerHTML = `<div class="loading">${message}</div>`;
                } else if (type === 'error') {
                    messageArea.innerHTML = `<div class="error">${message}</div>`;
                } else if (type === 'success') {
                    messageArea.innerHTML = `<div class="success">${message}</div>`;
                    setTimeout(() => {
                        messageArea.innerHTML = '';
                    }, 3000);
                }
            }
            
            async function loadDocuments() {
                try {
                    const response = await fetch('/documents');
                    const data = await response.json();
                    
                    const documentsList = document.getElementById('documentsList');
                    
                    if (data.documents.length === 0) {
                        documentsList.innerHTML = '<p style="color: #999; text-align: center;">No documents uploaded yet</p>';
                    } else {
                        documentsList.innerHTML = data.documents.map(doc => `
                            <div class="document-item">
                                <div class="info">
                                    <div class="name">📄 ${doc.name}</div>
                                    <div class="stats">${doc.chunks} chunks • ${Math.round(doc.text_length / 1000)}KB</div>
                                </div>
                                <button onclick="deleteDocument('${doc.name}')">Delete</button>
                            </div>
                        `).join('');
                    }
                } catch (error) {
                    console.error('Error loading documents:', error);
                }
            }
            
            async function deleteDocument(docName) {
                if (!confirm(`Delete "${docName}"?`)) return;
                
                try {
                    const response = await fetch(`/documents/${encodeURIComponent(docName)}`, {
                        method: 'DELETE'
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        showMessage(`✓ ${data.message}`, 'success');
                        loadDocuments();
                    } else {
                        showMessage(`✗ Error: ${data.detail}`, 'error');
                    }
                } catch (error) {
                    showMessage(`✗ Error: ${error.message}`, 'error');
                }
            }
            
            async function clearAll() {
                if (!confirm('Clear all documents? This cannot be undone.')) return;
                
                try {
                    const response = await fetch('/clear', {
                        method: 'DELETE'
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        showMessage(`✓ ${data.message}`, 'success');
                        loadDocuments();
                        answerSection.style.display = 'none';
                        questionInput.value = '';
                    } else {
                        showMessage(`✗ Error: ${data.detail}`, 'error');
                    }
                } catch (error) {
                    showMessage(`✗ Error: ${error.message}`, 'error');
                }
            }
            
            // Load documents on page load
            loadDocuments();
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
