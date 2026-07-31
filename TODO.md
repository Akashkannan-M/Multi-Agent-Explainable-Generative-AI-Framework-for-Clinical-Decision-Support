# Task: Fix Gemini API Quota Exceeded (429) Error

## Steps

- [x] 1. Analyze repo structure and understand the issue
- [x] 2. Get user confirmation on model choice (`gemini-1.5-flash`)
- [ ] 3. Fix `agents/genai_agent.py`:
  - Change invalid model name to `gemini-1.5-flash`
  - Add retry with exponential backoff on 429 errors
  - Parse `retry_delay` from error message when available
- [ ] 4. Fix `agents/chatbot_agent.py`:
  - Switch to `google-genai` SDK (consistent with genai_agent.py)
  - Add retry logic with wait on 429
  - Add graceful fallback response when quota exhausted
- [ ] 5. Fix `app.py`:
  - Remove duplicate `chatbot_agent.reply(question)` call (appears twice on consecutive lines)
- [ ] 6. Test and verify fixes

