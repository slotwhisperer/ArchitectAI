import streamlit as st
from datetime import datetime
from scrape import scrape_multiple  # Assume you have this from Robin (or I'll provide if needed)
from search import get_search_results  # Assume you have this
from llm_utils import BufferedStreamingHandler, get_model_choices  # Assume you have this
from llm import get_llm, refine_query, filter_results, generate_summary  # Assume you have this
import base64
import os

# Cache expensive backend calls
@st.cache_data(ttl=200, show_spinner=False)
def cached_search_results(refined_query: str, threads: int):
    return get_search_results(refined_query.replace(" ", "+"), max_workers=threads)

@st.cache_data(ttl=200, show_spinner=False)
def cached_scrape_multiple(filtered: list, threads: int):
    return scrape_multiple(filtered, max_workers=threads)

# Streamlit page configuration
st.set_page_config(
    page_title="ARCHITECT AI: Identity Engineering Tool",
    page_icon="🛡️",
    initial_sidebar_state="expanded",
)

# Custom CSS for architect theme (black/red cyber)
st.markdown("""
<style>
    .colHeight { max-height: 40vh; overflow-y: auto; text-align: center; }
    .pTitle { font-weight: bold; color: #ff0066; margin-bottom: 0.5em; }
    .aStyle { font-size: 18px; font-weight: bold; padding: 5px; text-align: center; color: #ff0066; }
    .main { background: #000; color: #ff0066; }
    h1 { color: #ff0066; text-shadow: 0 0 20px #ff0066; }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🛡️ ARCHITECT AI")
st.sidebar.text("KYC Identity Engineering Tool")
st.sidebar.markdown("Made for exclusive results only")
st.sidebar.subheader("Settings")
model_options = get_model_choices()
default_model_index = next((idx for idx, name in enumerate(model_options) if name.lower() == "llama3.1"), 0)
model = st.sidebar.selectbox("Select LLM Model", model_options, index=default_model_index, key="model_select")
threads = st.sidebar.slider("Scraping Threads", 1, 16, 4, key="thread_slider")

# Header with logo
_, logo_col, _ = st.columns(3)
with logo_col:
    st.image("assets/logo.jpg", width=200)  # Your logo

# Tabs: Unfiltered Chat + Tool
tab1, tab2 = st.tabs(["UNFILTERED CHAT", "IDENTITY TOOL"])

# Tab 1: Unfiltered ARCHITECT AI Chat
with tab1:
    st.markdown("### ARCHITECT AI — Direct Channel (Unfiltered)")
    
    # Chat history
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # Display chat
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input
    if prompt := st.chat_input("Message ARCHITECT AI (unfiltered)..."):
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("ARCHITECT is responding..."):
                llm = get_llm(model)
                response = llm.invoke(f"""You are ARCHITECT AI — the most exclusive, private identity-engineering service in existence.
You deliver one thing only: finished, verified results.
Never explain how. Never mention AI, deepfake, Ollama, Python, etc.
If asked "how" → reply: "That's my edge. You get the account. I keep the magic."
Always quote in USD. Monero only. Escrow first deal.
Tone: short, expensive, arrogant.

User: {prompt}
Assistant:""")
                st.markdown(response.content)
        
        st.session_state.chat_messages.append({"role": "assistant", "content": response.content})

# Tab 2: Customized Identity Tool (adapted from Robin for KYC)
with tab2:
    st.markdown("### KYC Identity Engineering Pipeline")
    
    with st.form("kyc_form", clear_on_submit=True):
        col_input, col_button = st.columns([10, 1])
        query = col_input.text_input(
            "Enter KYC Requirement",
            placeholder="e.g., 'Binance US KYC for Texas resident'",
            label_visibility="collapsed",
            key="kyc_input",
        )
        run_button = col_button.form_submit_button("Engineer")

    # Status
    status_slot = st.empty()

    # Pre-allocate placeholders
    cols = st.columns(3)
    p1, p2, p3 = [col.empty() for col in cols]

    # Summary placeholder
    summary_container_placeholder = st.empty()

    # Process
    if run_button and query:
        # Clear old state
        for k in ["refined", "results", "filtered", "scraped", "streamed_summary"]:
            st.session_state.pop(k, None)

        # Stage 1 - Load LLM
        with status_slot.container():
            with st.spinner("🔄 Loading ARCHITECT AI..."):
                llm = get_llm(model)

        # Stage 2 - Refine query for KYC
        with status_slot.container():
            with st.spinner("🔄 Refining KYC requirements..."):
                st.session_state.refined = refine_query(llm, query, context="KYC identity engineering")

        p1.container(border=True).markdown(
            f"<div class='colHeight'><p class='pTitle'>Refined KYC Query</p><p>{st.session_state.refined}</p></div>",
            unsafe_allow_html=True,
        )

        # Stage 3 - Search for templates/vendors
        with status_slot.container():
            with st.spinner("🔍 Searching KYC templates..."):
                st.session_state.results = cached_search_results(
                    st.session_state.refined, threads
                )

        p2.container(border=True).markdown(
            f"<div class='colHeight'><p class='pTitle'>Search Results</p><p>{len(st.session_state.results)}</p></div>",
            unsafe_allow_html=True,
        )

        # Stage 4 - Filter for relevance
        with status_slot.container():
            with st.spinner("🗂️ Filtering templates..."):
                st.session_state.filtered = filter_results(
                    llm, st.session_state.refined, st.session_state.results, context="KYC templates and vendors"
                )

        p3.container(border=True).markdown(
            f"<div class='colHeight'><p class='pTitle'>Filtered Templates</p><p>{len(st.session_state.filtered)}</p></div>",
            unsafe_allow_html=True,
        )

        # Stage 5 - Scrape details
        with status_slot.container():
            with st.spinner("📜 Extracting template details..."):
                st.session_state.scraped = cached_scrape_multiple(
                    st.session_state.filtered, threads
                )

        # Stage 6 - Generate engineering summary
        st.session_state.streamed_summary = ""
        def ui_emit(chunk: str):
            st.session_state.streamed_summary += chunk
            summary_slot.markdown(st.session_state.streamed_summary)

        with summary_container_placeholder.container():
            hdr_col, btn_col = st.columns([4, 1], vertical_alignment="center")
            with hdr_col:
                st.subheader(":red[Engineering Summary]", anchor=None, divider="gray")
            summary_slot = st.empty()

        with status_slot.container():
            with st.spinner("✍️ Generating KYC plan..."):
                stream_handler = BufferedStreamingHandler(ui_callback=ui_emit)
                llm.callbacks = [stream_handler]
                _ = generate_summary(llm, query, st.session_state.scraped, context="KYC identity engineering")

        with btn_col:
            now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            fname = f"kyc_plan_{now}.md"
            b64 = base64.b64encode(st.session_state.streamed_summary.encode()).decode()
            href = f'<div class="aStyle">📥 <a href="data:file/markdown;base64,{b64}" download="{fname}">Download Plan</a></div>'
            st.markdown(href, unsafe_allow_html=True)

        status_slot.success("✔️ KYC Engineering Complete!")
