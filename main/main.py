from embeddings.universal_sentence_encoder import get_embedding
from storage.faiss_db import FaissDB
from database.postgres_db import create_text_embeddings_table
from utils.utils import normalize_vector, generate_unique_id
from database.postgres_db import insert_into_postgresql, fetch_stories_by_ids
from config.config_secrets import DATABASE_CREDENTIALS

#  other imports
import faiss
import psycopg2
import tensorflow_hub as hub
import numpy as np


# Storing the Essence and the Story:
def insert_story_and_embedding(culture_name, title, text):
    embedding = get_embedding(text)  # Generate embedding from text
    embedding = normalize_vector(embedding)  # Normalize the embedding
    story_id = generate_unique_id(title)

    # Convert the NumPy array to a list **Remember to convert back into NumPy for FAISS
    embedding_list = embedding.tolist()

    # Store the story in PostgreSQL along with the embedding list
    insert_into_postgresql(story_id, culture_name, title, embedding_list)

    # Store the normalized embedding in Faiss
    faiss_index.add(np.array([embedding]))


# Seeking Similar Tales:
def get_similar_stories(query_text, top_k=5):
    query_embedding = get_embedding(query_text)
    query_embedding = normalize_vector(query_embedding).reshape(1, -1)  # Normalize the query embedding
    _, indices = faiss_index.search(query_embedding, top_k)
    
    story_ids = [story[0] for story in fetch_stories_by_ids(indices[0])]
    return story_ids

    # Preserving the Magic Mirror's Knowledge:
def save_faiss_index(filename="faiss_index.index"):
    """Save the Faiss index to a file."""
    faiss.write_index(faiss_index, filename)

def load_faiss_index(filename="faiss_index.index"):
    """Load the Faiss index from a file."""
    global faiss_index
    faiss_index = faiss.read_index(filename)

# Modify this function to retrieve data from the PostgreSQL database
def process_data_from_database():
    try:
        with psycopg2.connect(**DATABASE_CREDENTIALS) as conn:
            with conn.cursor() as cursor:
                select_query = """
                SELECT culture_name, title, text
                FROM mythology;
                """
                cursor.execute(select_query)
                rows = cursor.fetchall()
                for row in rows:
                    culture_name, title, data = row
                    insert_story_and_embedding(culture_name, title, data)
    except Exception as e:
        print(f"Error fetching data from PostgreSQL: {e}")

# Call the modified data retrieval function
process_data_from_database()

try:
    load_faiss_index()
except Exception as e:
    print(f"Error: {e}")