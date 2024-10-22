from app.chromadb_integration import query_book_content
from dotenv import load_dotenv
import openai
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_openai_question(user_id: str, question: str, conversation_history: str = "") -> str:
    
    # Retrieve relevant content from the vector database (ChromaDB)
    relevant_chunk = query_book_content(user_id, question, conversation_history)
    
    # If no relevant chunk is found
    if not relevant_chunk:
        return "No relevant content found in the book."

    # Prepare the conversation history and add the relevant chunk
    messages = [
        {"role": "system", "content": "You are an AI tutor."},
        {"role": "user", "content": f"Here is the relevant content from the book: {relevant_chunk}"},
        {"role": "user", "content": question}
    ]
    
    # If there's any previous conversation history, add that as well
    if conversation_history:
        messages.insert(1, {"role": "assistant", "content": conversation_history})

    # Call the OpenAI Chat Completion API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if using GPT-4
        messages=messages,
        max_tokens=500,
        temperature=0.7,
    )
    
    # Return the assistant's response
    return response['choices'][0]['message']['content'].strip()
