from pydantic import BaseModel
from typing import List, Optional

class LearningRequest(BaseModel):
    concept: str
    level: Optional[str] = "beginner"

class QuizRequest(BaseModel):
    topic: str
    num_questions: Optional[int] = 5
    difficulty: Optional[str] = "medium"

class TestRequest(BaseModel):
    text: str


class QARequest(BaseModel):
    question: str
    context: Optional[str] = None

class SummaryRequest(BaseModel):
    text: str
    max_length: Optional[int] = 200

class ExplanationRequest(BaseModel):
    concept: str

class LearningPathRequest(BaseModel):
   
    goal: str
    current_level: Optional[str] = "beginner"
class TextRequest(BaseModel):
     text: str
class ChatRequest(BaseModel):
     message: str