# Implementation Plan — Mentor: AI Conversational Wealth Coach

## Phase 1: MVP (Completed ✅)

| Task | Status |
|---|---|
| Streamlit app scaffold | ✅ |
| Groq + Llama 3.1 8B integration | ✅ |
| System prompt with mentor personality & guardrails | ✅ |
| Chat UI with session history | ✅ |
| Quick-reply suggestion buttons | ✅ |
| Compounding calculator with Plotly chart | ✅ |
| `.env` based API key management | ✅ |
| `.gitignore` for safe GitHub publishing | ✅ |

---

## Phase 2: Enhanced Personalization (Next)

| Task | Priority | Notes |
|---|---|---|
| Onboarding flow — collect income & expenses conversationally | High | Store in session_state, inject into system prompt as user context |
| Surplus calculator — auto-compute investable amount | High | income - expenses = surplus, show in sidebar |
| Risk profiling — 3-question quiz (conservative / moderate / aggressive) | Medium | Tag user profile, adjust chart default rate accordingly |
| Persist user context across turns in system prompt | High | Append "User context: income=X, surplus=Y, risk=Z" to system prompt dynamically |

---

## Phase 3: Content & UX Depth

| Task | Priority | Notes |
|---|---|---|
| Expand asset class coverage (NPS, ELSS, REITs, Gold) | Medium | Add to system prompt knowledge section |
| Goal-based planning mode ("I want to buy a car in 3 years") | Medium | Reverse-calculate required monthly SIP |
| Comparison table renderer — trigger on "compare X vs Y" | Low | Parse intent, render st.dataframe |
| Chat history export (PDF / text) | Low | Allow users to save their session |

---

## Phase 4: Production Readiness

| Task | Priority | Notes |
|---|---|---|
| Streamlit Cloud deployment | High | Add `secrets.toml` support for API key |
| Streaming responses (`stream=True`) | Medium | Better UX — responses appear word by word |
| Rate limiting & error handling | High | Handle Groq API errors gracefully |
| Prompt injection hardening | High | Add input sanitisation layer |
| Analytics — track question categories, session length | Low | Mixpanel or simple logging |
| Multilingual support (Hindi) | Low | Detect language, respond in kind |

---

## Deployment (Streamlit Cloud)

1. Push repo to GitHub (`.env` excluded via `.gitignore`)
2. Go to [share.streamlit.io](https://share.streamlit.io) → New app → connect repo
3. Add secret: `Settings → Secrets → GROQ_API_KEY = "gsk_..."`
4. Deploy — app is live at `https://<your-app>.streamlit.app`
