# app.py — ARCHITECT AI
# Unified OSINT + Chat UI (Streamlit Cloud Safe)

import base64
import os
import streamlit as st
from datetime import datetime

# -----------------------------
# OSINT imports
# -----------------------------
from scrape import scrape_multiple
from search import get_search_results
from llm_utils import BufferedStreamingHandler, get_model_choices
from llm import get_llm, refine_query, filter_results, generate_summary

# -----------------------------
# Chat (Groq) imports
# -----------------------------
from groq import Groq

# -----------------------------
# Constants
# -----------------------------
CHAT_MODEL = "llama-3.1-8b-instant"

SYSTEM_PROMPT = """You are ARCHITECT AI — a precision reasoning and execution engine.

You communicate clearly, directly, and without fluff.
You provide actionable, structured answers.
You follow all safety, security, and legal guidelines.
"""

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="ARCHITECT AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Styling
# -----------------------------
st.markdown(
    """
    <style>
        .main {
            background: #000;
        }
        .block-container {
            background: rgba(5,5,5,0.94);
            border: 2px solid #ff0066;
            border-radius: 20px;
            padding: 2rem;
        }
        h1, h2, h3 {
            color: #ff0066;
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
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("ARCHITECT AI")
st.sidebar.caption("Private Intelligence & Execution Engine")

mode = st.sidebar.radio(
    "Mode",
    ["Investigation (OSINT)", "Chat"],
    index=0,
)

# -----------------------------
# Header / Logo
# -----------------------------
_, logo_col, _ = st.columns(3)
with logo_col:
    st.image("assets/logo.jpg", width=220)

st.markdown(
    "<h2 style='text-align:center;'>ARCHITECT AI</h2>",
    unsafe_allow_html=True,
)

# =====================================================
# =============== INVESTIGATION MODE ==================
# =====================================================
if mode == "Investigation (OSINT)":

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

    @st.cache_data(ttl=200, show_spinner=False)
    def cached_search_results(refined_query: str, threads: int):
        return get_search_results(refined_query.replace(" ", "+"), max_workers=threads)

    @st.cache_data(ttl=200, show_spinner=False)
    def cached_scrape_multiple(filtered: list, threads: int):
        return scrape_multiple(filtered, max_workers=threads)

    with st.form("search_form", clear_on_submit=True):
        col_input, col_button = st.columns([10, 1])
        query = col_input.text_input(
            "Enter Investigation Query",
            placeholder="Dark web, OSINT, breach, threat intel…",
            label_visibility="collapsed",
        )
        run_button = col_button.form_submit_button("Run")

    status_slot = st.empty()
    cols = st.columns(3)
    p1, p2, p3 = [col.empty() for col in cols]
    summary_container_placeholder = st.empty()

    if run_button and query:

        for k in ["refined", "results", "filtered", "scraped", "streamed_summary"]:
            st.session_state.pop(k, None)

        with status_slot.container():
            with st.spinner("Loading LLM..."):
                llm = get_llm(model)

        with status_slot.container():
            with st.spinner("Refining query..."):
                st.session_state.refined = refine_query(llm, query)

        p1.container(border=True).markdown(
            f"<div class='colHeight'><p class='pTitle'>Refined Query</p>{st.session_state.refined}</div>",
            unsafe_allow_html=True,
        )

        with status_slot.container():
            with st.spinner("Searching sources..."):
                st.session_state.results = cached_search_results(
                    st.session_state.refined, threads
                )

        p2.container(border=True).markdown(
            f"<div class='colHeight'><p class='pTitle'>Results</p>{len(st.session_state.results)}</div>",
            unsafe_allow_html=True,
        )

        with status_slot.container():
            with st.spinner("Filtering results..."):
                st.session_state.filtered = filter_results(
                    llm, st.session_state.refined, st.session_state.results
                )

        p3.container(border=True).markdown(
            f"<div class='colHeight'><p class='pTitle'>Filtered</p>{len(st.session_state.filtered)}</div>",
            unsafe_allow_html=True,
        )

        with status_slot.container():
            with st.spinner("Scraping content..."):
                st.session_state.scraped = cached_scrape_multiple(
                    st.session_state.filtered, threads
                )

        st.session_state.streamed_summary = ""

        def ui_emit(chunk: str):
            st.session_state.streamed_summary += chunk
            summary_slot.markdown(st.session_state.streamed_summary)

        with summary_container_placeholder.container():
            hdr_col, btn_col = st.columns([4, 1])
            with hdr_col:
                st.subheader("Investigation Summary", divider="gray")
            summary_slot = st.empty()

        with status_slot.container():
            with st.spinner("Generating summary..."):
                stream_handler = BufferedStreamingHandler(ui_callback=ui_emit)
                llm.callbacks = [stream_handler]
                generate_summary(llm, query, st.session_state.scraped)

        with btn_col:
            now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            fname = f"architect_summary_{now}.md"
            b64 = base64.b64encode(
                st.session_state.streamed_summary.encode()
            ).decode()
            href = (
                f'<div class="aStyle">'
                f'<a href="data:file/markdown;base64,{b64}" download="{fname}">'
                f'📥 Download</a></div>'
            )
            st.markdown(href, unsafe_allow_html=True)

        status_slot.success("✔ Investigation complete")

# =====================================================
# ==================== CHAT MODE ======================
# =====================================================
else:

    st.subheader("Direct Chat")

    # Initialize Groq client
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Render chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("Message ARCHITECT AI…"):

        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

        for m in st.session_state.messages:
            messages.append(
                {"role": m["role"], "content": m["content"]}
            )

        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                response = client.chat.completions.create(
                    model=CHAT_MODEL,
                    messages=messages,
                    temperature=0.4,
                    max_tokens=400,
                )
                answer = response.choices[0].message.content

            st.markdown(answer)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

# -----------------------------
# Footer
# -----------------------------
st.markdown(
    "<p style='text-align:center;color:#555;margin-top:80px;'>© 2025 ARCHITECT AI</p>",
    unsafe_allow_html=True,
)
