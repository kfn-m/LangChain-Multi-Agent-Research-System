import streamlit as st

from research_manager import run_research_pipeline


st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🤖",
    layout="wide"
)


st.title("🤖 AI Research Assistant")

st.write(
    "Multi-Agent Research System"
)


topic = st.text_area(
    "Research Topic",
    placeholder="Example: Impact of AI on the job market in 2026"
)


if st.button(
    "🔍 Start Research",
    type="primary",
    use_container_width=True
):

    if not topic.strip():

        st.warning("Please enter a topic.")

    else:

        with st.spinner(
            "Research system is working..."
        ):

            state = run_research_pipeline(topic)


        st.success(
            "Research completed!"
        )


        # ====================================================
        # SEARCH
        # ====================================================

        with st.expander(
            "🔎 Search Results"
        ):

            st.write(
                state["search_results"]
            )


        # ====================================================
        # READER
        # ====================================================

        with st.expander(
            "📖 Scraped Content"
        ):

            st.write(
                state["scraped_content"]
            )


        # ====================================================
        # REPORT
        # ====================================================

        st.subheader(
            "📝 Final Report"
        )

        st.markdown(
            state["report"]
        )


        # ====================================================
        # CRITIC
        # ====================================================

        st.subheader(
            "🧐 Critic Review"
        )

        st.markdown(
            state["feedback"]
        )