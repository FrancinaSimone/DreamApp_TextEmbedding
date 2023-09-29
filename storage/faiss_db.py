import faiss
import numpy as np

# Summoning the Magic Mirror: or Initialize the FAISS index
faiss_index = faiss.IndexFlatL2(512)

class FaissDB:
    def __init__(self, embedding_dim):
        self.index = faiss.IndexFlatL2(embedding_dim)

    def add(self, embeddings, ids):
        """Add embeddings to the database."""
        self.index.add_with_ids(embeddings, ids)

    def search(self, embedding, k=1):
        """Find k most similar embeddings in the database."""
        distances, indices = self.index.search(embedding, k)
        return distances, indices
