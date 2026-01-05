from typing import List, Dict
import requests
from config import OPENAI_API_KEY, STOCKS_OF_INTEREST
from stocks_api import get_stock_data

def analyze_articles(articles: List[Dict], model: str = "gpt-4o-mini") -> str:
    # check if the API key is set
    if not OPENAI_API_KEY or not OPENAI_API_KEY.strip():
        raise RuntimeError("OPENAI_API_KEY is missing. Set it in your environment or .env.")

    stock_data = get_stock_data(STOCKS_OF_INTEREST)
    
    print("stock_data", stock_data)

    # create the prompt (tune as needed)
    prompt_lines = [
        f"You are an equity analyst. Portfolio: {', '.join([f'{t} ({n})' for t, n in STOCKS_OF_INTEREST])}.",
        "Instructions:",
        "- Use both recent articles and the current stock stats to form views, if provided.",
        "- Quote stock stats exactly as listed below; do not infer or invent numbers. If a value is missing, write 'N/A'.",
        "- For each portfolio ticker mentioned in articles, summarize existing news, price/vol impact, and key risks; cite title/source.",
        "- If stock data is provided for that news article, report it exactly and use it in your analysis.",
        "- For portfolio tickers without articles, base the view on the provided stock stats. Report all stats, analyze, and give investment view.",
        "- Give a 1–2 sentence hold/buy/sell view per portfolio ticker.",
        "- From articles not about portfolio tickers, propose 2 - 5 new tickers with rationale and major risks; if uncertain or insufficient info, say so.",
        "- If an article has nothing investment-useful, note that briefly and instead summarize the article in a couple of sentences and provide a brief view on how this might impact the market and/or future investments.",
        "Format:",
        "Portfolio updates:",
        "Again, for the following bullet points, use the exact stock stats as listed below; do not infer or invent numbers. If a value is missing, write 'N/A'.",
        "- <TICKER>: price=<price>, open=<open>, high=<high>, low=<low>, prev_close=<prev_close>, volume=<volume> (source: <title/source>)",
        "- <TICKER>: <summary>; risks: <...>; investment view: <buy/hold/sell> (source: <title/source>)",
        "Potential investments:",
        "- <TICKER>: <rationale>; risks: <...> (source: <title/source>)",
        "",
        "Stock data snapshot (use even if no articles):",
    ]
    if stock_data:
        for item in stock_data:
            prompt_lines.append(
                f"- {item.get('symbol')}: "
                f"price={item.get('price')}, open={item.get('open')}, high={item.get('high')}, low={item.get('low')}, "
                f"prev_close={item.get('previous_close')}, volume={item.get('volume')}, "
                f"change={item.get('change')}, change_pct={item.get('change_pct')}, market_cap={item.get('market_cap')}"
            )
    else:
        prompt_lines.append("- No stock data available for this ticker.")
    prompt_lines.extend([
        "",
        "Articles:",
    ])
    for article in articles:
        prompt_lines.append(
            f"- {article.get('title')} ({article.get('source', {}).get('name')}): "
            f"{article.get('description') or ''} {article.get('url')}"
        )
    if not articles:
        prompt_lines.append("- No articles provided for analysis.")

    # create the payload (request body)
    payload = {
        "model": model,
        "input": [
            {
                "role": "system",
                "content": "Be concise, evidence-based, and include key risks."
            },
            {
                "role": "user",
                "content": "\n".join(prompt_lines)
            }
        ],
        "temperature": 0.2,
    }

    # create the headers (authorization and content type)
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY.strip()}",
        "Content-Type": "application/json",
    }

    # send the request to the OpenAI API
    response = requests.post(
        "https://api.openai.com/v1/responses",
        json=payload,
        headers=headers,
        timeout=45,
    )

    # check if the response is successful
    response.raise_for_status()

    # get the data from the response
    data = response.json()
    
    # get the output text from the data
    output_text = []
    for item in data.get("output", []):
        if item.get("type") == "message":
            for content in item.get("content", []):
                if content.get("type") == "output_text":
                    output_text.append(content.get("text", ""))

    return "\n".join(output_text).strip()
