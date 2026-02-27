from integration_logic_m3.ticker_map import name_to_ticker
from integration_logic_m3.predict import predict_financial_risk
from news_sentiment.news_engine import get_news_sentiment
from integration_logic_m3.risk_engine import combine_risk



def handle_company_query(company_name: str):
    # Step 1: Convert name → ticker
    ticker = name_to_ticker(company_name)

    if not ticker:
        return {
            "mode": "name_not_found",
            "company_name": company_name,
            "message": "Company name not found in dataset."
        }

    # Step 2: Predict financial risk
    fin = predict_financial_risk(ticker)

    if not fin["found"]:
        return {
            "mode": "ticker_not_in_dataset",
            "company_name": company_name,
            "ticker": ticker,
            "message": "Ticker exists but no financial data found."
        }

    # Step 3: Fetch news sentiment
    news = get_news_sentiment(company_name)
    sentiment_score = news["sentiment_score"] if news["found"] else None

    # Step 4: Combine into final risk
    final = combine_risk(
        financial_prob=fin["risk_probability"],
        sentiment_score=sentiment_score
    )

    # Step 5: Return everything
    return {
        "mode": "verified_dataset",
        "company_name": fin["company_name"],
        "ticker": ticker,
        "financial_risk": fin,
        "news_sentiment": news,
        "final_risk": final
    }


if __name__ == "__main__":
    print(handle_company_query("ADANI ENTERPRISES LIMITED"))
