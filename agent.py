from langchain.agents import initialize_agent, Tool
from langchain.tools import tool
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentType

from services.news_service import fetch_latest_news, summarize_news_for_linkedin
from services.linkedin_service import post_to_linkedin
from services.llm_service import get_llm


@tool
def fetch_and_summarize_news(topic: str) -> str:
    """
    Fetches the latest news on a given topic and summarizes them into a single LinkedIn post string.
    """
    news_list = fetch_latest_news(topic=topic)
    return summarize_news_for_linkedin(news_list)


@tool
def post_summarized_news(topic: str) -> str:
    """
    Fetches the latest news, summarizes them, and posts to LinkedIn in a single step.
    Returns LinkedIn's API response message.
    """
    summarized_content = fetch_and_summarize_news(topic)
    response = post_to_linkedin(summarized_content)
    return str(response)


def create_news_posting_agent():
    """
    Creates and returns a zero-shot agent with memory and the tools for
    news fetching/summarizing and LinkedIn posting.
    """
    tools = [fetch_and_summarize_news, post_summarized_news]
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    llm = get_llm()

    news_posting_agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True
    )
    return news_posting_agent
