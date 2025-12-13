# app.py — ARCHITECT AI
# Streamlit Cloud Stable Version

import base64
import streamlit as st
from datetime import datetime

# OSINT imports
from scrape import scrape_multiple
from search import get_search_results
from llm import get_llm, refine_query, filter_results, generate_summary
from llm_utils import get_model_choices

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="ARCHITECT AI",
    page_icon="assets/icon.ico",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- BACKGROUND + STYLE ----------------
def set_bg():
    with open("assets/backsplash.png", "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("data:image/png;base64,{encoded}") no-repeat center fixed;
            background-size: cover;
        }}
        .block-container {{
            background: rgba(5,5,5,0.93);
            border-radius: 18px;
            padding: 2rem;
        }}
        h1, h2, h3 {{
            color: #ff004c;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

set_bg()

# ---------------- HEADER ----------------
_, logo_col, _ = st.columns(3)
with logo_col:
    st.image("assets/logo.jpg", width=220)

st.markdown(
    "<h1 style='text-align:center;'>ARCHITECT AI</h1>"
    "<h4 style='text-align:center;color:#999;'>Private Intelligence Platform</h4>",
    unsafe_allow_html=True,
)

st.divider()

# ---------------- SIDEBAR ----------------
st.sidebar.title("ARCHITECT AI")
mode = st.sidebar.radio(
    "Mode",
    ["🕵️ OSINT Investigation", "💬 Private Chat"],
)

st.sidebar.divider()

# ---------------- CHAT MODE ----------------
SYSTEM_PROMPT = """
You are ARCHITECT AI — a private intelligence and analysis system.
Be concise, professional, and results-focused.
"""

if mode == "💬 Private Chat":

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Message ARCHITECT AI…"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(st.session_state.messages)

        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                llm = get_llm("llama3.1")
                response = llm.invoke(messages)
                answer = response.content

            st.markdown(answer)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

# ---------------- OSINT MODE ----------------
if mode == "🕵️ OSINT Investigation":

    st.subheader("🕵️ OSINT Investigation")

    model_options = get_model_choices()
    model = st.sidebar.selectbox("LLM Model", model_options)
    threads = st.sidebar.slider("Scraping Threads", 1, 12, 4)

    with st.form("search_form"):  # 🚫 NO clear_on_submit
        query = st.text_input(
            "Investigation Query",
            placeholder="e.g. leaked credentials marketplace",
        )
        run = st.form_submit_button("Run Investigation")

    status = st.empty()
    col1, col2, col3 = st.columns(3)
    c1, c2, c3 = col1.empty(), col2.empty(), col3.empty()
    summary_holder = st.empty()

    if run and query:

        for k in ["refined", "results", "filtered", "scraped", "summary"]:
            st.session_state.pop(k, None)

        with status.spinner("Loading LLM…"):
            llm = get_llm(model)

        with status.spinner("Refining query…"):
            st.session_state.refined = refine_query(llm, query)
        c1.container(border=True).markdown(
            f"**Refined Query**\n\n{st.session_state.refined}"
        )

        with status.spinner("Searching sources…"):
            st.session_state.results = get_search_results(
                st.session_state.refined.replace(" ", "+"),
                max_workers=threads,
            )
        c2.container(border=True).markdown(
            f"**Results Found**\n\n{len(st.session_state.results)}"
        )

        with status.spinner("Filtering results…"):
            st.session_state.filtered = filter_results(
                llm,
                st.session_state.refined,
                st.session_state.results,
            )
        c3.container(border=True).markdown(
            f"**Filtered Results**\n\n{len(st.session_state.filtered)}"
        )

        with status.spinner("Scraping content…"):
            st.session_state.scraped = scrape_multiple(
                st.session_state.filtered,
                max_workers=threads,
            )

        with status.spinner("Generating intelligence summary…"):
            summary = generate_summary(
                llm,
                query,
                st.session_state.scraped,
            )

        with summary_holder.container():
            st.subheader("📄 Intelligence Summary")
            st.markdown(summary)

        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        b64 = base64.b64encode(summary.encode()).decode()
        st.markdown(
            f'<a download="architect_summary_{now}.md" '
            f'href="data:text/markdown;base64,{b64}">📥 Download Report</a>',
            unsafe_allow_html=True,
        )

        status.success("✔ Investigation complete")

# ---------------- FOOTER ----------------
st.markdown(
    "<p style='text-align:center;color:#555;margin-top:60px;'>"
    "© 2025 ARCHITECT AI</p>",
    unsafe_allow_html=True,
)


