import os

NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Tune based on your interests/current investment portfolio
STOCKS_OF_INTEREST = [
    ("VST", "Vistra Corp"),
    ("VRT", "Vertiv Holdings"),
    ("JPM", "JPMorgan Chase"),
    ("GS", "Goldman Sachs"),
    ("TSLA", "Tesla"),
    ("NVDA", "NVIDIA"),
]

# Query string for stock/equity news searches 
STOCKS_OF_INTEREST_QUERY = " OR ".join([f"{ticker} OR {name}" for ticker, name in STOCKS_OF_INTEREST])

# Query string for stock/equity news searches 
DEFAULT_NEWS = (
    "stocks OR stock market OR equities OR indexes OR global markets OR macro OR "
    "GDP OR inflation OR CPI OR jobs report OR unemployment OR earnings OR "
    "interest rates OR Fed OR recession OR volatility"
)

# join default query and stocks of interest query (used in fetch_news)
DEFAULT_NEWS_QUERY = DEFAULT_NEWS + " OR " + STOCKS_OF_INTEREST_QUERY

# Keyword scoring for stock/equity relevance
KEYWORDS = {
    # Indexes / benchmarks
    "s&p": 5,          # shorthand for S&P 500, broad U.S. large-cap benchmark
    "s&p 500": 5,      # 500 large U.S. companies; common market barometer
    "nasdaq": 5,       # tech-heavy Nasdaq Composite index
    "dow jones": 5,    # Dow Jones Industrial Average, 30 large blue chips
    "russell 2000": 4, # small-cap U.S. index

    # General companies / tickers of interest
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

# Exclude non-news/dev chatter (keep lowercase; substring checks)
EXCLUDE_KEYWORDS = [
    # package/release noise
    "pypi",
    "biztoc",
    "pip",
    "npm",
    "release notes",
    "changelog",
    "library",
    "llcuda",
    "framework",
    # repos and code snippets
    "github",
    "gitlab",
    "bitbucket",
    "repository",
    "source code",
    "code sample",
    "open source",
    # how-tos and q&a
    "tutorial",
    "how to",
    "walkthrough",
    "guide",
    "stack overflow",
    # devops/tooling updates
    "docker",
    "kubernetes",
    "terraform",
    "aws",
    "azure",
    "gcp",
    # politics (typically not investment-useful for this digest)
    "trump",
    "biden",
    "kamala",
    "election",
    "campaign",
    "republican",
    "democrat",
    "congress",
    "senate",
    "house",
    "mamdani",
    # misc low-signal
    "project",
    "listing"
]
