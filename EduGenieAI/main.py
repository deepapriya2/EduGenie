from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    question: str

class ExplainRequest(BaseModel):
    topic: str

class QuizRequest(BaseModel):
    topic: str
    count: int = 5

class SummarizeRequest(BaseModel):
    text: str

@app.get("/")
def root():
    return {"message": "EDUGENIE Running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/qa")
def qa(data: Query):
    return {"answer": f"Answer for: {data.question}"}

@app.post("/explain")
def explain(data: ExplainRequest):
    return {"explanation": f"Explanation for: {data.topic}"}

@app.post("/quiz")
def quiz(data: QuizRequest):
    return {"quiz": f"Quiz for: {data.topic} - {data.count} questions"}

@app.post("/summarize")
def summarize(data: SummarizeRequest):
    return {"summary": f"Summary for: {data.text[:50]}..."}

# ITHU THAAN DA MISSING-A IRUNTHATHU!
@app.post("/learn/recommendations")
def recommendations(data: Query):
    return {"recommendations": [f"Start with basics of {data.question}", "Practice daily", "Watch tutorials"]}