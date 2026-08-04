import os
from pathlib import Path
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

from app.config import settings
from app.services import process_and_save_document, ask_rag_system

app = FastAPI(
    title="Enterprise RAG API",
    description="Production-ready RAG API using AWS Bedrock and FAISS",
    version="1.0.0"
)

class QueryRequest(BaseModel):
    question: str

@app.get("/")
def read_root():
    """Root endpoint to check if the API is running."""
    return {"message": "Welcome to Enterprise RAG API powered by AWS Bedrock!"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a PDF or TXT document, process it, and index into FAISS."""
    if not file.filename.endswith((".pdf", ".txt")):
        raise HTTPException(status_code=400, detail="Only .pdf and .txt files are supported.")
    
    data_dir = Path(settings.data_path)
    data_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = data_dir / file.filename
    
    try:
        # Save uploaded file temporarily
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process and index document
        result_message = process_and_save_document(str(file_path), file.filename)
        return {"filename": file.filename, "message": result_message}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
def query_rag(payload: QueryRequest):
    """Ask a question and get an AI-generated answer based on uploaded documents."""
    try:
        response = ask_rag_system(payload.question)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))