import requests
from textblob import TextBlob
import os


NEWS_API_KEY = os.getenv("NEWS_API_KEY")
 # Replace with your key

def fetch_news(company_name):
    url = (
        "https://newsapi.org/v2/everything?"
        f"q={company_name}&"
        "sortBy=publishedAt&"
        "language=en&"
        f"apiKey={NEWS_API_KEY}"
    )

    response = requests.get(url)
    data = response.json()

    if data.get("status") != "ok":
        return None

    articles = data.get("articles", [])
    return articles[:5]  # top 5 articles

def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity  # -1 to +1

def get_news_sentiment(company_name):
    articles = fetch_news(company_name)

    if not articles:
        return {
            "found": False,
            "sentiment_score": None,
            "articles": []
        }

    scores = []
    cleaned_articles = []

    for a in articles:
        title = a.get("title", "")
        desc = a.get("description", "")

        combined = f"{title}. {desc}"
        score = analyze_sentiment(combined)

        scores.append(score)

        cleaned_articles.append({
            "title": title,
            "description": desc,
            "url": a.get("url"),
            "sentiment": score
        })

    avg_score = sum(scores) / len(scores)

    return {
        "found": True,
        "sentiment_score": avg_score,
        "articles": cleaned_articles
    }

if __name__ == "__main__":
    print(get_news_sentiment("Adani Enterprises"))
