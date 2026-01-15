def splitText(text: str, chunkSize: int = 500, overlap : int = 100):
    chunks = []
    start = 0
    textLength = len(text)

    while start < textLength:
        end = start + chunkSize
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunkSize - overlap

    return chunks    