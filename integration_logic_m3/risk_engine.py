def combine_risk(financial_prob, sentiment_score):
    # Normalize sentiment from [-1, 1] → [0, 1]
    if sentiment_score is None:
        sentiment_norm = 0.5  # neutral if no news
    else:
        sentiment_norm = (sentiment_score + 1) / 2

    # Weighting
    w_fin = 0.7
    w_news = 0.3

    final_score = (financial_prob * w_fin) + ((1 - sentiment_norm) * w_news)

    return {
        "final_risk_score": final_score,
        "financial_component": financial_prob,
        "sentiment_component": sentiment_norm,
        "weights": {"financial": w_fin, "news": w_news}
    }
