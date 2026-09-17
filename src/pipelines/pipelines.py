from src.agents.agents import (
    build_search_agent,
    build_reader_agent,
    critic_chain,
    writer_chain
)


def run_research_pipeline(topic):

    state = {}

    # ==========================================
    # STEP 1 - Search Agent
    # ==========================================

    print("\n" + "=" * 50)
    print("STEP 1 - Search Agent is working ...")
    print("=" * 50)

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

    state["search_results"] = search_result["messages"][-1].content

    print("\nSearch Results:\n")
    print(state["search_results"])


    # ==========================================
    # STEP 2 - Reader Agent
    # ==========================================

    print("\n" + "=" * 50)
    print("STEP 2 - Reader Agent is scraping resources ...")
    print("=" * 50)

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

    state["scraped_content"] = reader_result["messages"][-1].content

    print("\nScraped Content:\n")
    print(state["scraped_content"])


    # ==========================================
    # STEP 3 - Writer Chain
    # ==========================================

    print("\n" + "=" * 50)
    print("STEP 3 - Writer is drafting the report ...")
    print("=" * 50)

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

    print("\nFinal Report:\n")
    print(state["report"])


    # ==========================================
    # STEP 4 - Critic Chain
    # ==========================================

    print("\n" + "=" * 50)
    print("STEP 4 - Critic is reviewing the report ...")
    print("=" * 50)

    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    })

    print("\nCritic Report:\n")
    print(state["feedback"])


    return state