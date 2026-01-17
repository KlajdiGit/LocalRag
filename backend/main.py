from fastapi import FastAPI, UploadFile, File
import os

from rag.PDF_loader import extractTextFromPdf
from rag.textSplitter import splitText
from rag.vectorStore import createFaissIndex
from rag.embeddings import embed_chunks

app = FastAPI()

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok = True)


@app.get("/")
def root():
    return {
        "message": "Welcome to LocalRAG API",
        "docs": "/docs",
        "health": "/health",
        "upload_pdf": "/upload",
        "test_rag": "/test_rag"
    }

@app.get("/health")
def health_check():
    return {"status" : "ok"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    filePath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filePath, "wb") as f:
         f.write(await file.read())

    text = extractTextFromPdf(filePath)
    chunks = splitText(text)

    return{
        "filename": file.filename,
        "text_preview": text[:500]
    }  

@app.post("/test_rag")
async def test_rag(file: UploadFile = File(...)):
    filePath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filePath, "wb") as f:
        f.write(await file.read())

    text = extractTextFromPdf(filePath)
    chunks = splitText(text)
    embeddings = embed_chunks(chunks)
    index = createFaissIndex(embeddings)

    return{
        "chunks": len(chunks),
        "embedding_shape": len(embeddings[0]),
        "faiss_index_type": str(type(index))
    }     
    
    