from typing import List, Dict
import requests
from config import OPENAI_API_KEY, STOCKS_OF_INTEREST


def analyze_articles(articles: List[Dict], model: str = "gpt-4o-mini") -> str:
    # check if the API key is set
    if not OPENAI_API_KEY or not OPENAI_API_KEY.strip():
        raise RuntimeError("OPENAI_API_KEY is missing. Set it in your environment or .env.")

    # check if any articles are provided
    if not articles:
        return "No articles provided for analysis."

    # create the prompt (tune as needed)
    prompt_lines = [
    f"You are an equity analyst. Portfolio: {', '.join([f'{t} ({n})' for t, n in STOCKS_OF_INTEREST])}.",
    "Instructions:",
    "- For each article that mentions a portfolio ticker, summarize the news, price/vol impact, and key risks; cite title/source.",
    "- Give a 1–2 sentence hold/buy/sell view per mentioned portfolio ticker.",
    "- From articles not about portfolio tickers, propose up to 2 new tickers with rationale and major risks; if uncertain or insufficient info, say so.",
    "- If an article has nothing investment-useful, note that briefly.",
    "Format:",
    "Portfolio updates:",
    "- <TICKER>: <summary>; risks: <...>; view: <buy/hold/sell> (source: <title/source>)",
    "Potential investments:",
    "- <TICKER>: <rationale>; risks: <...> (source: <title/source>)",
    "",
    "Articles:",
    ]
    for article in articles:
        prompt_lines.append(
            f"- {article.get('title')} ({article.get('source', {}).get('name')}): "
            f"{article.get('description') or ''} {article.get('url')}"
        )

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
