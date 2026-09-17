import streamlit as st
from research_manager import run_research_pipeline

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="ResearchAI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CLEAN & SOLID CSS
# ============================================================
st.markdown("""
<style>
/* إعدادات الخلفية والنصوص */
.stApp {
    background-color: #09090B;
    color: #F4F4F5;
}

.block-container {
    max-width: 950px;
    padding-top: 2rem;
}

/* الهيدر العلوي */
.top-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #27272A;
    padding-bottom: 1rem;
    margin-bottom: 3rem;
    padding-top: 3rem;
}

.brand {
    font-size: 1.4rem;
    font-weight: 700;
    color: #FFFFFF;
}

.brand span {
    color: #6366F1;
}

.badge {
    background-color: #18181B;
    border: 1px solid #27272A;
    padding: 0.4rem 1rem;
    border-radius: 50px;
    font-size: 0.85rem;
    color: #A1A1AA;
}

/* (Hero) */
.hero {
    text-align: center;
    margin-bottom: 3rem;
}

.hero h1 {
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
    color: #FFFFFF;
}

.hero p {
    font-size: 1.1rem;
    color: #A1A1AA;
}

/* (Agents) Grid */
.agents-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 3rem;
}

.agent-card {
    background-color: #18181B;
    border: 1px solid #27272A;
    border-radius: 12px;
    padding: 1.5rem;
}

.agent-card:hover {
    border-color: #6366F1;
}

.agent-icon {
    font-size: 1.8rem;
    margin-bottom: 0.8rem;
}

.agent-title {
    font-size: 1.05rem;
    font-weight: 600;
    color: #FFFFFF;
    margin-bottom: 0.4rem;
}

.agent-desc {
    font-size: 0.85rem;
    color: #A1A1AA;
    line-height: 1.4;
}

/* تخصيص مدخلات Streamlit */
div[data-baseweb="textarea"] > div {
    background-color: #18181B !important;
    border: 1px solid #27272A !important;
    border-radius: 8px;
}

div[data-baseweb="textarea"] > div:focus-within {
    border-color: #6366F1 !important;
}

textarea {
    color: #FFFFFF !important;
}

/* Button Styling */
.stButton > button {
    background: linear-gradient(135deg, #a855f7 0%, #6366f1 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 14px !important;
    height: 50px !important;
    padding: 0 36px !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    letter-spacing: 0.3px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 8px 25px rgba(168, 85, 247, 0.3) !important;
    width: 100% !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 30px rgba(168, 85, 247, 0.5) !important;
}

/* صندوق النتائج */
.result-box {
    background-color: #18181B;
    border: 1px solid #27272A;
    border-radius: 12px;
    padding: 2rem;
    margin-top: 1rem;
    color: #E4E4E7;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div class="top-header">
    <div class="brand"><span>✦</span> ResearchAI</div>
    <div class="badge">● Local AI Model</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# HERO
# ============================================================
st.markdown("""
<div class="hero">
    <h1>Research smarter.</h1>
    <p>A multi-agent AI system that searches, reads, writes, and reviews your research.</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SEARCH
# ============================================================
topic = st.text_area(
    "Research Topic",
    placeholder="Example: Impact of artificial intelligence on the job market in 2026",
    label_visibility="collapsed",
    height=100
)

# توسيط الزر باستخدام الأعمدة
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    start_research = st.button("✦ Start Research")

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# AI TEAM (Grid Layout)
# ============================================================
st.markdown("""
<div class="agents-grid">
    <div class="agent-card">
        <div class="agent-icon">🔎</div>
        <div class="agent-title">Search Agent</div>
        <div class="agent-desc">Finds reliable sources and relevant information.</div>
    </div>
    <div class="agent-card">
        <div class="agent-icon">📖</div>
        <div class="agent-title">Reader Agent</div>
        <div class="agent-desc">Extracts useful content from web pages.</div>
    </div>
    <div class="agent-card">
        <div class="agent-icon">✍️</div>
        <div class="agent-title">Writer Agent</div>
        <div class="agent-desc">Turns gathered data into a structured report.</div>
    </div>
    <div class="agent-card">
        <div class="agent-icon">🧐</div>
        <div class="agent-title">Critic Agent</div>
        <div class="agent-desc">Reviews the report and fixes weaknesses.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# PIPELINE
# ============================================================
if start_research:
    if not topic.strip():
        st.warning("Please enter a research topic.")
    else:
        with st.status("✦ AI Agents are working...", expanded=True) as status:
            state = run_research_pipeline(topic.strip())
            status.update(label="✓ Research completed", state="complete", expanded=False)

        # FINAL REPORT
        st.markdown("### 📝 Final Research Report")
        
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown(state["report"])
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>### 📎 Technical Details", unsafe_allow_html=True)
        
        # DETAILS
        col1, col2 = st.columns(2)
        with col1:
            with st.expander("🔎 Search Results"):
                st.write(state["search_results"])
        with col2:
            with st.expander("🧐 Critic Feedback"):
                st.markdown(state["feedback"])
                
        with st.expander("📖 Scraped Content"):
            st.write(state["scraped_content"])

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div style="text-align: center; color: #71717A; font-size: 0.85rem; margin-top: 4rem; padding-top: 2rem; border-top: 1px solid #27272A;">
    ResearchAI · Built with LangChain & Streamlit
</div>
""", unsafe_allow_html=True)