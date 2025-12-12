import streamlit as st
import ollama

st.set_page_config(page_title="ARCHITECT AI", page_icon="assets/icon.ico", layout="centered")

st.markdown("""
<style>
    .main {background: url('assets/backsplash.jpg') fixed center; background-size: cover;}
    .block-container {background: rgba(5,5,5,0.94); border: 3px solid #ff0066; border-radius: 20px; padding: 2rem;}
    h1 {color: #ff0066; text-shadow: 0 0 20px #ff0066; text-align: center;}
</style>
""", unsafe_allow_html=True)

st.image("assets/logo.jpg", width=200)
st.markdown("<h1>ARCHITECT AI</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;color:#888;'>Monero Only • Escrow First • Verified Results</h3>", unsafe_allow_html=True)
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
            resp = ollama.chat(model="architect", messages=[{"role": "user", "content": prompt}])
            answer = resp['message']['content']
        st.markdown(answer)
    
    st.session_state.messages.append({"role": "assistant", "content": answer})

st.markdown(f"""
<div style='text-align:center;color:#555;margin-top:60px;'>
    <img src='assets/xmr.png' width='30'/> Monero Only • 
    <img src='assets/lock.png' width='25'/> Escrow First • 
    <img src='assets/skull.png' width='25'/> No Mercy
</div>
""", unsafe_allow_html=True)
