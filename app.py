import streamlit as st

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

# Fake responses (replace with real Ollama when you go cloud)
FAKE_RESPONSES = {
    "binance": "$5,000 USD. 5–7 days. Send selfie + ID scan. Monero escrow.",
    "coinbase": "$6,500 USD. 7 days. Full KYC required.",
    "paypal": "$4,200 USD. 3–5 days. Verified account only.",
    "cashapp": "$3,800 USD. 48 hours. Escrow required.",
    "default": "Quote sent via encrypted channel. Monero only."
}

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Message ARCHITECT AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Fake instant reply (replace later with real Ollama)
    lower = prompt.lower()
    response = "Quote sent via encrypted channel. Monero only."
    if "binance" in lower: response = FAKE_RESPONSES["binance"]
    elif "coinbase" in lower: response = FAKE_RESPONSES["coinbase"]
    elif "paypal" in lower: response = FAKE_RESPONSES["paypal"]
    elif "cashapp" in lower: response = FAKE_RESPONSES["cashapp"]

    with st.chat_message("assistant"):
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
