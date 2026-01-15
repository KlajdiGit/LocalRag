from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniM-L6-v2")

def embed_chunks(chunks: list[str]) -> list[list[float]]:
    embeddings = model.encode(chunks, show_progress_bar = True)
    return embeddings