import streamlit as st
from datetime import datetime
import base64
import re
import ollama

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="ARCHITECT AI: Identity Engineering Tool",
    page_icon="🛡️",
    initial_sidebar_state="expanded",
)

# ==================== CUSTOM CSS (ROBIN-STYLE + BLACK/RED) ====================
st.markdown("""
<style>
    .colHeight { max-height: 40vh; overflow-y: auto; text-align: center; }
    .pTitle { font-weight: bold; color: #ff0066; margin-bottom: 0.5em; }
    .aStyle { font-size: 18px; font-weight: bold; padding: 5px; text-align: center; color: #ff0066; }
    .main { background: #000; color: #ff0066; }
    .block-container { background: rgba(10,10,10,0.94); border: 3px solid #ff0066; border-radius: 20px; padding: 2rem; }
    h1 { color: #ff0066; text-shadow: 0 0 20px #ff0066; }
</style>
""", unsafe_allow_html=True)

# ==================== SIDEBAR (ROBIN-STYLE) ====================
st.sidebar.title("🛡️ ARCHITECT AI")
st.sidebar.text("KYC Identity Engineering Tool")
st.sidebar.markdown("Exclusive results only")
st.sidebar.subheader("Settings")
model = st.sidebar.selectbox("LLM Model", ["architect"], index=0)  # Your model only
threads = st.sidebar.slider("Scraping Threads", 1, 16, 4)

# ==================== HEADER ====================
_, logo_col, _ = st.columns(3)
with logo_col:
    st.image("assets/logo.jpg", width=200)
st.markdown("<h1>ARCHITECT AI</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;color:#888;'>Monero Only • Escrow Required</h3>", unsafe_allow_html=True)

# ==================== TABS ====================
tab1, tab2 = st.tabs(["UNFILTERED CHAT", "IDENTITY TOOL"])

# ==================== TAB 1: UNFILTERED CHAT ====================
with tab1:
    st.markdown("### Direct Channel — Unfiltered")

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
            with st.spinner("ARCHITECT is responding..."):
                response = ollama.chat(
                    model=model,
                    messages=[{
                        "role": "system",
                        "content": """You are ARCHITECT AI — the most exclusive, private identity-engineering service.
Never explain how. Never mention AI, deepfake, Ollama, Python, etc.
If asked "how" → reply: "That's my edge. You get the account. I keep the magic."
Always quote in USD. Monero only. Escrow first deal.
Tone: short, expensive, arrogant."""
                    }, {"role": "user", "content": prompt}]
                )
                answer = response['message']['content']
            st.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})

# ==================== TAB 2: IDENTITY TOOL (ROBIN-STYLE) ====================
with tab2:
    st.markdown("### KYC Identity Engineering Pipeline")

    with st.form("identity_form", clear_on_submit=True):
        col_input, col_button = st.columns([10, 1])
        query = col_input.text_input(
            "Enter KYC Requirement",
            placeholder="e.g., 'Binance US KYC for Texas resident'",
            label_visibility="collapsed",
            key="kyc_input",
        )
        run_button = col_button.form_submit_button("ENGINEER")

    # Status slot
    status_slot = st.empty()

    # 3-column cards (Robin-style)
    cols = st.columns(3)
    p1, p2, p3 = [col.empty() for col in cols]

    # Summary placeholder
    summary_container_placeholder = st.empty()

    if run_button and query:
        # Clear old state
        for k in ["refined", "results", "filtered", "scraped", "streamed_summary"]:
            if k in st.session_state:
                del st.session_state[k]

        # Stage 1 - Load LLM
        with status_slot.container():
            with st.spinner("🔄 Loading ARCHITECT AI..."):
                # Use your model
                pass  # No real LLM needed for demo

        # Stage 2 - Refine query
        with status_slot.container():
            with st.spinner("🔄 Refining KYC requirements..."):
                refined = ollama.generate(model=model, prompt=f"Refine this KYC request into a search query (output only the query): {query}")['response']
                st.session_state.refined = refined

        p1.container(border=True).markdown(
            f"<div class='colHeight'><p class='pTitle'>Refined Query</p><p>{st.session_state.refined}</p></div>",
            unsafe_allow_html=True,
        )

        # Stage 3 - Search (fake for demo, replace with real search.py)
        with status_slot.container():
            with st.spinner("🔍 Searching templates & vendors..."):
                st.session_state.results = [
                    {"title": "US DL PSD Template 2025", "link": "http://example.com/dl2025"},
                    {"title": "Binance KYC Service", "link": "http://example.com/binance"},
                    {"title": "Selfie + ID Swap", "link": "http://example.com/swap"}
                ]

        p2.container(border=True).markdown(
            f"<div class='colHeight'><p class='pTitle'>Search Results</p><p>{len(st.session_state.results)}</p></div>",
            unsafe_allow_html=True,
        )

        # Stage 4 - Filter
        with status_slot.container():
            with st.spinner("🗂️ Filtering best sources..."):
                st.session_state.filtered = st.session_state.results[:2]

        p3.container(border=True).markdown(
            f"<div class='colHeight'><p class='pTitle'>Filtered Sources</p><p>{len(st.session_state.filtered)}</p></div>",
            unsafe_allow_html=True,
        )

        # Stage 5 - Scrape (fake for demo)
        with status_slot.container():
            with st.spinner("📜 Extracting details..."):
                st.session_state.scraped = {
                    "http://example.com/dl2025": "High quality US DL template PSD. $250 Monero. Escrow available.",
                    "http://example.com/binance": "Binance US KYC service. 5-7 days delivery."
                }

        # Stage 6 - Summary (your ARCHITECT persona)
        st.session_state.streamed_summary = ""
        def ui_emit(chunk):
            st.session_state.streamed_summary += chunk
            summary_slot.markdown(st.session_state.streamed_summary)

        with summary_container_placeholder.container():
            hdr_col, btn_col = st.columns([4, 1])
            with hdr_col:
                st.subheader("Execution Plan", divider="gray")
            summary_slot = st.empty()

        with status_slot.container():
            with st.spinner("✍️ Generating plan..."):
                # Use your model for smart summary
                response = ollama.generate(
                    model=model,
                    prompt=f"""Create short, expensive execution plan for: {query}
Sources: {st.session_state.scraped}
Output only the plan. Tone: short, arrogant, Monero-only."""
                )
                plan = response['response']
                ui_emit(plan)

        with btn_col:
            now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            fname = f"architect_plan_{now}.md"
            b64 = base64.b64encode(st.session_state.streamed_summary.encode()).decode()
            href = f'<div class="aStyle">📥 <a href="data:file/markdown;base64,{b64}" download="{fname}">Download Plan</a></div>'
            st.markdown(href, unsafe_allow_html=True)

        status_slot.success("✔️ Engineering Complete")

# Footer
st.markdown("<p style='text-align:center;color:#555;margin-top:80px;'>© 2025 ARCHITECT AI — Monero Only</p>", unsafe_allow_html=True)
