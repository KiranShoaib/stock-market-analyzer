import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

# 🛠 Set Page Layout
st.set_page_config(layout="wide")

# 🎨 Custom CSS for Background and Styling
st.markdown("""
    <style>
        /* Custom Background */
        .stApp {
            background-color: #f5f7fa;
            color: #333;
        }

        /* Center Content */
        .block-container {
            max-width: 1000px;
            margin: auto;
            padding: 20px;
            background: white;
            border-radius: 15px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        }

        /* Header */
        h1 {
            color: #2b7de9;
            text-align: center;
        }

        /* Sidebar */
        .sidebar .sidebar-content {
            background: #2b7de9 !important;
            color: white;
        }

        /* Improve Buttons & Links */
        .stButton>button {
            background: #ff5722;
            color: white;
            border-radius: 10px;
        }

        /* Table Styling */
        .dataframe {
            border-radius: 10px;
            overflow: hidden;
        }
    </style>
""", unsafe_allow_html=True)

# 📌 App Title
st.title("📈 Stock Market Analyzer")

# 🔍 Sidebar Inputs
st.sidebar.header("📅 Select Date Range")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

# 📊 User input for stock symbol
ticker = st.text_input("🔎 Enter Stock Symbol (e.g., AAPL, TSLA, GOOG):", "AAPL").upper()

# Fetch Stock Data
if ticker:
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date, end=end_date)

        if hist.empty:
            st.warning("⚠️ No data found! Please check the stock symbol or date range.")
        else:
            st.success(f"📊 Showing data for {ticker}")

            # 📄 Show Data Table
            st.subheader("📄 Recent Stock Data")
            st.dataframe(hist.tail(10))

            # 📉 Stock Price Trend
            st.subheader("📉 Stock Price Trend")
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.lineplot(x=hist.index, y=hist['Close'], ax=ax, label="Closing Price", color="blue")
            ax.set_xlabel("Date")
            ax.set_ylabel("Price (USD)")
            ax.legend()
            st.pyplot(fig)

            # 📊 Candlestick Chart
            st.subheader("📊 Candlestick Chart")
            reduced_hist = hist.iloc[-90:]  # Last 90 days for performance
            fig_candle = go.Figure()
            fig_candle.add_trace(go.Candlestick(
                x=reduced_hist.index,
                open=reduced_hist['Open'],
                high=reduced_hist['High'],
                low=reduced_hist['Low'],
                close=reduced_hist['Close'],
                name="Candlestick"
            ))
            st.plotly_chart(fig_candle, use_container_width=True)

            # 📰 Stock News (Fixed Titles & Links)
            st.subheader("📰 Latest Stock News")
            news = stock.news if hasattr(stock, "news") else []

            valid_news = [article for article in news if article.get("title") and article.get("link")]
            
            if valid_news:
                for article in valid_news[:5]:
                    title = article["title"]
                    link = article["link"]
                    st.markdown(f"🔹 [{title}]({link})", unsafe_allow_html=True)
            else:
                st.write("⚠️ No news found for this stock.")

    except Exception as e:
        st.error(f"❌ Error: {e}")


