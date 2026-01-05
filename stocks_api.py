from config import STOCKS_API_KEY
import requests

def get_stock_data(stocks: list[tuple[str, str]]) -> list[dict]:
    if not STOCKS_API_KEY or not STOCKS_API_KEY.strip():
        raise RuntimeError("STOCKS_API_KEY is missing. Set it in your environment or .env.")

    normalized: list[dict] = []

    # Fetch per-ticker to avoid multi-symbol billing requirements.
    for ticker, _ in stocks:
        try:
            response = requests.get(
                "https://financialmodelingprep.com/stable/quote",
                params={
                    "apikey": STOCKS_API_KEY.strip(),
                    "symbol": ticker,
                },
                timeout=10,
            )
            response.raise_for_status()  # Raise on any non-2xx status.
            raw_data = response.json()

            # API may return a list or a single object; normalize to a list.
            items = raw_data if isinstance(raw_data, list) else [raw_data]

            for item in items:
                normalized.append({
                    "symbol": item.get("symbol"),                    # Ticker symbol
                    "price": item.get("price"),                      # Last traded price
                    "open": item.get("open"),                        # Today's opening price
                    "high": item.get("dayHigh"),                     # Intraday high
                    "low": item.get("dayLow"),                       # Intraday low
                    "previous_close": item.get("previousClose"),     # Prior session close
                    "volume": item.get("volume"),                    # Shares traded today
                    "change": item.get("change"),                    # Price change vs previous close
                    "change_pct": item.get("changePercentage"),      # Percent change vs previous close
                    "market_cap": item.get("marketCap"),             # Market capitalization
                })
        except requests.exceptions.RequestException as e:
            print(f"Error fetching stock data for {ticker}: {e}")
            continue

    return normalized
