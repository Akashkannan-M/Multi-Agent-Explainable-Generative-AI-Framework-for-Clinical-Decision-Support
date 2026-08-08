# TODO - Fix Reports, Doctor Analytics, AI Chatbot, and Streamlit UI

## Confirmed root causes

### 1. AI Chatbot not working
- Gemini API key not resolvable in deployment; model/API config needs hardening.
- Fixed: robust key resolution (env/.env/Streamlit secrets), model fallback chain, clear error messages. App still needs a valid GEMINI_API_KEY in Streamlit Cloud secrets to return live AI responses.

### 2. Doctor Specialization duplicates
- `database.py` seeded doctors on every startup with plain INSERT (no UNIQUE) -> duplicates accumulated.
- `doctor_analytics_agent.doctor_specialization()` query had no DISTINCT/GROUP BY.
- Fixed: DISTINCT query + idempotent seeding + UNIQUE index + deduplicated existing rows.

### 3. Streamlit branding
- Fork / GitHub / Streamlit toolbar + footer visible.
- Fixed: toolbarMode=minimal in config.toml + safe CSS in app.py.

## Progress

- [x] Fix `doctor_analytics_agent.py` doctor_specialization to use DISTINCT
- [x] Make `database.py` doctor seeding idempotent + add UNIQUE index
- [x] Deduplicate existing doctor rows in clinical.db
- [x] Harden `_resolve_api_key()` in chatbot_agent.py and genai_agent.py
- [x] Add model fallback chain in chatbot_agent.py
- [x] Pin google-genai in requirements.txt
- [x] Add `client.toolbarMode = "minimal"` to .streamlit/config.toml
- [x] Inject safe CSS in app.py to hide Streamlit footer/menu
- [x] Run comprehensive local verification of all modules
- [x] Test doctor_specialization returns exactly one row per doctor
- [x] Test chatbot path (no-key graceful error + reach-API check)
- [x] Commit all changes (commit a32e3fe)
- [x] Push to origin/main (repo moved to Multi-Agent-Explainable-Generative-AI-Framework-for-Clinical-Decision-Support)
- [ ] Wait for Streamlit Cloud redeploy and verify live app
