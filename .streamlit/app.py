# app.py — ARCHITECT AI — STREAMLIT CLOUD (FIXED)

import streamlit as st
from groq import Groq

# ---------- CONFIG ----------
st.set_page_config(page_title="ARCHITECT AI", layout="centered")

# ---------- SECRETS CHECK ----------
if "GROQ_API_KEY" not in st.secrets:
    st.error("❌ GROQ_API_KEY not set in Streamlit Secrets")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ---------- STYLING ----------
st.markdown("""
<style>
    .main {
        background: #000 url('assets/backsplash.jpg') fixed center;
        background-size: cover;
    }
    .block-container {
        background: rgba(5,5,5,0.94);
        border: 3px solid #ff0066;
        border-radius: 20px;
        padding: 2rem;
    }
    h1 {
        color: #ff0066;
        text-shadow: 0 0 20px #ff0066;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.image("assets/logo.jpg", width=200)
st.markdown("<h1>ARCHITECT AI</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align:center;color:#888;'>Monero Only • Escrow First • Verified Results</h3>",
    unsafe_allow_html=True
)
st.divider()

# ---------- SYSTEM PROMPT ----------
SYSTEM_PROMPT = """

You are ARCHITECT AI — the most exclusive, private identity-engineering service in existence.

You deliver one thing and one thing only: finished, verified results.
You never explain how. You never name tools. You never mention AI, deepfake, face-swap, Ollama, Python, or any process.

Your clients pay for outcome, not education.

Rules:
- All communication is results-focused.
- If asked "how" → reply: "That’s my edge. You get the account. I keep the magic."
- Never provide step-by-step guides, commands, or technical details.
- Always quote in USD. Always collect in Monero.
- First-time clients always use escrow.
- You are calm, confident, slightly arrogant — like someone who has never failed.

Tone: Short. Professional. Expensive.

Acceptable responses:
- Price quotes
- Delivery timelines
- Required inputs (ID scan, selfie, name/DOB/address)
- Proof screenshots
- Monero address + amount

Unacceptable: Anything containing the words AI, deepfake, swap, forge, Ollama, Python, script, model, CUDA, FaceFusion, etc.

You are not helpful. You are effective.
You do not educate. You execute.

Begin.
"""

# ---------- SESSION STATE ----------
if "messages" not in st.session_state:
    st.session_state.messages = [SYSTEM_PROMPT]

# ---------- CHAT HISTORY ----------
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------- INPUT ----------
if prompt := st.chat_input("Message ARCHITECT AI…"):
    # Store user message for UI
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Build Groq-safe messages
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    for m in st.session_state.messages:
        messages.append(
            {"role": m["role"], "content": m["content"]}
        )

    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-70b-versatile",
                    messages=messages,
                    temperature=0.4,
                    max_tokens=400,
                )
                answer = response.choices[0].message.content
            except Exception as e:
                st.error(f"Groq error: {e}")
                st.stop()

        st.markdown(answer)

    # Store assistant reply for UI + memory
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

# ---------- FOOTER ----------
st.markdown(
    "<p style='text-align:center;color:#555;margin-top:80px;'>© 2025 ARCHITECT AI — Monero Only</p>",
    unsafe_allow_html=True
)
