from config import settings
from gemini_client import GeminiService


_local_pipeline = None


def _local_explanation(concept: str) -> str:
    global _local_pipeline

    try:
        from transformers import pipeline
    except ImportError as exc:
        raise RuntimeError(
            "Local explanation requires transformers. "
            "Install requirements-local.txt."
        ) from exc

    if _local_pipeline is None:
        _local_pipeline = pipeline(
            "text2text-generation",
            model=settings.LOCAL_EXPLANATION_MODEL,
        )

    prompt = f"""
Explain the following concept to a beginner.

Concept:
{concept}

Give:

1. Simple definition
2. How it works
3. Simple example
4. Important points

Use simple language.
"""

    result = _local_pipeline(
        prompt,
        max_new_tokens=500,
        do_sample=False,
    )

    if not result:
        raise RuntimeError(
            "The local explanation model returned no result."
        )

    return result[0]["generated_text"].strip()


def _gemini_explanation(concept: str) -> str:
    prompt = f"""
You are EduGenie, a patient and highly effective teacher.

Explain this concept to a beginner:

{concept}

Structure the answer as:

## Simple Definition
Explain it in very simple words.

## How It Works
Explain the main idea step by step.

## Example
Give a practical example.

## Key Points
List the most important things to remember.

Avoid unnecessary technical jargon.
"""

    service = GeminiService()

    return service.generate(
        prompt,
        temperature=0.4,
    )


def explain_concept(concept: str) -> str:
    concept = concept.strip()

    if not concept:
        raise ValueError(
            "Concept cannot be empty."
        )

    if len(concept) > settings.MAX_INPUT_CHARS:
        raise ValueError(
            f"Concept is too long. Maximum allowed length is "
            f"{settings.MAX_INPUT_CHARS} characters."
        )

    provider = settings.EXPLANATION_PROVIDER.lower()

    if provider == "local":
        try:
            return _local_explanation(concept)
        except Exception as local_error:
            fallback = _gemini_explanation(concept)

            return (
                f"{fallback}\n\n"
                "Note: The configured local explanation model "
                f"was unavailable, so Gemini was used instead. "
                f"Technical detail: {local_error}"
            )

    return _gemini_explanation(concept)
    if __name__ == "__main__":
         concept = input("Enter concept:")
         print(explain_concept(concept))