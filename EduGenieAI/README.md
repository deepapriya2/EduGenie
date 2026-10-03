# EduGenieAI - AI Education Assistant

EduGenieAI is a FastAPI based AI learning assistant.

## How to Run

1. Install packages:
   pip install fastapi uvicorn pydantic

2. Start Server:
   python -m uvicorn main:app --reload

3. Open Browser:
   http://127.0.0.1:8000/docs

## API Endpoints

### 1. Health Check
- GET /health
- Response: {"status": "ok"}

### 2. Q&A
- POST /qa
- Body: {"question": "What is photosynthesis?"}

### 3. Explain Topic
- POST /explain
- Body: {"topic": "Black Hole"}

### 4. Quiz Generator
- POST /quiz
- Body: {"topic": "Solar System", "count": 5}

### 5. Summarize
- POST /summarize
- Body: {"text": "Long paragraph here..."}

### 6. Learn Recommendations
- POST /learn/recommendations
- Body: {"question": "I want to learn Python from scratch"}

## Tech Stack
- Python
- FastAPI
- Uvicorn

Developed by: [Un Name]