import os

NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Query string for stock/equity news searches (used in fetch_news)
DEFAULT_NEWS_QUERY = "stock market OR equities OR stocks OR S&P 500 OR Dow Jones OR Nasdaq"

# Keyword scoring for stock/equity relevance
KEYWORDS = {
    # Indexes / benchmarks
    "s&p": 5,
    "s&p 500": 5,
    "nasdaq": 5,
    "dow jones": 5,
    "russell 2000": 4,

    # Companies / tickers of interest
    "apple": 4,
    "microsoft": 4,
    "amazon": 4,
    "google": 4,
    "alphabet": 4,
    "meta": 4,
    "nvidia": 5,
    "tesla": 4,
    "netflix": 3,
    "broadcom": 3,
    "amd": 3,
    "intel": 3,
    "qualcomm": 3,
    "salesforce": 3,
    "adobe": 3,
    "oracle": 3,

    # Sectors / themes
    "semiconductor": 4,
    "chip": 3,
    "ai": 3,
    "cloud": 3,
    "cybersecurity": 3,
    "renewable": 2,
    "energy": 2,
    "oil": 2,
    "bank": 2,
    "financial": 2,
    "biotech": 3,

    # Market actions
    "earnings": 4,
    "guidance": 3,
    "upgrade": 3,
    "downgrade": 3,
    "dividend": 2,
    "buyback": 3,
    "ipo": 3,
    "m&a": 3,
    "acquisition": 3,
    "merger": 3,
    "spinoff": 2,
    "sec": 2,
}

# Source weighting stays generic; adjust as needed
SOURCE_WEIGHTS = {
    "Reuters": 5,
    "Bloomberg": 5,
    "Financial Times": 5,
    "The Wall Street Journal": 4,
    "The New York Times": 4,
    "Barron's": 4,
    "CNBC": 3,
    "MarketWatch": 3,
    "Yahoo Finance": 3,
    "Investing.com": 3,
    "Investor's Business Daily": 3,
    "Seeking Alpha": 3,
    "The Motley Fool": 2,
    "Forbes": 2,
    "Fortune": 2,
    "Business Insider": 2,
    "Morningstar": 3,
    "The Economist": 3,
    "Bloomberg Opinion": 3,
}
