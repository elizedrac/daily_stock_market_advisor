from fetch_news import fetch_articles
from rank import score_article
from email_digest import send_email
from market_analysis import analyze_articles
from config import NEWS_API_KEY, OPENAI_API_KEY

def main():
    if not NEWS_API_KEY:
        raise RuntimeError("NEWS_API_KEY is missing. Set it before running.")
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is missing. Set it before running.")

    articles = fetch_articles()
    ranked = sorted(articles, key=score_article, reverse=True)

    top_articles = ranked[:10]
    # analysis = analyze_articles(top_articles)

    lines = ["Top articles:"]
    for i, article in enumerate(top_articles[:5], 1):
        lines.append(f"{i}. {article['title']}")
        lines.append(article["url"])
        lines.append("")

    # lines.append("LLM analysis:")
    # lines.append(analysis)

    body = "\n".join(lines)

    send_email(
        subject="Daily Stock Market Analysis",
        body=body
    )

if __name__ == "__main__":
    main()

