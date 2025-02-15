import datetime
import requests
from typing import List, Dict
from langchain.prompts import PromptTemplate
from services.llm_service import get_llm
from config import Config

def fetch_latest_news(topic: str = "technology", days_ago: int = 1, num_articles: int = 5) -> List[Dict[str, str]]:
    """
    Fetches the latest news articles given a topic and returns a list of article dictionaries.
    """
    from_date = (datetime.datetime.today() - datetime.timedelta(days=days_ago)).strftime('%Y-%m-%d')
    url = f"https://newsapi.org/v2/everything?q={topic}&from={from_date}&sortBy=popularity&apiKey={Config.NEWS_API_KEY}"
    
    response = requests.get(url)
    news_data = response.json()

    if news_data.get("status") != "ok":
        raise ValueError(f"Error fetching news: {news_data.get('message', 'Unknown error')}")

    articles = news_data.get("articles", [])[:num_articles]
    
    news_list = []
    for article in articles:
        news_list.append({
            "title": article["title"],
            "description": article["description"],
            "url": article["url"],
            "publishedAt": article["publishedAt"]
        })

    return news_list


def summarize_news_for_linkedin(news_list: List[Dict[str, str]], max_chars: int = Config.LINKEDIN_SAFE_LIMIT) -> str:
    """
    Summarizes multiple news articles into a LinkedIn-friendly post under the
    configured character limit. Returns a combined summary as a single string.
    """
    llm = get_llm()
    summaries = []
    
    prompt_template = PromptTemplate.from_template(
        "Summarize this article professionally for a LinkedIn post, under 400 characters:\n{article}"
    )

    for news in news_list:
        full_text = f"Title: {news['title']}\nDescription: {news['description']}"
        prompt = prompt_template.format(article=full_text)
        summary = llm.predict(prompt)
        
        entry = (
            f"🚀 {news['title']}\n"
            f"{summary}\n"
            f"🔗 [Read more]({news['url']})\n"
        )
        summaries.append(entry)

    full_post = "🌍 Latest News Update:\n\n" + "\n".join(summaries) + "\n#News #Technology #AI"

    # Ensure the total post does not exceed the limit
    if len(full_post) > max_chars:
        full_post = full_post[:max_chars] + "\n🔗 [More news on our blog]"

    return full_post
