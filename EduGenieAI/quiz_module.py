from typing import Any

from config import settings
from gemini_client import GeminiService


def _validate_quiz(
    data: Any,
    topic: str,
    count: int,
    difficulty: str,
) -> dict:

    if not isinstance(data, dict):
        raise ValueError(
            "Quiz response must be a JSON object."
        )

    questions = data.get("questions")

    if not isinstance(questions, list):
        raise ValueError(
            "Quiz response does not contain a questions list."
        )

    if len(questions) != count:
        raise ValueError(
            f"Expected {count} questions but received "
            f"{len(questions)}."
        )

    cleaned_questions = []

    for index, question in enumerate(questions, start=1):

        if not isinstance(question, dict):
            raise ValueError(
                f"Question {index} is invalid."
            )

        question_text = str(
            question.get("question", "")
        ).strip()

        options = question.get("options")

        correct_answer = str(
            question.get("correct_answer", "")
        ).strip()

        explanation = str(
            question.get("explanation", "")
        ).strip()

        if not question_text:
            raise ValueError(
                f"Question {index} has no question text."
            )

        if not isinstance(options, list):
            raise ValueError(
                f"Question {index} options are invalid."
            )

        if len(options) != 4:
            raise ValueError(
                f"Question {index} must contain exactly "
                "4 options."
            )

        options = [
            str(option).strip()
            for option in options
        ]

        if any(not option for option in options):
            raise ValueError(
                f"Question {index} contains an empty option."
            )

        if correct_answer not in options:
            raise ValueError(
                f"Question {index}'s correct_answer must "
                "exactly match one of its options."
            )

        if not explanation:
            raise ValueError(
                f"Question {index} requires an explanation."
            )

        cleaned_questions.append(
            {
                "question": question_text,
                "options": options,
                "correct_answer": correct_answer,
                "explanation": explanation,
            }
        )

    return {
        "topic": topic,
        "difficulty": difficulty,
        "questions": cleaned_questions,
    }


def generate_quiz(
    topic: str,
    count: int = 3,
    difficulty: str = "medium",
) -> dict:

    topic = topic.strip()
    difficulty = difficulty.strip()

    if not topic:
        raise ValueError(
            "Quiz topic cannot be empty."
        )

    if count < 1 or count > 10:
        raise ValueError(
            "Quiz count must be between 1 and 10."
        )

    prompt = f"""
You are EduGenie, an educational quiz generator.

Generate exactly {count} multiple-choice questions about:

TOPIC:
{topic}

DIFFICULTY:
{difficulty}

Return ONLY valid JSON.

Required JSON structure:

{{
  "questions": [
    {{
      "question": "Question text",
      "options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
      ],
      "correct_answer": "The exact correct option text",
      "explanation": "Why this answer is correct"
    }}
  ]
}}

Rules:
- Exactly {count} questions.
- Exactly 4 options for every question.
- Only one correct answer per question.
- correct_answer must exactly match one option.
- Questions must be educational.
- Avoid ambiguous questions.
- Include explanations.
"""

    service = GeminiService()

    try:
        data = service.generate_json(
            prompt,
            temperature=0.3,
        )

        return _validate_quiz(
            data,
            topic,
            count,
            difficulty,
        )

    except Exception as first_error:

        repair_prompt = f"""
You are repairing a JSON quiz response.

Topic:
{topic}

Difficulty:
{difficulty}

Required number of questions:
{count}

The previous response failed validation.

Error:
{first_error}

Generate a completely new valid response.

Return ONLY JSON in this exact structure:

{{
  "questions": [
    {{
      "question": "Question text",
      "options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
      ],
      "correct_answer": "Exact option text",
      "explanation": "Explanation"
    }}
  ]
}}
"""

        data = service.generate_json(
            repair_prompt,
            temperature=0.2,
        )

        return _validate_quiz(
            data,
            topic,
            count,
            difficulty,
        )