from google import genai
from google.genai import errors
from dotenv import load_dotenv
import os
import logging

load_dotenv()

# Use "gemini-flash-latest", an alias Google keeps pointing at the newest
# supported Flash model, to avoid hardcoding a deprecated/removed model.
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-latest")
FALLBACK_MODELS = [
    "gemini-flash-latest",
    "gemini-pro-latest",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
]

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


class GenAIAgent:

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
                    self.model = model
                    return response.text
                last_error = "Empty response from " + model
            except RuntimeError:
                raise  # Missing key -> propagate so app.py can show the message
            except errors.ClientError as exc:
                if exc.code == 429:
                    last_error = exc
                    continue  # quota -> try next supported model
                elif exc.code in (400, 403, 404) and "model" in str(exc).lower():
                    logger.warning("Model %s unavailable: %s", model, exc)
                    last_error = exc
                    continue  # model not supported -> try next
                else:
                    raise RuntimeError(
                        f"Gemini request failed for '{model}' (HTTP {exc.code}): {exc.message}"
                    ) from exc

        # All models failed. Surface the most relevant error.
        if isinstance(last_error, errors.ClientError) and getattr(last_error, "code", None) == 429:
            raise RuntimeError(
                "Gemini API quota is unavailable for all configured models (HTTP 429). "
                "Enable billing on the key's Google AI Studio / Cloud project, or provide "
                "a key with available quota. Detail: " + str(last_error)[:300]
            )
        raise RuntimeError(
            "AI explanation is currently unavailable. None of the configured Gemini "
            "models returned a response."
        )

