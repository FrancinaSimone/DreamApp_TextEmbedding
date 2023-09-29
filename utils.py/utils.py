import numpy as np
from hashlib import sha256

# Crafting a Unique Sigil:
def generate_unique_id(title):
    """Generate a unique ID using SHA256 hashing."""
    return sha256(title.encode()).hexdigest()

# Understanding the Essence:
def normalize_vector(embedding):
    return embedding / np.linalg.norm(embedding)