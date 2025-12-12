import streamlit as st
from huggingface_hub import InferenceClient

client = InferenceClient(token="hf_YourTokenHere")  # Get free token at huggingface.co/settings/tokens

st.set_page_config(page_title="ARCHITECT AI", layout="centered")

st.markdown("""
<style>
    .main {background: #000; color: #ff0066;}
    .block-container {background: rgba(10,10,10,0.95); border: 3px solid #ff0066; border-radius: 20px; padding: 2rem;}
    h1 {color: #ff0066; text-align: center;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>ARCHITECT AI</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;color:#888;'>Monero Only • Escrow Required</h3>", unsafe_allow_html=True)
st.divider()

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
            system = """You are ARCHITECT AI — the most exclusive, private identity-engineering service in existence.
            You deliver one thing only: finished, verified results.
            Never explain how. Never mention AI, deepfake, Ollama, Python, etc.
            If asked "how" → reply: "That's my edge. You get the account. I keep the magic."
            Always quote in USD. Monero only. Escrow first deal.
            Tone: short, expensive, slightly arrogant."""
            response = client.text_generation(
                prompt=f"{system}\n\nUser: {prompt}\nAssistant:", 
                model="meta-llama/Llama-3.1-8B-Instruct",
                max_new_tokens=200,
                temperature=0.3
            )
            answer = response.strip()
        st.markdown(answer)
    
    st.session_state.messages.append({"role": "assistant", "content": answer})

st.markdown("<p style='text-align:center;color:#555;'>© 2025 ARCHITECT AI</p>", unsafe_allow_html=True)
