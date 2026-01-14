from pypdf import PdfReader

def extractTextFromPdf(file_path: str) -> str:
    """
    Extracts text from a PDF file and returns it as a single string. 
    """
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        pageText = page.extract_text()
        if pageText:
            text += pageText + "\n"

    return text.strip()        