import requests
from config import NEWS_API_KEY, DEFAULT_NEWS_QUERY

def fetch_articles():
    # check if the API key is set
    if not NEWS_API_KEY or not NEWS_API_KEY.strip():
        raise RuntimeError("NEWS_API_KEY is missing. Set it in your environment or .env.")

    # get the API key and set the URL, headers, and parameters
    api_key = NEWS_API_KEY.strip()
    url = "https://newsapi.org/v2/everything"
    headers = {"X-Api-Key": api_key}
    params = {
        "q": DEFAULT_NEWS_QUERY,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 100,
    }

    # get the news articles from the NewsAPI
    try:
        response = requests.get(url, headers=headers, params=params)
        # check if the response is successful
        response.raise_for_status()
        articles = response.json()["articles"]
        return articles
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news articles: {e}")
        return []

