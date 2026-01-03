# AI & Tech Daily Digest

An automated daily pipeline that fetches, ranks, and delivers the most relevant AI and technology news via email.

This project runs entirely server-side using GitHub Actions and sends a curated digest every morning without requiring any local machine or manual intervention.

---

## Overview

The AI & Tech Daily Digest is a Python-based automation that:

- Ingests AI and technology news from a REST API  
- Ranks articles using heuristic scoring based on relevance, source credibility, and recency  
- Selects the top articles from a larger candidate pool  
- Automatically emails a daily digest to a distribution list  
- Runs on a fixed daily schedule via GitHub Actions  

---

## Motivation

The pace of development in AI and technology makes it difficult to stay consistently up to date. Important developments are often spread across many sources, mixed with low-signal or repetitive content.

This project was built to:
- Create a lightweight, reliable way to surface the most relevant AI news each day  
- Reduce noise by prioritizing high-quality sources and technically relevant topics  
- Establish a daily habit of staying informed without manual searching  
- Introduce accountability by delivering a scheduled digest that cannot be ignored  

Rather than relying on ad-hoc browsing or social media feeds, this system provides a structured, automated approach to staying current with major AI and technology developments.

---

## How It Works

### 1. Data Ingestion (REST API)
- Fetches recent AI-related news from NewsAPI using authenticated HTTP GET requests  
- Retrieves structured JSON responses containing article metadata  

### 2. Heuristic Ranking
Each article is scored using a rule-based heuristic that combines:
- Keyword relevance (AI concepts, labs, companies)
- Source credibility (e.g. Reuters and Bloomberg weighted higher)
- Recency (newer articles prioritized)

Articles are sorted by score, and the top results are selected for delivery.

### 3. Automated Delivery
- Formats the ranked articles into a readable digest
- Sends the digest via email using SMTP (Gmail App Password authentication)
- Supports multiple recipients via a distribution list

### 4. Scheduling and Infrastructure
- Deployed using GitHub Actions
- Runs daily via a cron schedule (UTC-adjusted for Eastern Time)
- Secrets (API keys and email credentials) are managed securely using GitHub Secrets

---

## Tech Stack

- Language: Python  
- APIs: NewsAPI (REST, JSON)  
- Automation: GitHub Actions (CI/CD and scheduling)  
- Email: SMTP (Gmail App Passwords)  
- Security: Environment-based secret management  

---

## Security and Best Practices

- No credentials are committed to the repository  
- API keys and email credentials are stored as GitHub Actions secrets  
- Each workflow run executes in a fresh, isolated environment  

---

## Future Improvements

Potential extensions include:
- LLM-based article summarization  
- Personalized ranking per recipient  
- Slack or Notion delivery  
- Historical trend tracking  
- Learned ranking models  

---

## Example Output

Subject:  
AI and Tech Daily Digest — <Date>

Body:  
Ranked list of top AI and technology news articles with direct source links.

---

## License

This project is for educational and personal use.
