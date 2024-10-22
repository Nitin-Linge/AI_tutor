from pydantic import BaseModel

class QuestionRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    answer: str

class UploadBookResponse(BaseModel):
    message: str
