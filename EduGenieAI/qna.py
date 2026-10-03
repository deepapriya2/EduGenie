from config import settings
from gemini_client import generate_text


def answer_question(question: str) -> str:
    if len(question) > settings.MAX_INPUT_CHARS:
        raise ValueError(
            f"Question is too long. Maximum allowed length is "
            f"{settings.MAX_INPUT_CHARS} characters."
        )

    prompt = f"""
You are EduGenie, an educational AI learning assistant.

Answer the student's question accurately and clearly.

Student question:
{question}

Instructions:
- Explain the answer in beginner-friendly language.
- Use headings when useful.
- Use examples when helpful.
- Break complicated ideas into smaller steps.
- Do not invent facts.
- If the question is ambiguous, explain the reasonable interpretation.
- Keep the response educational and easy to understand.
"""

    return generate_text(
        prompt,
        temperature=0.3,
    )

    if __name__ == "__main":
        test_q = "What is photosynthesis?"
        print("Terxting EduGenie...")
        print(answer_question(test_q))