# Daily Stock Market Advisor

A small pipeline that pulls fresh stock-market news, scores relevance, asks an LLM for concise recommendations/risks, and emails a digest. It can run locally or on a schedule via GitHub Actions.

## Motivation
- Created to help beginners reduce noise in market news and see a concise daily view of what matters.
- LLM summaries emphasize tickers, rationale, and risks to build investment literacy, not just surface headlines.
- Automated email delivery provides consistent coverage without manual research effort.

## How it works
1) `fetch_news.py` pulls recent stock/equities headlines from NewsAPI using `DEFAULT_NEWS_QUERY`.
2) `rank.py` scores by keywords/source quality to pick the most relevant items.
3) `stocks_api.py` fetches per-ticker snapshots from Financial Modeling Prep for `STOCKS_OF_INTEREST` (price, open/high/low, prev close, volume, change, market cap). One call per ticker avoids multi-symbol billing limits.
4) `market_analysis.py` sends the top articles **and** the fresh stock stats to OpenAI, asking for concise investment recommendations and risks for the portfolio tickers plus any other relevant tickers mentioned in articles or broader market context.
5) `main.py` assembles the digest and `email_digest.py` sends it.
6) `.github/workflows/daily_digest.yml` can run it twice daily via GitHub Actions.

## Requirements
- Python 3.12 (GitHub Actions uses 3.12)
- `pip install -r requirements.txt`
- API keys and email creds set via env vars or GitHub Secrets:
  - `NEWS_API_KEY` (NewsAPI)
  - `OPENAI_API_KEY` (OpenAI)
  - `STOCKS_API_KEY` (Financial Modeling Prep)
  - `EMAIL_USER`, `EMAIL_PASS`, `EMAIL_TO` (SMTP)

## Getting API keys
### NewsAPI key
1) Go to https://newsapi.org/ and sign up.
2) Find your API key in the dashboard.
3) Set `NEWS_API_KEY` as an env var or GitHub secret.

### OpenAI API key
1) Go to https://platform.openai.com/api-keys and create a new secret key.
2) Copy it once; store safely.
3) Set `OPENAI_API_KEY` as an env var or GitHub secret.
4) If a key was ever leaked, rotate it immediately.

### Financial Modeling Prep (FMP) key
1) Go to https://site.financialmodelingprep.com/developer and create an API key.
2) Set `STOCKS_API_KEY` as an env var or GitHub secret.

## Local setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export NEWS_API_KEY="your-newsapi-key"
export OPENAI_API_KEY="your-openai-key"
export STOCKS_API_KEY="your-fmp-key"
export EMAIL_USER="your_email@example.com"
export EMAIL_PASS="your_smtp_app_password"
export EMAIL_TO="recipient@example.com"

python main.py
```

Optional: create a `.env` (kept out of git by `.gitignore`):
```
NEWS_API_KEY=...
OPENAI_API_KEY=...
STOCKS_API_KEY=...
EMAIL_USER=...
EMAIL_PASS=...
EMAIL_TO=...
```

## GitHub Actions (scheduled digest)
The workflow `.github/workflows/daily_digest.yml` runs at 8am and 5pm ET. Add these repository secrets:
- `NEWS_API_KEY`
- `OPENAI_API_KEY`
- `EMAIL_USER`
- `EMAIL_PASS`
- `EMAIL_TO`

## Outputs
- Email subject: `Daily Stock Market Analysis`
- Body: top headlines/links plus the LLM’s concise recommendations and risks.
- Includes stock stat snapshots for the configured portfolio tickers (`STOCKS_OF_INTEREST`) and investment views that combine article signals with the fetched FMP data; also proposes other relevant tickers mentioned in articles or broader market context.

## Notes & tips
- Keep your keys secret; rotate if exposed.
- Tune relevance in `config.py` (`DEFAULT_NEWS_QUERY`, keyword weights, source weights).
- If you hit OpenAI/NewsAPI quotas, reduce frequency or `pageSize` in `fetch_news.py`.
- `STOCKS_OF_INTEREST` in `config.py` controls which tickers get stock stat lookups; one request per ticker is made to avoid multi-symbol billing. Adjust the list to change coverage and API usage.
