from fastapi import FastAPI, UploadFile, File
import os
import requests
from pydantic import BaseModel
import json
import faiss

from rag.PDF_loader import extractTextFromPdf
from rag.textSplitter import splitText
from rag.vectorStore import createFaissIndex, searchFaiss
from rag.embeddings import embed_chunks, model # reuse the same model


INDEX_PATH = "data/index/faiss.index"
CHUNKS_PATH = "data/index/chunks.json"

app = FastAPI()

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok = True)

faissIndex = None
storedChunks = None

def saveIndexAndChunks(faissInd, chunks):
    # Save FAISS index
    faiss.write_index(faissInd, INDEX_PATH)
    
    # Save chunks
    with open(CHUNKS_PATH, "w", encoding = "utf-8") as f:
        json.dump(chunks, f, ensure_ascii = False, indent = 2)

def loadIndexAndChunks():
    if not os.path.exists(INDEX_PATH)   or not os.path.exists(CHUNKS_PATH):
        return None, None

    faissInd = faiss.read_index(INDEX_PATH)

    with open(CHUNKS_PATH, "r", encoding = "utf-8") as f:
        chunks = json.load(f)

    return faissInd, chunks   


faissIndex, storedChunks = loadIndexAndChunks()    

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
    #chunks = splitText(text)
    chunks = [
        {"doc": file.filename, "text": chunk}
        for chunk in splitText(text)
    ]
    embeddings = embed_chunks(chunks)

    # storedChunks = chunks
    # faissIndex = createFaissIndex(embeddings)
    if storedChunks is None:
        storedChunks = chunks
        faissIndex = createFaissIndex(embeddings)
    else:
        storedChunks.extend(chunks)
        faissIndex.add(embeddings)    


    # Save the read data to disk
    saveIndexAndChunks(faissIndex, storedChunks)
    
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

def call_llm(prompt: str) -> str:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json = {
            "model": "phi3", # or llama3.1
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]

def build_rag_prompt(question: str, chunks: list[str]) -> str:
    context = "\n\n".join(chunks)
    return f"""
    Use ONLY the context below to answer the question.
    If the answer is not in the context, say "I don't know."

    Context:
    {context}

    Question: {question}
    Answer:
    """

def retrieve_top_chunks(question: str, k: int = 3):
    global faissIndex, storedChunks
    # 1. Embed the question
    query_embedding = model.encode([question]).astype("float32")

    # 2. Search FAISS (your existing function)
    indices = searchFaiss(faissIndex, query_embedding, k)

    # 3. Convert indices → actual chunk text
    return [storedChunks[i] for i in indices]


class QuestionRequest(BaseModel):
    question: str

@app.post("/answer")
def answer_question(payload: QuestionRequest):
    question = payload.question

    top_chunks = retrieve_top_chunks(question, k=3)
    prompt = build_rag_prompt(question, top_chunks)
    answer = call_llm(prompt)

    return {
        "question": question,
        "answer": answer,
        "chunks_used": top_chunks
    }

@app.post("/reset_rag")
def reset_rag():
    global faissIndex, storedChunks

    faissIndex = None
    storedChunks = None

    if os.path.exists(INDEX_PATH):
       os.remove(INDEX_PATH)
    if os.path.exists(CHUNKS_PATH):
        os.remove(CHUNKS_PATH)  

    return {"status": "reset complete"}              


    