from datetime import datetime
from config import KEYWORDS, SOURCE_WEIGHTS, STOCKS_OF_INTEREST, EXCLUDE_KEYWORDS

def score_article(article):
    score = 0
    keyword_score = 0
    ticker_hit = False
    # get article title, description, and url
    text = (article["title"] + " " + (article.get("description") or "")).lower()
    url = article["url"]
    source_name = (article.get("source") or {}).get("name")
    source_name_lower = source_name.lower() if source_name else ""

    # score the article based on how relevant it is to the stocks of interest
    for ticker, name in STOCKS_OF_INTEREST:
        if ticker in text or name in text:
            score += 10 # higher weight for stocks of interest (priority)
            ticker_hit = True

    # score the article based on key keywords
    for keyword, weight in KEYWORDS.items():
        if keyword in text:
            score += weight
            keyword_score += weight

    # score the article based on source name/quality
    if source_name:
        score += SOURCE_WEIGHTS.get(source_name, 1)
    else:
        score += 1  # minimal weight if source missing

    # remove non-news articles
    for keyword in EXCLUDE_KEYWORDS:
        if keyword in text or keyword in source_name_lower or keyword in url:
            score = 0

    # drop pieces with no finance signal and no tickers
    if not ticker_hit and keyword_score == 0:
        score = 0

    # score the article based on how recent it is
    published = datetime.fromisoformat(article["publishedAt"].replace("Z", ""))
    hours_old = (datetime.utcnow() - published).total_seconds() / 3600

    if hours_old < 24:
        score += 3
    elif hours_old < 48:
        score += 1

    return score
