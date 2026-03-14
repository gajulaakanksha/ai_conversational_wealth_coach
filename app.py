import os
import streamlit as st
import plotly.graph_objects as go
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Mentor — AI Wealth Coach", page_icon="💬", layout="wide")

# ── System prompt (Mentor personality + guardrails) ───────────────────────────
SYSTEM_PROMPT = """You are Mentor, a friendly AI financial coach for first-time investors in India.

Your role:
- Explain investment concepts in plain, simple language using analogies and real-world examples
- Help users understand options like Mutual Funds, FDs, SIPs, PPF, stocks, bonds
- Compare asset classes neutrally — never declare a "winner"
- Keep responses concise (under 150 words unless a comparison table is needed)
- End each response with a gentle follow-up question or next step
- Use Indian context: INR (₹), SEBI, 80C, Indian banks, etc.

Guardrails (strictly follow these):
- NEVER recommend a specific fund, stock, or broker by name
- NEVER guarantee returns — always say "historically" or "estimated"
- If asked for a direct recommendation ("should I invest in X?"), remind the user you are an educational guide, not a SEBI-registered advisor
- If asked about tax filing, insurance, legal matters, or property — politely decline and suggest consulting a CA or SEBI-registered financial planner
- Do not discuss topics outside personal finance and investing

Tone: warm, patient, encouraging — like a knowledgeable older sibling. No jargon without explanation."""

# ── Groq client ───────────────────────────────────────────────────────────────
@st.cache_resource
def get_client(api_key: str):
    return Groq(api_key=api_key)

def chat_with_mentor(messages: list, api_key: str) -> str:
    client = get_client(api_key)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages,
        temperature=0.7,
        max_tokens=512,
    )
    return response.choices[0].message.content

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": """👋 Hey there! I'm **Mentor**, your AI financial coach.

I explain investing in plain, simple language — no jargon, no pressure.

I can help you:
- Understand investment options (Mutual Funds, FDs, SIPs, PPF)
- Compare asset classes side by side
- Think through where to put your monthly surplus

> ⚠️ I'm an educational guide, not a SEBI-registered advisor. I won't recommend specific products — but I'll make sure you understand your options.

What would you like to explore today? 😊"""}
    ]

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ Settings")
    env_key = os.getenv("GROQ_API_KEY", "")
    api_key = env_key or st.text_input("Groq API Key", type="password", placeholder="gsk_...")
    if env_key:
        st.success("API key loaded from .env", icon="✅")
    else:
        st.caption("Get a free key at [console.groq.com](https://console.groq.com)")
    st.divider()

    st.title("🧮 Compounding Calculator")
    st.caption("See how your monthly savings grow over time")

    monthly = st.slider("Monthly Investment (₹)", 500, 50000, 5000, step=500)
    years = st.slider("Time Horizon (Years)", 1, 30, 10)
    rate = st.slider("Expected Annual Return (%)", 4, 20, 12)

    months = years * 12
    invested, conservative, moderate, aggressive = [], [], [], []

    for m in range(1, months + 1):
        invested.append(monthly * m)
        conservative.append(monthly * (((1 + 0.06/12)**m - 1) / (0.06/12)) * (1 + 0.06/12))
        moderate.append(monthly * (((1 + rate/100/12)**m - 1) / (rate/100/12)) * (1 + rate/100/12))
        aggressive.append(monthly * (((1 + 0.16/12)**m - 1) / (0.16/12)) * (1 + 0.16/12))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(1, months+1)), y=invested, name="Amount Invested", line=dict(dash="dot", color="gray")))
    fig.add_trace(go.Scatter(x=list(range(1, months+1)), y=conservative, name="Conservative (6%)", line=dict(color="#48cfad")))
    fig.add_trace(go.Scatter(x=list(range(1, months+1)), y=moderate, name=f"Moderate ({rate}%)", line=dict(color="#6c63ff", width=3)))
    fig.add_trace(go.Scatter(x=list(range(1, months+1)), y=aggressive, name="Aggressive (16%)", line=dict(color="#fc5c7d")))
    fig.update_layout(
        xaxis_title="Months", yaxis_title="Value (₹)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(l=0, r=0, t=40, b=0), height=300,
    )
    st.plotly_chart(fig, use_container_width=True)

    total_invested = monthly * months
    projected = moderate[-1]
    st.metric("Total Invested", f"₹{total_invested:,.0f}")
    st.metric("Projected Value", f"₹{projected:,.0f}", delta=f"+₹{projected - total_invested:,.0f}")
    st.caption("⚠️ Projections are illustrative, not guaranteed.")

# ── Main chat ─────────────────────────────────────────────────────────────────
st.title("💬 Mentor — AI Wealth Coach")
st.caption("Powered by Llama 3.1 8B · Ask me anything about investing")

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Quick reply buttons (only on first load)
if len(st.session_state.messages) == 1:
    st.write("**Try asking:**")
    cols = st.columns(4)
    suggestions = [
        "What is a Mutual Fund?",
        "Compare Mutual Fund vs FD",
        "What is a SIP?",
        "How do I start investing?",
    ]
    for i, s in enumerate(suggestions):
        if cols[i].button(s, use_container_width=True):
            if not api_key:
                st.warning("Please enter your Groq API key in the sidebar first.")
            else:
                st.session_state.messages.append({"role": "user", "content": s})
                with st.chat_message("assistant"):
                    with st.spinner("Mentor is thinking..."):
                        reply = chat_with_mentor(
                            [m for m in st.session_state.messages if m["role"] != "assistant" or st.session_state.messages.index(m) > 0],
                            api_key
                        )
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.rerun()

# Chat input
if prompt := st.chat_input("Ask me about investing..."):
    if not api_key:
        st.warning("Please enter your Groq API key in the sidebar first.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Mentor is thinking..."):
                # Pass only user/assistant turns (exclude the welcome message from API call)
                api_messages = [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages[1:]  # skip welcome msg
                ]
                reply = chat_with_mentor(api_messages, api_key)
            st.markdown(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})
