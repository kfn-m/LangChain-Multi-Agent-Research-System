import streamlit as st

from src.agents.agents import (
    build_search_agent,
    build_reader_agent,
    critic_chain,
    writer_chain
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #777;
    margin-bottom: 35px;
}

.step-title {
    font-size: 24px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🤖 AI Research Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Multi-Agent Research System</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ About")

    st.write(
        """
        This system uses multiple AI components:

        🔎 **Search Agent**  
        Finds relevant information from the web.

        📖 **Reader Agent**  
        Reads and analyzes web pages.

        📝 **Writer**  
        Generates the research report.

        🧐 **Critic**  
        Reviews the generated report.
        """
    )

    st.divider()

    st.caption("Built with LangChain + Streamlit")


# ============================================================
# USER INPUT
# ============================================================

st.subheader("🔍 Research Topic")

topic = st.text_area(
    "Enter the topic you want to research:",
    placeholder="Example: Impact of AI on the job market in 2026",
    height=100
)


# ============================================================
# START BUTTON
# ============================================================

start_research = st.button(
    "🔍 Start Research",
    type="primary",
    use_container_width=True
)


# ============================================================
# RESEARCH PIPELINE
# ============================================================

if start_research:

    if not topic.strip():

        st.warning("⚠️ Please enter a research topic.")

    else:

        state = {}

        # ====================================================
        # STEP 1 - SEARCH AGENT
        # ====================================================

        with st.status(
            "🔎 Step 1: Search Agent is working...",
            expanded=True
        ) as status:

            search_agent = build_search_agent()

            search_result = search_agent.invoke({
                "messages": [
                    (
                        "user",
                        f"""
                        Find recent, reliable and detailed information about:

                        {topic}

                        Return the most relevant sources and include their URLs.

                        Prefer sources that are publicly accessible.
                        """
                    )
                ]
            })

            state["search_results"] = (
                search_result["messages"][-1].content
            )

            st.markdown("### Search Results")
            st.write(state["search_results"])

            status.update(
                label="✅ Step 1 completed",
                state="complete"
            )


        # ====================================================
        # STEP 2 - READER AGENT
        # ====================================================

        with st.status(
            "📖 Step 2: Reader Agent is scraping resources...",
            expanded=True
        ) as status:

            reader_agent = build_reader_agent()

            reader_result = reader_agent.invoke({
                "messages": [
                    (
                        "user",
                        f"""
                        We are researching the following topic:

                        {topic}

                        Below are the search results:

                        {state["search_results"]}

                        Identify the most relevant accessible URL
                        from the search results and use scrape_url
                        to read its content.

                        Extract information that is directly relevant
                        to the research topic.

                        Do not invent information if scraping fails.
                        """
                    )
                ]
            })

            state["scraped_content"] = (
                reader_result["messages"][-1].content
            )

            st.markdown("### Scraped Content")

            with st.expander(
                "📖 View scraped content",
                expanded=False
            ):
                st.write(state["scraped_content"])

            status.update(
                label="✅ Step 2 completed",
                state="complete"
            )


        # ====================================================
        # STEP 3 - WRITER
        # ====================================================

        with st.status(
            "📝 Step 3: Writer is drafting the report...",
            expanded=True
        ) as status:

            research_combined = (
                f"SEARCH RESULTS:\n"
                f"{state['search_results']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n"
                f"{state['scraped_content']}"
            )

            state["report"] = writer_chain.invoke({
                "topic": topic,
                "research": research_combined
            })

            st.markdown("### Final Report")

            st.markdown(state["report"])

            status.update(
                label="✅ Step 3 completed",
                state="complete"
            )


        # ====================================================
        # STEP 4 - CRITIC
        # ====================================================

        with st.status(
            "🧐 Step 4: Critic is reviewing the report...",
            expanded=True
        ) as status:

            state["feedback"] = critic_chain.invoke({
                "report": state["report"]
            })

            st.markdown("### Critic Review")

            st.markdown(state["feedback"])

            status.update(
                label="✅ Step 4 completed",
                state="complete"
            )


        # ====================================================
        # FINAL MESSAGE
        # ====================================================

        st.success("🎉 Research completed successfully!")