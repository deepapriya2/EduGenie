import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_text(prompt: str, temperature: float = 0.7, **kwargs) -> str:
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
            config={"temperature": temperature}
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

class GeminiService:
    def ask(self, text: str):
        return generate_text(text)