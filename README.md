# WealthMentor AI — Conversational Wealth Coach

WealthMentor AI is a conversational AI system designed to help first-time investors learn about investing through natural language conversations instead of complex dashboards.

The application acts as a friendly AI mentor that explains financial concepts, analyzes user surplus income, and visualizes long-term investment growth.

---

## Problem Statement

For many beginner investors, traditional financial dashboards introduce cognitive overload rather than clarity.

Challenges faced by new investors:

• Too many investment options
• Complex financial terminology
• Confusing graphs and dashboards
• Lack of personalized guidance

Instead of dashboards, beginners prefer asking a mentor simple questions.

This project solves that problem using a conversational AI mentor.

---

## Solution

WealthMentor AI replaces traditional dashboards with a chat-based financial mentor.

Users can:

• Ask investment questions
• Understand financial concepts
• Analyze their monthly surplus
• Visualize how investments grow over time

The system combines LLMs, financial knowledge retrieval, and data visualization to provide a beginner-friendly investment learning experience.

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
git clone https://github.com/gajulaakanksha/mentor-wealth-coach.git
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

# Demo

!https://github.com/gajulaakanksha/ai_conversational_wealth_coach/blob/main/images/Screenshot_1.png

---

Example User Flow

Step 1 — User enters financial details
```
Monthly Income: ₹50,000
Monthly Expenses: ₹40,000
```
Step 2 — System calculates
```
Monthly Surplus = ₹10,000
```
Step 3 — User asks the AI mentor
```
Why should I invest in mutual funds?
```
Step 4 — AI explains investment concepts in simple language.

Step 5 — User visualizes investment growth using the simulator.

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

Future Improvements

Potential enhancements include:

• Goal-based financial planning
• Risk profile analysis
• Portfolio tracking dashboard
• Advanced financial RAG knowledge base
• Multi-language financial education
• AI-generated investment learning paths

---

## Disclaimer

Mentor is an educational tool, not a SEBI-registered financial advisor. It does not recommend specific investment products. Always consult a qualified financial planner before making investment decisions.
