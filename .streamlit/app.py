# app.py — ARCHITECT AI
# OSINT Investigation + Chat Interface
# Streamlit Cloud compatible

import base64
import streamlit as st
from datetime import datetime

from scrape import scrape_multiple
from search import get_search_results
from llm import get_llm, refine_query, filter_results, generate_summary
from llm_utils import BufferedStreamingHandler, get_model_choices

# ===============================
# Streamlit Page Config
# ===============================
st.set_page_config(
    page_title="ARCHITECT AI",
    page_icon="assets/icon.ico",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ===============================
# Global Background + Styling
# ===============================
st.markdown(
    """
    <style>
        .main {
            background: url("assets/backsplash.png") no-repeat center center fixed;
            background-size: cover;
        }

        .block-container {
            background: rgba(5, 5, 5, 0.92);
            border-radius: 18px;
            padding: 2rem;
        }

        .colHeight {
            max-height: 40vh;
            overflow-y: auto;
            text-align: center;
        }

        .pTitle {
            font-weight: bold;
            color: #ff0066;
            margin-bottom: 0.5em;
        }

        .aStyle {
            font-size: 18px;
            font-weight: bold;
            padding: 5px;
            text-align: center;
        }

        h1, h2, h3 {
            color: #ff0066;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ===============================
# Centered Logo Header
# ===============================
_, logo_col, _ = st.columns(3)
with logo_col:
    st.image("assets/logo.jpg", width=240)

st.markdown(
    "<h1 style='text-align:center;'>ARCHITECT AI</h1>",
    unsafe_allow_html=True,
)

st.markdown(
    "<p style='text-align:center;color:#888;'>Private Intelligence & Analysis</p>",
    unsafe_allow_html=True,
)

st.divider()

# ===============================
# Sidebar
# ===============================
st.sidebar.title("ARCHITECT AI")
st.sidebar.caption("Private Intelligence Platform")

mode = st.sidebar.radio(
    "Select Mode",
    ["OSINT Investigation", "Chat"],
    index=0,
)

st.sidebar.divider()

# ===============================
# SHARED STATE
# ===============================
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# ===============================
# MODE: CHAT
# ===============================
if mode == "Chat":
    st.markdown("## 💬 Secure Chat")

    SYSTEM_PROMPT = (
        "You are ARCHITECT AI. "
        "You provide precise, confident, professional responses. "
        "Clear. Direct. Efficient."
    )

    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Message ARCHITECT AI…"):
        st.session_state.chat_messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(st.session_state.chat_messages)

        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                llm = get_llm("llama3.1")
                response = llm.invoke(messages)
                answer = response.content

            st.markdown(answer)

        st.session_state.chat_messages.append(
            {"role": "assistant", "content": answer}
        )

# ===============================
# MODE: OSINT INVESTIGATION
# ===============================
else:
    st.markdown("## 🕵️ OSINT Investigation")

    # Sidebar controls
    st.sidebar.subheader("OSINT Settings")

    model_options = get_model_choices()
    model = st.sidebar.selectbox(
        "Select LLM Model",
        model_options,
        index=0,
    )

    threads = st.sidebar.slider(
        "Scraping Threads",
        1,
        16,
        4,
    )

    # Search Form (with submit button)
    with st.form("search_form", clear_on_submit=True):
        col_input, col_button = st.columns([10, 1])

        query = col_input.text_input(
            "Enter Search Query",
            placeholder="Enter investigation query",
            label_visibility="collapsed",
        )

        run_button = col_button.form_submit_button("Run")

    status_slot = st.empty()
    cols = st.columns(3)
    p1, p2, p3 = [col.empty() for col in cols]
    summary_container = st.empty()

    if run_button and query:
        for k in ["refined", "results", "filtered", "scraped", "streamed_summary"]:
            st.session_state.pop(k, None)

        with status_slot.container():
            with st.spinner("Loading model…"):
                llm = get_llm(model)

        with status_slot.container():
            with st.spinner("Refining query…"):
                st.session_state.refined = refine_query(llm, query)

        p1.container(border=True).markdown(
            f"<div class='colHeight'><p class='pTitle'>Refined Query</p>"
            f"<p>{st.session_state.refined}</p></div>",
            unsafe_allow_html=True,
        )

        with status_slot.container():
            with st.spinner("Searching sources…"):
                st.session_state.results = get_search_results(
                    st.session_state.refined.replace(" ", "+"),
                    max_workers=threads,
                )

        p2.container(border=True).markdown(
            f"<div class='colHeight'><p class='pTitle'>Search Results</p>"
            f"<p>{len(st.session_state.results)}</p></div>",
            unsafe_allow_html=True,
        )

        with status_slot.container():
            with st.spinner("Filtering results…"):
                st.session_state.filtered = filter_results(
                    llm,
                    st.session_state.refined,
                    st.session_state.results,
                )

        p3.container(border=True).markdown(
            f"<div class='colHeight'><p class='pTitle'>Filtered Results</p>"
            f"<p>{len(st.session_state.filtered)}</p></div>",
            unsafe_allow_html=True,
        )

        with status_slot.container():
            with st.spinner("Scraping content…"):
                st.session_state.scraped = scrape_multiple(
                    st.session_state.filtered,
                    max_workers=threads,
                )

        st.session_state.streamed_summary = ""

        def ui_emit(chunk: str):
            st.session_state.streamed_summary += chunk
            summary_slot.markdown(st.session_state.streamed_summary)

        with summary_container.container():
            hdr_col, btn_col = st.columns([4, 1])
            with hdr_col:
                st.subheader("Investigation Summary", divider="gray")
            summary_slot = st.empty()

        with status_slot.container():
            with st.spinner("Generating summary…"):
                handler = BufferedStreamingHandler(ui_callback=ui_emit)
                llm.callbacks = [handler]
                generate_summary(llm, query, st.session_state.scraped)

        with btn_col:
            now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            fname = f"architect_ai_summary_{now}.md"
            b64 = base64.b64encode(
                st.session_state.streamed_summary.encode()
            ).decode()
            href = (
                f'<div class="aStyle">📥 '
                f'<a href="data:file/markdown;base64,{b64}" '
                f'download="{fname}">Download</a></div>'
            )
            st.markdown(href, unsafe_allow_html=True)

        status_slot.success("✔️ Investigation completed")

# ===============================
# Footer
# ===============================
st.markdown(
    "<p style='text-align:center;color:#555;margin-top:80px;'>"
    "© 2025 ARCHITECT AI</p>",
    unsafe_allow_html=True,
)

