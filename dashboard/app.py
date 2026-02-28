import streamlit as st
import sys
import os

# Ensure project root is in Python path
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)

from integration_logic_m3.router import handle_company_query

st.set_page_config(page_title="Corporate Risk Radar", layout="wide")

st.title("📊 Corporate Risk Radar")
st.write("Enter a company name to analyze financial risk, news sentiment, and overall risk score.")

company_name = st.text_input("Company Name", "")

if st.button("Analyze"):
    if company_name.strip() == "":
        st.warning("Please enter a company name.")
    else:
        result = handle_company_query(company_name)

        if result["mode"] == "name_not_found":
            st.error("Company not found in dataset.")
        elif result["mode"] == "ticker_not_in_dataset":
            st.error("Ticker found but no financial data available.")
        else:
            fin = result["financial_risk"]
            news = result["news_sentiment"]
            final = result["final_risk"]

            st.subheader("🏢 Company Information")
            st.write(f"**Name:** {result['company_name']}")
            st.write(f"**Ticker:** {result['ticker']}")

            st.subheader("📉 Financial Risk")
            st.metric("Prediction (0 = Low Risk, 1 = High Risk)", fin["prediction"])
            st.metric("Risk Probability", round(fin["risk_probability"], 4))
            st.write(f"**Data Year Used:** {fin['date_used']}")

            st.subheader("📰 News Sentiment")
            if news["found"]:
                st.metric("Sentiment Score (-1 to +1)", round(news["sentiment_score"], 4))

                for article in news["articles"]:
                    st.write(f"### {article['title']}")
                    st.write(article["description"])
                    st.write(f"[Read more]({article['url']})")
                    st.write(f"Sentiment: {round(article['sentiment'], 4)}")
                    st.write("---")
            else:
                st.write("No news found.")

            st.subheader("🔥 Final Risk Score")
            st.metric("Final Risk Score (0 = Safe, 1 = Risky)", round(final["final_risk_score"], 4))
            st.write(f"**Financial Component:** {round(final['financial_component'], 4)}")
            st.write(f"**Sentiment Component:** {round(final['sentiment_component'], 4)}")
            st.write(f"**Weights:** {final['weights']}")
