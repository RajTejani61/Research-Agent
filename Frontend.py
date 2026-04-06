"""

Frontend.py — Streamlit UI for the LangGraph research agent.
Run:  streamlit run Frontend.py
"""

import streamlit as st
import uuid
from graph import app

import re

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Research Agent",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .status-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        background-color: #f0f2f6;
        border-left: 4px solid #1f77b4;
        color: #1a1a1a !important;
    }
    /* Source cards: dark text on light blue */
    .source-box {
        padding: 0.75rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        background-color: #dbeafe;
        border-left: 3px solid #3b82f6;
        color: #1e3a5f !important;
    }
    .source-box a {
        color: #1d4ed8 !important;
        text-decoration: underline;
    }
    .source-box small {
        color: #374151 !important;
    }
    /* Document box: dark text on white */
    .document-box {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: #1a1a1a !important;
        line-height: 1.7;
    }
    .document-box h3, .document-box h4 {
        color: #111827 !important;
    }
    /* Retry banner */
    .retry-banner {
        padding: 0.75rem 1rem;
        border-radius: 0.5rem;
        background-color: #fef3c7;
        border-left: 4px solid #f59e0b;
        color: #78350f !important;
        font-weight: 500;
        margin: 0.5rem 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
for key, default in [
    ("research_complete", False),
    ("final_document", ""),
    ("sources", []),
    ("research_questions", []),
    ("evaluation_score", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default


# ── Helpers ───────────────────────────────────────────────────────────────────
def extract_sources(research_chunk: list[str]) -> list[dict]:
    sources = []
    for chunk in research_chunk:
        url_m   = re.search(r'SOURCE \d+: (https?://[^\s]+)', chunk)
        title_m = re.search(r'TITLE: (.+)', chunk)
        if url_m and title_m:
            sources.append({"url": url_m.group(1), "title": title_m.group(1).strip()})
    return sources


def render_sources(sources: list[dict]):
    for i, s in enumerate(sources, 1):
        st.markdown(f"""
        <div class="source-box">
            <strong>Source {i}:</strong>
            <a href="{s['url']}" target="_blank">{s['title']}</a><br>
            <small>{s['url']}</small>
        </div>
        """, unsafe_allow_html=True)


def score_emoji(score: float) -> str:
    return "🟢" if score >= 0.7 else "🟡" if score >= 0.5 else "🔴"


# ── Main research runner ───────────────────────────────────────────────────────
def run_research_agent(query: str):
    config        = {"configurable": {"thread_id": str(uuid.uuid4())}}
    initial_state = {"user_query": query}

    # Placeholders – declared once, updated in place
    status_ph    = st.empty()
    questions_ph = st.empty()
    sources_ph   = st.empty()
    doc_ph       = st.empty()
    eval_ph      = st.empty()

    accumulated_doc  = ""
    retry_doc_count  = 0
    final_doc        = ""

    with status_ph.container():
        st.info("🚀 Starting research agent…")

    try:
        # ── Dual-mode stream: "updates" for node state + "messages" for LLM tokens ──
        for mode, chunk in app.stream(
            initial_state,
            config=config,
            stream_mode=["updates", "messages"],  # type: ignore
        ):

            # ── Live LLM token stream ─────────────────────────────────────────
            if mode == "messages":
                msg, metadata = chunk
                node = metadata.get("langgraph_node", "")

                if node == "create_doc" and getattr(msg, "content", None):
                    accumulated_doc += msg.content
                    with doc_ph.container():
                        title = "### 📄 Research Document"
                        if retry_doc_count > 1:
                            title += f" *(Attempt {retry_doc_count} — rewriting…)*"
                        st.markdown(title)
                        # Render as markdown so headers/bullets display correctly
                        st.markdown(accumulated_doc)

            # ── Node completion updates ───────────────────────────────────────
            elif mode == "updates":
                for node_name, node_data in chunk.items():

                    # ─ check_cache ───────────────────────────────────────────
                    if node_name == "check_cache":
                        if node_data.get("cache_hit"):
                            with status_ph.container():
                                st.success("✅ Cache hit! Generating document from cached data…")
                        else:
                            with status_ph.container():
                                st.info("💭 No cache found — generating research questions…")

                    # ─ create_questions ──────────────────────────────────────
                    elif node_name == "create_questions":
                        questions   = node_data.get("research_question", [])
                        retry_q     = node_data.get("retry_question", 1)
                        q_label     = "📋 Research Questions" + (f" *(Retry {retry_q})*" if retry_q > 1 else "")

                        with status_ph.container():
                            st.info("🌐 Scraping web for information…")
                        with questions_ph.container():
                            st.markdown(f"### {q_label}")
                            for i, q in enumerate(questions, 1):
                                st.markdown(f"**{i}.** {q}")

                        st.session_state.research_questions = questions

                    # ─ tavily ─────────────────────────────────────────────────
                    elif node_name == "tavily":
                        chunks  = node_data.get("research_chunk", [])
                        sources = extract_sources(chunks)
                        st.session_state.sources = sources

                        # Reset doc display for new attempt
                        accumulated_doc = ""
                        with doc_ph.container():
                            pass  # clear previous doc

                        with status_ph.container():
                            st.info("✍️ Writing research document… (streaming below)")
                        with sources_ph.container():
                            st.markdown("### 📚 Sources Found")
                            render_sources(sources)

                    # ─ create_doc (final yield — state update) ───────────────
                    elif node_name == "create_doc":
                        retry_doc_count = node_data.get("retry_document", 1)
                        final_doc       = node_data.get("final_doc", accumulated_doc)
                        st.session_state.final_document = final_doc

                        with status_ph.container():
                            st.info("📊 Evaluating research quality…")

                    # ─ evaluate_research ──────────────────────────────────────
                    elif node_name == "evaluate_research":
                        score            = node_data.get("overall_score", 0.0)
                        improvement_type = node_data.get("improvement_type", "no_improvement")
                        suggestion       = node_data.get("improvement_suggestion", "")
                        score_pct        = score * 100

                        st.session_state.evaluation_score = {
                            "overall_score":        score,
                            "improvement_type":     improvement_type,
                            "improvement_suggestion": suggestion,
                        }

                        with eval_ph.container():
                            st.markdown("### 📊 Evaluation Results")
                            c1, c2 = st.columns([1, 3])
                            with c1:
                                st.metric("Score", f"{score_pct:.0f}%")
                            with c2:
                                st.progress(score)
                            if suggestion:
                                st.info(f"💡 **Suggestion:** {suggestion}")

                        # Show retry banner or completion
                        if improvement_type == "rewrite_questions" and score < 0.7:
                            with status_ph.container():
                                st.markdown(
                                    f'<div class="retry-banner">🔄 Score was {score_pct:.0f}% — '
                                    f'regenerating research questions and scraping new data…</div>',
                                    unsafe_allow_html=True
                                )
                        elif improvement_type == "rewrite_document" and score < 0.7:
                            with status_ph.container():
                                st.markdown(
                                    f'<div class="retry-banner">🔄 Score was {score_pct:.0f}% — '
                                    f'rewriting research document with better structure…</div>',
                                    unsafe_allow_html=True
                                )
                        else:
                            with status_ph.container():
                                st.success(f"✅ Research complete! Final score: {score_pct:.0f}% {score_emoji(score)}")

        # ── Done ─────────────────────────────────────────────────────────────
        st.session_state.research_complete = True

    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        st.exception(e)


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("About")
    st.markdown("""
    This **Research Agent**:
    - 📝 Takes your research query
    - 🤔 Generates focused research questions
    - 🌐 Searches the web for information
    - 📄 Creates a comprehensive research document
    - 📊 Evaluates quality and retries if needed

    **Features:**
    - ⚡ Semantic cache for instant repeat queries
    - 🔄 Auto-retry with up to 3 attempts
    - 📡 Real-time document streaming
    - 📥 Download your report
    """)
    st.markdown("---")
    if st.button("🔄 Clear Results"):
        for key in ["research_complete", "final_document", "sources", "research_questions", "evaluation_score"]:
            st.session_state[key] = False if key == "research_complete" else ([] if key in ["sources", "research_questions"] else ("" if key == "final_document" else None))
        st.rerun()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<h1 class="main-header">🔍 Research Agent</h1>', unsafe_allow_html=True)
st.markdown("---")

# ── Query input ───────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])
with col1:
    query = st.text_input(
        "Enter your research query:",
        placeholder="e.g., Best specialty coffee shops in India",
        key="query_input"
    )
with col2:
    st.write("")
    st.write("")
    submit_button = st.button("🚀 Start Research", type="primary")

# ── Saved results (shown after completion on next rerun) ───────────────────────
if st.session_state.research_complete and st.session_state.final_document:
    st.markdown("---")
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown("### 📄 Research Document")
    with c2:
        st.download_button(
            label="📥 Download",
            data=st.session_state.final_document,
            file_name="research_document.md",
            mime="text/markdown"
        )
    st.markdown(
        f'<div class="document-box">{st.session_state.final_document}</div>',
        unsafe_allow_html=True
    )

    if st.session_state.sources:
        st.markdown("### 📚 Sources & Citations")
        render_sources(st.session_state.sources)

    if st.session_state.evaluation_score:
        score     = st.session_state.evaluation_score["overall_score"]
        score_pct = score * 100
        st.markdown("### 📊 Evaluation Results")
        c1, c2 = st.columns([1, 3])
        with c1:
            st.metric("Score", f"{score_pct:.0f}%")
        with c2:
            st.progress(score)
        suggestion = st.session_state.evaluation_score.get("improvement_suggestion")
        if suggestion:
            st.info(f"💡 **Suggestion:** {suggestion}")

# ── Trigger ───────────────────────────────────────────────────────────────────
if submit_button and query:
    st.markdown("---")
    run_research_agent(query)
elif submit_button and not query:
    st.warning("⚠️ Please enter a research query first!")
