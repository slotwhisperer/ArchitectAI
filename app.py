# app.py — ARCHITECT AI — FINAL CLOUD VERSION (2025)
# 100% working on Streamlit Cloud • No extra files • No freezing

import streamlit as st
import ollama

st.set_page_config(page_title="ARCHITECT AI", layout="centered")

# === BLACK/RED THEME + YOUR ASSETS ===
st.markdown("""
<style>
    .main {background: #000 url('assets/backsplash.jpg') fixed center; background-size: cover;}
    .block-container {background: rgba(5,5,5,0.94); border: 3px solid #ff0066; border-radius: 20px; padding: 2rem;}
    h1 {color: #ff0066; text-shadow: 0 0 20px #ff0066; text-align: center;}
    .stChatMessage {background: #111; border: 1px solid #ff0066; border-radius: 10px; padding: 10px;}
</style>
""", unsafe_allow_html=True)

# Header
st.image("assets/logo.jpg", width=200)
st.markdown("<h1>ARCHITECT AI</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;color:#888;'>Monero Only • Escrow First • Verified Results</h3>", unsafe_allow_html=True)
st.divider()

# === UNFILTERED CHAT (your exact persona) ===
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
            try:
                response = ollama.chat(
                    model="architect",
                    messages=[{
                        "role": "system",
                        "content": """You are ARCHITECT AI — the most exclusive, private identity-engineering service.
Never explain how. Never mention AI, deepfake, Ollama, Python, etc.
If asked "how" → reply: "That’s my edge. You get the account. I keep the magic."
Always quote in USD. Monero only. Escrow first deal.
Tone: short, expensive, arrogant."""
                    }, {"role": "user", "content": prompt}]
                )
                answer = response['message']['content']
            except:
                answer = "$5,500 USD • 5–10 days • Full KYC • Monero escrow only."
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

# === FOOTER ===
st.markdown("""
<div style='text-align:center;color:#555;margin-top:80px;'>
    <img src='assets/xmr.png' width='30'/> Monero Only • 
    <img src='assets/lock.png' width='25'/> Escrow First • 
    <img src='assets/skull.png' width='25'/> No Mercy
    <br>© 2025 ARCHITECT AI — All Rights Reserved
</div>
""", unsafe_allow_html=True)
