This project is a AI tutor system that uses **ChromaDB** to store book content in chunks and allows users to query that content. It also integrates **OpenAI** for question-answering based on the stored book content. Users can upload books, store their content in a vector database, and interact with the content via natural language queries.

## Features

- **Book Upload**: Upload a book (PDF) for content extraction and storage in ChromaDB.
- **Chunk Storage**: Book content is split into chunks and stored in a vector database.
- **Querying**: Users can ask questions related to the content, and the app will retrieve relevant chunks.
- **OpenAI Integration**: The app integrates with OpenAI's GPT model to provide human-like responses based on the content retrieved from the book.
- **Book Deletion**: Users can delete their books, including associated content and data in the vector database.

## Prerequisites

Before you begin, make sure you have the following installed:

- **Python 3.8+**
- **Docker** (for containerization)
- **OpenAI API Key** (add to `.env` file)
- **ChromaDB** (Vector database)

## Project Setup

### 1. Clone the repository

```bash
git clone https://github.com/Nitin-Linge/AI_tutor
cd chromadb-book-app
```

### 2. Install Python Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 3. Set up Environment Variables

Create a `.env` file in the root of the project and add your **OpenAI API key**:

```
OPENAI_API_KEY=your_openai_api_key
```

### 4. Running the Application Locally

To run the application locally without Docker:

```bash
uvicorn app.main:app --reload
```

The app will be accessible at `http://localhost:8000`.

## Usage

### 1. Uploading a Book

You can upload a PDF book using the `/upload_book/{user_id}` endpoint by sending a `POST` request with the file.

### 2. Asking Questions

You can ask questions about the uploaded book using the `/ask_question/{user_id}` endpoint by sending a `POST` request with a question.

**payload**

{
    "question": "user question"
}

### 3. Removing a Book

To remove a book and its associated content, send a `DELETE` request to the `/remove_book/{user_id}` endpoint.

## API Endpoints

- **POST /upload_book/{user_id}**: Uploads a PDF book for the user.
- **POST /ask_question/{user_id}**: Queries the uploaded book content.
- **DELETE /remove_book/{user_id}**: Removes the book content and uploaded file.

## Docker Instructions

### 1. Build Docker Image

To build the Docker image for the project:

```bash
docker build -t ai_tutor .
```

### 2. Run the Docker Container

Once the image is built, you can run the container:

```bash
docker run -d -p 8000:8000 ai_tutor
```

This will start the application, and it will be accessible at `http://localhost:8000`.

## Deployment Instructions

To deploy the application:

1. **Ensure Docker is installed** on the server.
2. **Clone the repository** on the server.
3. **Build the Docker image** using the steps provided in the Docker Instructions section.
4. **Run the container** using the provided `docker run` command.