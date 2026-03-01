import requests
from textblob import TextBlob
import os
from dotenv import load_dotenv

# Load the hidden .env file
load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_news(company_name):
    print(f"\n--- ATTEMPTING TO FETCH NEWS FOR: {company_name} ---")
    
    if not NEWS_API_KEY:
        print("🚨 ERROR: NEWS_API_KEY is completely blank! The .env file isn't working.")
        return None

    url = "https://newsapi.org/v2/everything"
    
    # Using 'params' safely formats spaces (e.g., "Adani Enterprises" -> "Adani%20Enterprises")
    params = {
        "q": company_name,
        "sortBy": "publishedAt",
        "language": "en",
        "apiKey": NEWS_API_KEY
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if data.get("status") != "ok":
            print(f"🚨 NEWS API ERROR: {data.get('message', 'Unknown error')}")
            return None

        articles = data.get("articles", [])
        print(f"✅ SUCCESS: Found {len(articles)} articles!")
        return articles[:5]  # top 5 articles
        
    except Exception as e:
        print(f"🚨 REQUEST CRASHED: {e}")
        return None

def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

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
        
        # Safety check in case title or description is missing
        if not title: title = ""
        if not desc: desc = ""

        combined = f"{title}. {desc}"
        score = analyze_sentiment(combined)
        scores.append(score)

        cleaned_articles.append({
            "title": title,
            "description": desc,
            "url": a.get("url"),
            "sentiment": score
        })

    if len(scores) > 0:
        avg_score = sum(scores) / len(scores)
    else:
        avg_score = 0

    return {
        "found": True,
        "sentiment_score": avg_score,
        "articles": cleaned_articles
    }

if __name__ == "__main__":
    print(get_news_sentiment("Adani Enterprises"))