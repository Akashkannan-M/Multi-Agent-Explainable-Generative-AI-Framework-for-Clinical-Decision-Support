from google import genai
from google.genai import errors
from dotenv import load_dotenv
import os

load_dotenv()

DEFAULT_MODEL = "gemini-3.5-flash-lite"


class GenAIAgent:

    def __init__(self, model=None):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not set. Add it to the .env file before using Gemini."
            )

        self.model = model or os.getenv("GEMINI_MODEL", DEFAULT_MODEL)
        self.client = genai.Client(api_key=api_key)

    def generate_response(self, disease, confidence, recommendations):

        prompt = f"""
You are an AI Medical Assistant.

Predicted Disease:
{disease}

Confidence:
{confidence}%

Recommendations:
{recommendations}

Explain this disease in simple English.
Also give health precautions.
Keep the explanation short.
"""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
        except errors.ClientError as exc:
            if exc.code == 429:
                raise RuntimeError(
                    f"Gemini quota is unavailable for '{self.model}'. "
                    "Use a model enabled for this API key, wait for the quota reset, "
                    "or enable billing in Google AI Studio."
                ) from exc

            raise RuntimeError(
                f"Gemini request failed for '{self.model}' (HTTP {exc.code}): {exc.message}"
            ) from exc

        return response.text
