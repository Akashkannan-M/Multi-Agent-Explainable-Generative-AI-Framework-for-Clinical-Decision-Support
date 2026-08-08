from google import genai
from google.genai import errors
from dotenv import load_dotenv
import os

load_dotenv()

DEFAULT_MODEL = "gemini-2.0-flash"


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


class GenAIAgent:

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
            client = self._get_client()
            response = client.models.generate_content(
                model=self.model,
                contents=prompt
            )
        except RuntimeError:
            raise
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
