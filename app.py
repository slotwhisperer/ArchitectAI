import streamlit as st
import ollama

# ==================== PAGE CONFIG ====================
st.set_page_config(page_title="ARCHITECT AI", page_icon="https://i.imgur.com/8X5c1aS.png", layout="centered")

# ==================== STYLE ====================
st.markdown("""
<style>
    .main {background: #000; color: #ff0066;}
    .block-container {background: rgba(10,10,10,0.95); border: 3px solid #ff0066; border-radius: 20px; padding: 2rem;}
    h1 {color: #ff0066; text-shadow: 0 0 20px #ff0066; text-align: center;}
    .stChatMessage {background: #111; border: 1px solid #ff0066; border-radius: 10px; padding: 10px;}
</style>
""", unsafe_allow_html=True)

# ==================== HEADER (hosted images) ====================
st.image("https://i.imgur.com/8X5c1aS.png", width=180)  # your logo hosted online
st.markdown("<h1>ARCHITECT AI</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;color:#888;'>Verified Results Only • Monero Only • Escrow Required</h3>", unsafe_allow_html=True)
st.divider()

# ==================== CHAT ====================
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

# ==================== FOOTER ====================
st.markdown("<p style='text-align:center;color:#555;margin-top:50px;'>© 2025 ARCHITECT AI — Monero Only</p>", unsafe_allow_html=True)
