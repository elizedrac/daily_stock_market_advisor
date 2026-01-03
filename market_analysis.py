from typing import List, Dict
import requests
from config import OPENAI_API_KEY


def analyze_articles(articles: List[Dict], model: str = "gpt-4o-mini") -> str:
    """
    Take already-fetched news articles and return a concise LLM stock analysis.
    Expects each article to have 'title', 'description', 'url', and 'source'.
    """
    if not OPENAI_API_KEY or not OPENAI_API_KEY.strip():
        raise RuntimeError("OPENAI_API_KEY is missing. Set it in your environment or .env.")

    if not articles:
        return "No articles provided for analysis."

    prompt_lines = [
        "You are an equity analyst. From these articles, give 3-5 actionable stock recommendations with tickers, rationale, and major risks. If unsure, say so.",
        "",
        "Articles:",
    ]
    for article in articles:
        prompt_lines.append(
            f"- {article.get('title')} ({article.get('source', {}).get('name')}): "
            f"{article.get('description') or ''} {article.get('url')}"
        )

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

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY.strip()}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        "https://api.openai.com/v1/responses",
        json=payload,
        headers=headers,
        timeout=45,
    )

    response.raise_for_status()

    data = response.json()

    output_text = []
    for item in data.get("output", []):
        if item.get("type") == "message":
            for content in item.get("content", []):
                if content.get("type") == "output_text":
                    output_text.append(content.get("text", ""))

    return "\n".join(output_text).strip()
