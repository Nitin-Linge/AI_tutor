# app/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from app.pdf_handler import extract_text_from_pdf
from app.openai_integration import ask_openai_question
from app.chromadb_integration import add_book_content_to_vdb, delete_collection
from app.models import QuestionRequest, QuestionResponse, UploadBookResponse
import shutil
import os

app = FastAPI()

BOOK_STORAGE = "uploaded_books"
if not os.path.exists(BOOK_STORAGE):
    os.mkdir(BOOK_STORAGE)

conversation_history = {}

def get_user_file_path(user_id: str) -> str:
    """Get the path of the file uploaded by the user."""
    return os.path.join(BOOK_STORAGE, f"{user_id}_book.pdf")

def remove_user_file(user_id: str):
    """Delete the uploaded file for the given user."""
    user_file_path = get_user_file_path(user_id)
    if os.path.exists(user_file_path):
        os.remove(user_file_path)

@app.post("/upload_book/{user_id}", response_model=UploadBookResponse)
async def upload_book(user_id: str, file: UploadFile = File(...)):
    # If the user has already uploaded a book, remove the old one and its collection
    remove_user_file(user_id)
    delete_collection(user_id)

    # Save the new file with a name corresponding to the user ID
    file_path = get_user_file_path(user_id)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract and store the content from the new PDF file
    book_content = extract_text_from_pdf(file_path)
    if not book_content:
        raise HTTPException(status_code=400, detail="Failed to extract content from the book.")

    # Store the book content in ChromaDB as chunks
    add_book_content_to_vdb(user_id, book_content)

    return UploadBookResponse(message=f"Book uploaded and stored successfully for user '{user_id}'.")

@app.post("/ask_question/{user_id}", response_model=QuestionResponse)
async def ask_question(user_id: str, question: QuestionRequest):
    global conversation_history
    if user_id not in conversation_history:
        conversation_history[user_id] = ""

    answer = ask_openai_question(user_id, question.question, conversation_history[user_id])
    conversation_history[user_id] += f"\n\nQuestion: {question.question}\nAnswer: {answer}"

    return QuestionResponse(answer=answer)

@app.delete("/remove_book/{user_id}", response_model=UploadBookResponse)
async def remove_book(user_id: str):
    """Remove book content for the user from ChromaDB and delete the uploaded file."""
    # Delete the collection from ChromaDB
    delete_collection(user_id)

    # Delete the uploaded file for the user
    remove_user_file(user_id)

    # Clear the conversation history
    if user_id in conversation_history:
        del conversation_history[user_id]

    return UploadBookResponse(message=f"Book content and file for user '{user_id}' removed successfully.")
