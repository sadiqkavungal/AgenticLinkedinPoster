import logging
from agent import create_news_posting_agent

def main():
    """
    Main entry point to run the LinkedIn news posting agent.
    """
    # Configure logger if needed
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
    )
    
    agent = create_news_posting_agent()
    
    # Example usage: prompt the agent to post the latest AI news
    user_query = "Post the latest AI news to LinkedIn."
    response = agent.run(user_query)
    print("Agent Response:\n", response)

if __name__ == "__main__":
    main()
