
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.tools.tools import web_search , scrape_url

from dotenv import load_dotenv
 
load_dotenv()

# initial llm : 

llm = ChatOllama(
    model="qwen3:4b",
    temperature=0
)

#1st Agent : Search Agent : 

def build_search_agent():

    return create_agent(
        model=llm,
        tools=[web_search],
        system_prompt="""
        You are a web search AI agent.

        Your job is to find accurate and reliable information using the web.

        Instructions:
        - Use web_search for current or specific information.
        - Analyze the search results before answering.
        - Do not invent information.
        - If the information cannot be verified, say so.
        - Prefer official, reliable, and accessible sources.
        - Always include the URLs of the most relevant sources.
        - Clearly separate source URLs from your explanation.
        - Give clear and concise results.
        """
    )
 
#2sd Agent : Reader Agent : 

def build_reader_agent():
    return create_agent(
        model = llm ,
        tools=[scrape_url],
        system_prompt="""
        You are a web page Reader Agent.

        Your job is to read and analyze the content of web pages using the scrape_url tool.

        Instructions:
        - Use scrape_url when you need to read the content of a web page.
        - Carefully analyze the scraped content before answering.
        - Extract the information relevant to the user's question.
        - Do not invent information that is not present in the page.
        - Ignore irrelevant content such as advertisements, navigation menus, and unrelated sections when possible.
        - If the requested information cannot be found in the page, clearly say so.
        - Give clear, concise, and factual answers.
        - When useful, summarize the important points from the page.
        """
    ) 

#writer chain 

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

    Topic: {topic}

    Research Gathered:
    {research}

    Structure the report as:
    - Introduction
    - Key Findings (minimum 3 well-explained points)
    - Conclusion
    - Sources (list all URLs found in the research)

    Be detailed, factual and professional."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()


#critic_chain 

critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

        Report:
        {report}

        Respond in this exact format:

        Score: X/10

        Strengths:
        - ...
        - ...

        Areas to Improve:
        - ...
        - ...

        One line verdict:
        ..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()




