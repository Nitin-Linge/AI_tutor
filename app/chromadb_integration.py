import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

import os

UPLOAD_DIR = "./uploaded_books/"

client = chromadb.PersistentClient(path="./chromadb/")

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def create_collection(user_id: str):

    return client.create_collection(user_id) 

def get_collection(user_id: str):
    try:
        return client.get_collection(user_id)
    except:
        return None

def delete_collection(user_id: str):
    # Delete the ChromaDB collection for the user
    try:
        client.delete_collection(user_id)
    except Exception as e:
        print(f"Error deleting collection: {e}")
    
    # Construct the file path based on the user_id (assuming the filename is based on user_id)
    file_path = os.path.join(UPLOAD_DIR, f"{user_id}.pdf")  # Assuming the file is a PDF
    
    # Delete the file if it exists
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"File {file_path} deleted successfully.")
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")
    else:
        print(f"No file found for user {user_id}.")

def add_book_content_to_vdb(user_id: str, book_content: str, chunk_size: int = 500):
    collection = get_collection(user_id)
    if not collection:
        collection = create_collection(user_id)

    chunks = [book_content[i:i+chunk_size] for i in range(0, len(book_content), chunk_size)]
    

    embeddings = model.encode(chunks).tolist() 
    
    for idx, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            ids=[f"{user_id}_chunk_{idx}"],
            embeddings=[embeddings[idx]] 
        )

def query_book_content(user_id: str, query: str, conversation_history: str = ""):

    collection = get_collection(user_id)
    if not collection:
        return None

    combined_query = f"{conversation_history}\n{query}"


    query_embedding = model.encode([combined_query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding, 
        n_results=1
    )
    
    if results["documents"]:
        return results["documents"][0]
    return None
