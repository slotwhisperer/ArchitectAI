import streamlit as st
import ollama
import os

ASSETS = "C:\\Architect AI\\assets"

st.set_page_config(page_title="ARCHITECT AI", page_icon=f"{ASSETS}/icon.ico", layout="centered")

st.markdown(f"""
<style>
    .main {{ background: url('file://{ASSETS}/backsplash.jpg') fixed center; background-size: cover; }}
    .block-container {{ background: rgba(5,5,5,0.94); border: 3px solid #ff0066; border-radius: 20px; padding: 2rem; }}
    h1, h2 {{ color: #ff0066; text-shadow: 0 0 20px #ff0066; text-align: center; }}
    .stChatMessage {{ background: #111; border: 1px solid #ff0066; border-radius: 10px; padding: 10px; }}
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,2,1])
with col2: st.image(f"{ASSETS}/logo.jpg", width=200)
st.markdown("<h1>ARCHITECT AI</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;color:#888;'>Monero Only • Escrow First</h3>", unsafe_allow_html=True)
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
            response = ollama.chat(model="architect", messages=[{"role": "user", "content": prompt}])
            answer = response['message']['content']
        st.markdown(answer)
    
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()