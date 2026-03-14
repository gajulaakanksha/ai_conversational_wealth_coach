# 💬 Mentor — AI Conversational Wealth Coach

An AI-powered financial mentor for first-time investors. Ask questions about investing in plain language and get clear, jargon-free answers — like talking to a knowledgeable friend.

Built with **Streamlit** + **Llama 3.1 8B** (via Groq).

---

## Features

- Conversational chat interface powered by Llama 3.1 8B
- Explains Mutual Funds, FDs, SIPs, PPF, risk, and more
- Side-by-side asset class comparisons
- Compounding calculator with interactive chart (conservative / moderate / aggressive scenarios)
- Guardrails — stays educational, never recommends specific products
- Loads API key from `.env` automatically

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        Browser / User                        │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                     Streamlit App (app.py)                   │
│                                                              │
│  ┌─────────────────────────┐   ┌──────────────────────────┐  │
│  │       Chat Panel        │   │         Sidebar          │  │
│  │  ─────────────────────  │   │  ──────────────────────  │  │
│  │  • st.chat_message      │   │  • API key input / .env  │  │
│  │  • st.chat_input        │   │  • Monthly SIP slider    │  │
│  │  • Quick-reply buttons  │   │  • Time horizon slider   │  │
│  │  • Session history      │   │  • Return rate slider    │  │
│  │    (session_state)      │   │  • Plotly compound chart │  │
│  └────────────┬────────────┘   │  • st.metric summary     │  │
│               │                └──────────────────────────┘  │
└───────────────┼──────────────────────────────────────────────┘
                │
                │  [system_prompt] + [chat_history]
                ▼
┌──────────────────────────────────────────────────────────────┐
│                        Groq API                              │
│                  Model: llama-3.1-8b-instant                 │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            │  AI response
                            ▼
                     Rendered in chat
```

### Data Flow

```
User message
    │
    ├─► Append to session_state.messages
    │
    ├─► Build payload: [system_prompt] + messages[1:]
    │
    ├─► groq.chat.completions.create()
    │
    ├─► Append response to session_state.messages
    │
    └─► st.rerun() → re-render chat
```

---

## Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/your-username/mentor-wealth-coach.git
cd mentor-wealth-coach
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up your API key

Copy `.env.example` to `.env` and add your Groq API key:
```bash
cp .env.example .env
```

Edit `.env`:
```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free key at [console.groq.com](https://console.groq.com).

### 4. Run the app
```bash
streamlit run app.py
```

Opens at `http://localhost:8501`

---

## Project Structure

```
mentor-wealth-coach/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .env                    # API keys (not committed)
├── .env.example            # Template for environment variables
├── .gitignore              # Git ignore rules
├── questions.md            # Sample questions to test the app
├── PRD.md                  # Product Requirement Document
├── DESIGN.md               # Architecture & design decisions
├── IMPLEMENTATION_PLAN.md  # Roadmap & future phases
└── README.md               # This file
```

---

## Deploying to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → New app → select your repo
3. Add your secret: `Settings → Secrets`
```toml
GROQ_API_KEY = "gsk_..."
```
4. Deploy — your app will be live at `https://<your-app>.streamlit.app`

---

## Sample Questions

See [`questions.md`](questions.md) for a full list. Quick examples:

- "What is a Mutual Fund?"
- "Compare Mutual Fund vs Fixed Deposit"
- "How do I start investing with ₹5000 a month?"
- "What is risk in investing?"

---

## Tech Stack

| Layer | Tool |
|---|---|
| Frontend | Streamlit |
| LLM | Llama 3.1 8B Instant (Groq) |
| Charts | Plotly |
| Config | python-dotenv |

---

## Disclaimer

Mentor is an educational tool, not a SEBI-registered financial advisor. It does not recommend specific investment products. Always consult a qualified financial planner before making investment decisions.
