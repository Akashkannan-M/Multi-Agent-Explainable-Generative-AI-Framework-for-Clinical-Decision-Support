from google import genai
from google.genai import errors
from dotenv import load_dotenv
import os
import time
import re
import logging

load_dotenv()

# Order of preference for models. "gemini-flash-latest" is an alias that
# Google keeps pointing at the newest supported Flash model, so it is a good
# resilient default that avoids hardcoding a deprecated/removed model.
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-latest")
FALLBACK_MODELS = [
    "gemini-flash-latest",
    "gemini-pro-latest",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
]
MAX_RETRIES = 3

logger = logging.getLogger(__name__)


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
        self.model = model or DEFAULT_MODEL
        self.api_key = _resolve_api_key()
        self.client = None

    def _get_client(self):
        if self.client is None:
            if not self.api_key:
                raise RuntimeError(
                    "GEMINI_API_KEY is not set. Configure it as a Render "
                    "environment variable or Streamlit secret to use the AI feature."
                )
            self.client = genai.Client(api_key=self.api_key)
        return self.client

    def _parse_retry_delay(self, error_message):
        """Extract retry delay in seconds from the error message."""
        match = re.search(r'retry in (\d+\.?\d*)s', error_message, re.IGNORECASE)
        if match:
            return float(match.group(1))
        return None

    def _quota_message(self, exc):
        """Return a clear, actionable message for 429 quota errors."""
        return (
            "Gemini API quota is currently exhausted for this API key. "
            "Enable billing at https://ai.google.dev/google-api or use a key "
            "with available quota, then set GEMINI_API_KEY in Render. "
            "Detail: " + str(exc)[:300]
        )

    def reply(self, question):

        prompt = f"""
    You are an AI Clinical Decision Support Assistant.

    Answer only medical and healthcare related questions.

    If the question is outside the medical domain,
    politely reply that you only answer medical questions.

    Question:
    {question}
    """

        models_to_try = [self.model] + [
            m for m in FALLBACK_MODELS if m != self.model
        ]
        last_error = None

        for model in models_to_try:
            try:
                client = self._get_client()
                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )
                if response and response.text:
                    # Remember the working model for subsequent calls.
                    self.model = model
                    return response.text
                last_error = "Empty response from " + model
            except RuntimeError as e:
                # Missing API key - abort immediately with the message.
                return str(e)
            except errors.ClientError as exc:
                if exc.code == 429:
                    last_error = exc
                    retry_delay = self._parse_retry_delay(str(exc))
                    # If there is a short retry window, honor it once.
                    if retry_delay is not None and retry_delay <= 5:
                        time.sleep(retry_delay)
                    # Try the next fallback model before giving up.
                    continue
                elif exc.code in (400, 403, 404) and "model" in str(exc).lower():
                    logger.warning("Model %s unavailable: %s", model, exc)
                    last_error = exc
                    continue  # model not supported -> try next
                else:
                    return f"Gemini Error (HTTP {exc.code}): {exc.message}"
            except Exception as e:
                return f"Unexpected Error: {str(e)}"

        # All models failed. If the last one was a quota error, say so clearly.
        if isinstance(last_error, errors.ClientError) and getattr(last_error, "code", None) == 429:
            return (
                "AI service is currently unavailable because the Gemini API key "
                "has exhausted its quota (HTTP 429). Enable billing on the key's "
                "Google AI Studio / Cloud project, or provide a key with available "
                "quota. No supported model could be reached."
            )
        return "AI service is currently unavailable. None of the configured Gemini models returned a response."

