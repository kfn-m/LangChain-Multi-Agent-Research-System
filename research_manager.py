import hashlib

from pathlib import Path

from src.agents.agents import (
    build_search_agent,
    build_reader_agent,
    critic_chain,
    writer_chain
)


# ============================================================
# STORAGE
# ============================================================

BASE_DIR = Path("research_data")


def get_topic_folder(topic):

    topic_hash = hashlib.md5(
        topic.strip().lower().encode("utf-8")
    ).hexdigest()

    folder = BASE_DIR / topic_hash

    folder.mkdir(
        parents=True,
        exist_ok=True
    )

    return folder


# ============================================================
# SAVE / LOAD
# ============================================================

def save_result(folder, filename, content):

    path = folder / filename

    path.write_text(
        content,
        encoding="utf-8"
    )


def load_result(folder, filename):

    path = folder / filename

    if path.exists():
        return path.read_text(
            encoding="utf-8"
        )

    return None


# ============================================================
# SEARCH
# ============================================================

def run_search(topic):

    folder = get_topic_folder(topic)

    cached = load_result(
        folder,
        "search.txt"
    )

    if cached:

        print("Using cached search results.")

        return cached


    print("Running Search Agent...")

    search_agent = build_search_agent()

    result = search_agent.invoke({
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

    search_results = result["messages"][-1].content

    save_result(
        folder,
        "search.txt",
        search_results
    )

    return search_results


# ============================================================
# READER
# ============================================================

def run_reader(topic, search_results):

    folder = get_topic_folder(topic)

    cached = load_result(
        folder,
        "scraped.txt"
    )

    if cached:

        print("Using cached scraped content.")

        return cached


    print("Running Reader Agent...")

    reader_agent = build_reader_agent()

    result = reader_agent.invoke({
        "messages": [
            (
                "user",
                f"""
                We are researching the following topic:

                {topic}

                Below are the search results:

                {search_results}

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

    scraped_content = result["messages"][-1].content

    save_result(
        folder,
        "scraped.txt",
        scraped_content
    )

    return scraped_content


# ============================================================
# WRITER
# ============================================================

def run_writer(topic, search_results, scraped_content):

    folder = get_topic_folder(topic)

    cached = load_result(
        folder,
        "report.txt"
    )

    if cached:

        print("Using cached report.")

        return cached


    print("Running Writer...")

    research = (
        f"SEARCH RESULTS:\n"
        f"{search_results}\n\n"
        f"DETAILED SCRAPED CONTENT:\n"
        f"{scraped_content}"
    )

    report = writer_chain.invoke({
        "topic": topic,
        "research": research
    })

    save_result(
        folder,
        "report.txt",
        report
    )

    return report


# ============================================================
# CRITIC
# ============================================================

def run_critic(topic, report):

    folder = get_topic_folder(topic)

    cached = load_result(
        folder,
        "feedback.txt"
    )

    if cached:

        print("Using cached critic feedback.")

        return cached


    print("Running Critic...")

    feedback = critic_chain.invoke({
        "report": report
    })

    save_result(
        folder,
        "feedback.txt",
        feedback
    )

    return feedback


# ============================================================
# COMPLETE PIPELINE
# ============================================================

def run_research_pipeline(topic):

    state = {}

    state["search_results"] = run_search(topic)

    state["scraped_content"] = run_reader(
        topic,
        state["search_results"]
    )

    state["report"] = run_writer(
        topic,
        state["search_results"],
        state["scraped_content"]
    )

    state["feedback"] = run_critic(
        topic,
        state["report"]
    )

    return state