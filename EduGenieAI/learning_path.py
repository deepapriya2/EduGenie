from config import settings
from gemini_client import GeminiService


def generate_learning_path(
    topic: str,
    current_level: str,
    hours_per_week: float,
    goal: str,
) -> dict:

    topic = topic.strip()
    current_level = current_level.strip()
    goal = goal.strip()

    if not topic:
        raise ValueError(
            "Learning topic cannot be empty."
        )

    if hours_per_week <= 0:
        raise ValueError(
            "Hours per week must be greater than zero."
        )

    prompt = f"""
You are EduGenie, an AI-powered personalized learning assistant.

Create a personalized learning path.

Topic:
{topic}

Current level:
{current_level}

Available study time:
{hours_per_week} hours per week

Learning goal:
{goal}

Create a roadmap from the learner's current level toward the stated goal.

Return ONLY valid JSON using this structure:

{{
  "topic": "{topic}",
  "current_level": "{current_level}",
  "goal": "{goal}",
  "estimated_duration": "Example: 8 weeks",
  "overview": "Short overview",
  "stages": [
    {{
      "stage": 1,
      "title": "Stage title",
      "difficulty": "Beginner",
      "concepts": [
        "Concept 1",
        "Concept 2"
      ],
      "activities": [
        "Activity 1",
        "Activity 2"
      ],
      "project": "Small practical project"
    }}
  ],
  "weekly_schedule": [
    {{
      "week": 1,
      "focus": "Topic focus",
      "study_hours": 5,
      "tasks": [
        "Task 1",
        "Task 2"
      ]
    }}
  ],
  "resources": [
    {{
      "title": "Resource title",
      "type": "Book / Documentation / Course / Practice",
      "description": "Why this resource is useful"
    }}
  ],
  "milestones": [
    "Milestone 1",
    "Milestone 2"
  ]
}}

Rules:
- Start at the learner's current level.
- Progress gradually toward more advanced concepts.
- Match the schedule to the available hours.
- Include practical exercises.
- Include projects where appropriate.
- Do not invent URLs.
- Do not claim a specific course or resource exists unless you are confident it does.
- Keep the roadmap realistic.
"""

    service = GeminiService()

    data = service.generate_json(
        prompt,
        temperature=0.4,
    )

    if not isinstance(data, dict):
        raise ValueError(
            "Learning path response must be a JSON object."
        )

    data.setdefault("topic", topic)
    data.setdefault("current_level", current_level)
    data.setdefault("goal", goal)

    return data