from google import genai
from google.genai import errors
from dotenv import load_dotenv
import os
import time
import re

load_dotenv()

DEFAULT_MODEL = "gemini-2.0-flash"
MAX_RETRIES = 3


def _resolve_api_key():
    """Return the Gemini API key from the environment, .env, or Streamlit secrets."""
    key = os.getenv("GEMINI_API_KEY")
    if key:
        return key.strip()
    # Try .env file (in case load_dotenv was not picked up)
    try:
        from dotenv import dotenv_values
        env_vals = dotenv_values(".env")
        key = env_vals.get("GEMINI_API_KEY")
        if key:
            return key.strip()
    except Exception:
        pass
    try:
        import streamlit as st
        key = st.secrets.get("GEMINI_API_KEY")
        return key.strip() if key else None
    except Exception:
        return None


class ChatbotAgent:

    def __init__(self, model=None):
        # Defer API key validation until it is actually used so that the
        # app can still start (login, dashboards, etc.) even if the Gemini
        # API key is not present in the environment.
        self.model = model or os.getenv("GEMINI_MODEL", DEFAULT_MODEL)
        self.api_key = _resolve_api_key()
        self.client = None

    def _get_client(self):
        if self.client is None:
            if not self.api_key:
                raise RuntimeError(
                    "GEMINI_API_KEY is not set. Configure it as a Streamlit "
                    "secret or environment variable to use the AI feature."
                )
            self.client = genai.Client(api_key=self.api_key)
        return self.client

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
                client = self._get_client()

                response = client.models.generate_content(
                    model=self.model,
                    contents=prompt
                )

                return response.text

            except RuntimeError as e:
                return str(e)

            except errors.ClientError as exc:

                # Model not enabled for this API key -> try a fallback model.
                if exc.code in (400, 404, 403) and "model" in str(exc).lower():
                    fallback = self._try_fallback(prompt)
                    if fallback is not None:
                        return fallback

                if exc.code == 429:

                    retry_delay = self._parse_retry_delay(str(exc))

                    if retry_delay is None:
                        retry_delay = min(10 * attempt, 60)

                        if attempt < MAX_RETRIES:
                            time.sleep(retry_delay)

                        else:
                            return (
                                "Gemini API quota exceeded. "
                                "Please try again later."
                            )

                else:
                    return f"Gemini Error (HTTP {exc.code}): {exc.message}"

            except Exception as e:
                return f"Unexpected Error: {str(e)}"

        return "AI service is currently unavailable."

    def _try_fallback(self, prompt):
        """Try alternative Gemini models that are commonly enabled by default."""
        candidates = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-flash-8b"]
        tried = {self.model}
        for model in candidates:
            if model in tried:
                continue
            tried.add(model)
            try:
                client = self._get_client()
                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )
                if response and response.text:
                    self.model = model
                    return response.text
            except Exception:
                continue
        return None

