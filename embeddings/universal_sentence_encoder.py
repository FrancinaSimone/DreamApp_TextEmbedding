import tensorflow_hub as hub
import numpy as np

# Load the Universal Sentence Encoder model
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

def get_embedding(text):
    return np.array(embed([text])[0])

# Understanding the Spirit's Insight:
def get_embedding(text):
    """Returns a 512-dimensional vector using Universal Sentence Encoder."""
    embeddings = embed([text])
    return embeddings.numpy()[0]
