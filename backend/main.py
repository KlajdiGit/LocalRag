from fastapi import FastAPI, UploadFile, File
import os

from rag.PDF_loader import extractTextFromPdf
from rag.textSplitter import splitText
from rag.vectorStore import createFaissIndex, searchFaiss
from rag.embeddings import embed_chunks, model # reuse the same model


app = FastAPI()

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok = True)

faissIndex = None
storedChunks = None

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
    global faissIndex, storedChunks
    filePath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filePath, "wb") as f:
        f.write(await file.read())

    text = extractTextFromPdf(filePath)
    chunks = splitText(text)
    embeddings = embed_chunks(chunks)

    storedChunks = chunks
    faissIndex = createFaissIndex(embeddings)
    
    return{
        "chunks": len(chunks),
        "embedding_shape": len(embeddings[0]),
        "faiss_index_type": str(type(faissIndex))
    }   

@app.post("/query")
async def query_rag(question: str):
    global faissIndex, storedChunks

    if (faissIndex is None or storedChunks is None):
        return {"ERROR":"No document uploaded yet."}
    
    queryEmbedding = model.encode([question]).astype("float32")
    
    topIndices = searchFaiss(faissIndex, queryEmbedding, k = 3)

    retrieved = [storedChunks[i] for i in topIndices]

    return{
        "question": question,
        "top_chunks": retrieved
    }
    