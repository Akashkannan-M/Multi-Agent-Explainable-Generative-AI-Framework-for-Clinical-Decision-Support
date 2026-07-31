from google import genai
from google.genai import errors
from dotenv import load_dotenv
import os
import time
import re

load_dotenv()

DEFAULT_MODEL = "gemini-1.5-flash"
MAX_RETRIES = 3


class ChatbotAgent:

    def __init__(self, model=None):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not set. Add it to the .env file before using Gemini."
            )

        self.model = model or os.getenv("GEMINI_MODEL", DEFAULT_MODEL)
        self.client = genai.Client(api_key=api_key)

    def _parse_retry_delay(self, error_message):
        """Extract retry delay in seconds from the error message."""
        match = re.search(r'retry in (\d+\.?\d*)s', error_message, re.IGNORECASE)
        if match:
            return float(match.group(1))
        return None

    def reply(self, question):

        prompt = f"""
You are an AI Clinical Decision Support Assistant.

Answer only medical and healthcare related questions.

If the question is outside the medical domain,
politely reply that you only answer medical questions.

Question:
{question}
"""

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt
                )
                return response.text

            except errors.ClientError as exc:
                if exc.code == 429:
                    retry_delay = self._parse_retry_delay(str(exc))

                    if retry_delay is None:
                        retry_delay = min(10 * attempt, 60)

                    if attempt < MAX_RETRIES:
                        time.sleep(retry_delay)
                    else:
                        return (
                            "I'm sorry, but the AI service is temporarily unavailable "
                            "due to API quota limits. Please try again later. "
                            "For urgent medical concerns, please consult a doctor immediately."
                        )
                else:
                    return (
                        f"I'm sorry, an error occurred while processing your request. "
                        f"Please try again later."
                    )

        # Fallback if all retries exhausted
        return (
            "I'm sorry, but the AI service is currently unavailable due to API quota limits. "
            "Please try again later. For urgent medical concerns, please consult a doctor immediately."
        )

