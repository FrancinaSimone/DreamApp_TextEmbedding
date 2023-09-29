import psycopg2
from config.config_secrets import DATABASE_CREDENTIALS

DATABASE_CREDENTIALS = DATABASE_CREDENTIALS

def create_text_embeddings_table():
    try:
        conn = psycopg2.connect(**DATABASE_CREDENTIALS)
        cursor = conn.cursor()
        
        # Check if the 'dreams' table already exists
        cursor.execute("SELECT EXISTS(SELECT FROM information_schema.tables WHERE table_name='dreams');")
        table_exists = cursor.fetchone()[0]

        if not table_exists:
            create_table_query = '''
            CREATE TABLE TextEmbeddings (
                story_id TEXT PRIMARY KEY,
                culture_name TEXT,
                title TEXT,
                embedding REAL[] -- Assuming the embedding is a 1D array of REAL numbers
            );
            '''
            
            cursor.execute(create_table_query)
            conn.commit()
            
            print("Table 'TextEmbeddings' created successfully!")
        else:
            print("Table 'dreams' already exists.")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL or executing the SQL command:", error)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    create_text_embeddings_table()


# Storing Treasures in the Vault:
def insert_into_postgresql(story_id, culture_name, title, embedding):
    """Insert metadata, culture_name, title, and embedding into PostgreSQL."""
    try:
        with psycopg2.connect(**DATABASE_CREDENTIALS) as conn:
            with conn.cursor() as cursor:
                insert_query = """
                INSERT INTO TextEmbeddings (story_id, culture_name, title, embedding)
                VALUES (%s, %s, %s, %s);
                """
                cursor.execute(insert_query, (story_id, culture_name, title, embedding))
            conn.commit()
    except Exception as e:
        print(f"Error inserting into PostgreSQL: {e}")


# Fetching Tales from the Vault:
def fetch_stories_by_ids(story_ids):
    """Fetch stories from PostgreSQL using a list of story IDs."""
    stories = []
    try:
        with psycopg2.connect(**DATABASE_CREDENTIALS) as conn:
            with conn.cursor() as cursor:
                select_query = """
                SELECT story_id, culture_name, title, embedding 
                FROM TextEmbeddings 
                WHERE story_id = ANY(%s);
                """
                cursor.execute(select_query, (story_ids,))
                stories = cursor.fetchall()
    except Exception as e:
        print(f"Error fetching stories from PostgreSQL: {e}")
    
    return stories