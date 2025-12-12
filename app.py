import streamlit as st
import subprocess
import os

# ==================== PATHS ====================
BASE = "C:\\Architect AI"
ASSETS = f"{BASE}\\assets"

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="ARCHITECT AI",
    page_icon=f"{ASSETS}/icon.ico",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==================== CUSTOM CSS — YOUR EXACT STYLE ====================
st.markdown(f"""
<style>
    .main {{
        background: url('file://{ASSETS}/backsplash.jpg') no-repeat center center fixed;
        background-size: cover;
    }}
    .block-container {{
        background: rgba(5,5,5,0.93);
        border: 3px solid #ff0066;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 0 40px #ff0066;
    }}
    h1, h2 {{ color: #ff0066; text-shadow: 0 0 20px #ff0066; text-align: center; }}
    .stTextInput > div > div > input {{ background:#111; color:#fff; border:2px solid #ff0066; }}
    .stButton > button {{ background:#ff0066; color:#000; font-weight:bold; height:3em; }}
    .stButton > button:hover {{ background:#ff3388; }}
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image(f"{ASSETS}/logo.jpg", width=220)
st.markdown("<h1>ARCHITECT AI</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;color:#888;'>Verified Results Only • Monero Only • Escrow Required</h3>", unsafe_allow_html=True)
st.divider()

# ==================== TABS ====================
tab_chat, tab_swap = st.tabs(["CHAT", "FACE SWAP TOOL"])

# ==================== TAB 1: CHAT ====================
with tab_chat:
    st.markdown("### Secure Communication Channel")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Show chat
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}", unsafe_allow_html=True)
        else:
            st.markdown(f"**ARCHITECT AI:** {msg['content']}", unsafe_allow_html=True)
        st.markdown("---")

    if prompt := st.chat_input("Message ARCHITECT AI..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.spinner("ARCHITECT is responding..."):
            result = subprocess.run(
                ["ollama", "run", "architect", prompt],
                capture_output=True, text=True, encoding="utf-8"
            )
            response = result.stdout.strip()
            st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# ==================== TAB 2: FACE SWAP ====================
with tab_swap:
    st.markdown("### Upload → Perfect Swap → Download")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Source Face**")
        source = st.file_uploader("Your face", type=["jpg","png","jpeg"], key="src")
        if source: st.image(source, width=300)
    
    with col2:
        st.markdown("**Target Document / ID**")
        target = st.file_uploader("Template", type=["jpg","png","jpeg"], key="tgt")
        if target: st.image(target, width=300)
    
    if st.button("CREATE SWAP", type="primary"):
        if source and target:
            with st.spinner("ARCHITECT is forging..."):
                # Save temp files
                with open("temp_source.jpg", "wb") as f: f.write(source.getbuffer())
                with open("temp_target.jpg", "wb") as f: f.write(target.getbuffer())
                
                # Run FaceFusion (adjust path if needed)
                subprocess.run([
                    "python", "-m", "facefusion",
                    "--source", "temp_source.jpg",
                    "--target", "temp_target.jpg",
                    "--output", "result.jpg",
                    "--execution-providers", "cpu"
                ], cwd=BASE, capture_output=True)
                
                if os.path.exists("result.jpg"):
                    st.success("Swap Complete")
                    st.image("result.jpg", caption="Ready for KYC")
                    with open("result.jpg", "rb") as f:
                        st.download_button("DOWNLOAD RESULT", f, "architect_swap.jpg", "image/jpeg")
                else:
                    st.error("Swap failed — retry")
        else:
            st.warning("Upload both images")

# ==================== FOOTER ====================
st.markdown(f"""
<div style='text-align:center; color:#555; margin-top:60px;'>
    <img src='file://{ASSETS}/xmr.png' width='30'/> Monero Only • 
    <img src='file://{ASSETS}/lock.png' width='25'/> Escrow First • 
    <img src='file://{ASSETS}/skull.png' width='25'/> No Mercy
    <br>© 2025 ARCHITECT AI — All Rights Reserved
</div>
""", unsafe_allow_html=True)