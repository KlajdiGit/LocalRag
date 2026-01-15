from fastapi import FastAPI, UploadFile, File
import os

from rag.PDF_loader import extractTextFromPdf

app = FastAPI()

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok = True)

@app.get("/health")
def health_check():
    return {"status" : "ok"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    filePath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filePath, "wb") as f:
         f.write(await file.read())

    text = extractTextFromPdf(filePath)

    return{
        "filename": file.filename,
        "text_preview": text[:500]
    }     
    
    