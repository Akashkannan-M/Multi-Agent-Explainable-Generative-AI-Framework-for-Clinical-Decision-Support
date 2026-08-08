# TODO - Deployment Fixes

## Status: All fixes implemented and pushed to `main`

## 1. AI Chatbot / AI Clinical Explanation

- **Root cause:** The Gemini API key had exhausted its free-tier quota (HTTP 429
  `Quota exceeded ... limit: 0`) for every model, and the hardcoded default
  `gemini-2.0-flash` / `gemini-2.5-pro` names may not match models enabled for
  the key. The app was correctly surfacing the 429 error.
- **Fix (agents/chatbot_agent.py, agents/genai_agent.py):**
  - Default model changed to `gemini-flash-latest` (a maintained alias).
  - Added a fallback model list (`gemini-flash-latest`, `gemini-pro-latest`,
    `gemini-2.5-flash`, `gemini-2.0-flash`) so a single unsupported model does
    not kill the feature.
  - Clear, actionable quota messages instead of generic errors.
  - API key resolves from env var, `.env`, or Streamlit/Render secrets — never
    hardcoded.
- **Action required by user:** The API key must be set as a Render environment
  variable `GEMINI_API_KEY` using a valid key with available quota / billing.

## 2. Doctor Specialization — Duplicates

- **Root cause:** `doctor_specialization()` in `agents/doctor_analytics_agent.py`
  selected `doctor_name, specialization` from `doctors` without `DISTINCT` /
  `GROUP BY`. The seed data in `database/database.py` inserts the same 3 doctors
  on every startup only if they are absent, but prior runs accumulated duplicate
  rows (e.g. 2 rows each) which then all appeared.
- **Fix:** `doctor_specialization()` now uses `SELECT DISTINCT doctor_name,
  specialization FROM doctors`. Each doctor appears exactly once.
  - Also added `UNIQUE`-style dedupe in the seed insert (guarded by a check) so
    duplicates are not re-added on future startups.

## 3. Streamlit UI / Branding Cleanup

- **Fix (.streamlit/config.toml + app.py CSS):**
  - `toolbarMode = "minimal"` removes the Fork / GitHub / Share items while
    keeping the theme (Light/Dark) toggle.
  - CSS hides the Streamlit footer ("Hosted with Streamlit") and the main menu.
  - Removed the aggressive rule that hid `[data-testid="stToolbar"]` entirely
    (that was breaking the theme toggle). The toolbar is now kept visible so the
    Light/Dark toggle works.

## Deployment

- [x] Local compile checks pass for app.py and all touched agents.
- [x] Committed to `main`: `1e20959`
- [x] Pushed to `origin/main` (verified via `git ls-remote`).
- [x] Render must be pointed at the GitHub repo to auto-redeploy.
