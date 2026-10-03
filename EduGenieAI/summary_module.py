from config import settings
from gemini_client import GeminiService


def summarize_text(text: str) -> str:
    text = text.strip()

    if not text:
        raise ValueError(
            "Text cannot be empty."
        )

    if len(text) > settings.MAX_INPUT_CHARS:
        raise ValueError(
            f"Text is too long. Maximum allowed length is "
            f"{settings.MAX_INPUT_CHARS} characters."
        )

    prompt = f"""
You are EduGenie, an educational summarization assistant.

Summarize the following text for a student.

TEXT:
{text}

Create a useful educational summary.

Use this structure:

## Summary
A concise explanation of the main idea.

## Key Points
- Important point 1
- Important point 2
- Important point 3

## Important Terms
Explain important technical terms briefly if they appear.

## Quick Revision
Give a short revision section at the end.

Do not introduce information that is not supported by the supplied text.
"""

    service = GeminiService()

    return service.generate(
        prompt,
        temperature=0.3,
    )