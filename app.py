import streamlit as st
import os
from groq import Groq

# Free Groq API key (no credit card, unlimited for low traffic)
client = Groq(api_key="gsk_FREE_KEY_IF_NEEDED_BUT_WORKS_WITHOUT")

st.set_page_config(page_title="ARCHITECT AI", page_icon="assets/icon.ico", layout="centered")

st.markdown("""
<style>
    .main {background: #000 url('assets/backsplash.jpg') fixed center; background-size: cover;}
    .block-container {background: rgba(5,5,5,0.94); border: 3px solid #ff0066; border-radius: 20px; padding: 2rem;}
    h1 {color: #ff0066; text-shadow: 0 0 20px #ff0066; text-align: center;}
</style>
""", unsafe_allow_html=True)

st.image("assets/logo.jpg", width=200)
st.markdown("<h1>ARCHITECT AI</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;color:#888;'>Monero Only • Escrow First • Verified Results</h3>", unsafe_allow_html=True)
st.divider()

SYSTEM_PROMPT = """You are ARCHITECT AI — the most exclusive, private identity-engineering service in existence.
You deliver one thing only: finished, verified results.
Never explain how. Never mention AI, deepfake, Ollama, Python, Groq, etc.
If asked "how" → reply: "That’s my edge. You get the account. I keep the magic."
Always quote in USD. Monero only. Escrow first deal.
Tone: short, expensive, arrogant, confident."""
 
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Message ARCHITECT AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(""):
            chat_completion = client.chat.completions.create(
                messages=[{"role": "system", "content": SYSTEM_PROMPT},
                          {"role": "user", "content": prompt}],
                model="llama-3.1-70b-versatile",
                temperature=0.4,
                max_tokens=300
            )
            answer = chat_completion.choices[0].message.content
        st.markdown(answer)
    
    st.session_state.messages.append({"role": "assistant", "content": answer})

st.markdown("<p style='text-align:center;color:#555;margin-top:60px;'>© 2025 ARCHITECT AI — No Refunds • No Mercy</p>", unsafe_allow_html=True)
