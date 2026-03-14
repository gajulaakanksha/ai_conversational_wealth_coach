# Design Document — Mentor: AI Conversational Wealth Coach

## 1. Overview

Mentor is a conversational AI application that helps first-time investors in India understand personal finance concepts through a chat interface. It uses Llama 3.1 8B (via Groq) as the language model, guided by a carefully crafted system prompt that enforces the "educational mentor" personality and guardrails.

---

## 2. Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Streamlit Frontend                  │
│                                                     │
│  ┌─────────────────┐      ┌──────────────────────┐  │
│  │   Chat Panel    │      │  Sidebar             │  │
│  │  - Chat history │      │  - API key input     │  │
│  │  - Chat input   │      │  - Compounding chart │  │
│  │  - Quick reply  │      │  - SIP calculator    │  │
│  └────────┬────────┘      └──────────────────────┘  │
└───────────┼─────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────┐
│   Groq API (LLM Layer)  │
│   Model: llama-3.1-8b-instant │
│   + System Prompt       │
└─────────────────────────┘
```

---

## 3. Component Breakdown

### 3.1 System Prompt
The core of the mentor's behavior. It defines:
- Role: educational financial coach for Indian first-time investors
- Tone: warm, simple, analogy-driven
- Guardrails: no specific product recommendations, no return guarantees, out-of-scope deflection
- Context: Indian financial instruments (₹, SEBI, 80C, SIP, etc.)

### 3.2 Chat Panel
- Built with `st.chat_message` and `st.chat_input`
- Maintains full conversation history in `st.session_state.messages`
- Passes `[system_prompt] + [chat_history]` to Groq on every turn
- Quick-reply buttons surface on first load to reduce blank-slate anxiety

### 3.3 Compounding Calculator (Sidebar)
- Pure Streamlit sliders: monthly investment, time horizon, expected return
- Plotly line chart showing 3 scenarios: conservative (6%), moderate (user-set), aggressive (16%)
- `st.metric` cards for total invested vs projected value
- All calculations are client-side (no API call needed)

### 3.4 Environment & Config
- API key loaded from `.env` via `python-dotenv`
- Falls back to sidebar text input if `.env` key is absent
- `@st.cache_resource` used to avoid re-initialising the Groq client on every rerender

---

## 4. Data Flow

```
User types message
      │
      ▼
Append to session_state.messages
      │
      ▼
Build API payload:
  [system_prompt] + session_state.messages[1:]  ← skip welcome msg
      │
      ▼
groq.chat.completions.create(model="llama-3.1-8b-instant")
      │
      ▼
Append response to session_state.messages
      │
      ▼
st.rerun() → re-render chat
```

---

## 5. Guardrail Design

Guardrails are enforced at the system prompt level (LLM-side), not in application code. This means:

| Scenario | Behavior |
|---|---|
| User asks "which fund should I buy?" | LLM declines to name a fund, explains why |
| User asks about tax filing / ITR | LLM redirects to CA / SEBI advisor |
| User asks for return guarantees | LLM qualifies with "historically" / "estimated" |
| First session load | Welcome message surfaces disclaimer upfront |

---

## 6. Key Design Decisions

| Decision | Rationale |
|---|---|
| Groq over OpenAI | Free tier, faster inference for Llama 3.1 8B |
| System prompt guardrails over code-level filters | More flexible, handles edge cases naturally via LLM reasoning |
| Single-file app (`app.py`) | Simplicity for prototype; easy to demo and deploy |
| Plotly for chart | Richer interactivity than `st.line_chart` |
| `.env` + sidebar fallback | Works locally and on hosted platforms (Streamlit Cloud) |

---

## 7. Limitations (Prototype Scope)

- No persistent storage — chat history resets on page refresh
- No user authentication or profiles
- Responses depend on Groq API availability
- Not tested for adversarial prompt injection
- Financial data in system prompt is static (not live market data)
