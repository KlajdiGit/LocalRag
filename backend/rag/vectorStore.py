import faiss
import numpy as np

def createFaissIndex(embeddings : list[list[float]]):

    vectors = np.array(embeddings).astype("float32")

    # Get the dimension of the vectors
    # vector [x][384] --> we need to know how many numbers
    # do we have per vector
    dimension = vectors.shape[1]
    
    # Create a FAISS index (L2 distance)
    index = faiss.IndexFlatL2(dimension)
    index.add(vectors)

    return index