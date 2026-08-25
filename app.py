import subprocess
import sys

# yfinance లేకపోతే ఆటోమేటిక్‌గా ఇన్స్టాల్ చేసే లాజిక్
try:
    import yfinance as yf
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance"])
    import yfinance as yf

import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Order Flow Mobile", layout="centered")

st.markdown("""
    <style>
    .metric-card {
        background-color: #1e222d;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 10px;
        color: white;
    }
    .bullish { border-left: 5px solid #26a69a; }
    .bearish { border-left: 5px solid #ef5350; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Live Nifty Tracker")

def fetch_market_data():
    try:
        nifty = yf.Ticker("^NSEI")
        df = nifty.history(period="1d", interval="1m")
        
        if df.empty:
            return []

        latest_price = round(df['Close'].iloc[-1], 2)
        open_price = df['Open'].iloc[0]
        price_change = round(latest_price - open_price, 2)
        curr_time = datetime.datetime.now().strftime("%H:%M:%S")
        
        state = "BULL" if price_change >= 0 else "BEAR"
        signal = "STRONG TREND" if abs(price_change) > 50 else "SIDEWAYS / FLOW ONLY"
        wall = f"Day Open: {round(open_price, 2)} | Change: {price_change}"

        return [
            {"Time": curr_time, "Strike": f"NIFTY SPOT ({latest_price})", "State": state, "Signal": signal, "Wall": wall}
        ]
    except Exception as e:
        return []

if st.button("🔄 Refresh Market Data"):
    st.rerun()

data = fetch_market_data()

if not data:
    st.info("Market Data Loading... (Or Market Closed)")
else:
    for row in data:
        card_class = "bullish" if row["State"] == "BULL" else "bearish"
        color = "#26a69a" if row["State"] == "BULL" else "#ef5350"
        
        st.markdown(f"""
        <div class="metric-card {card_class}">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <b style="font-size: 16px;">{row['Time']} | {row['Strike']}</b>
                <span style="background-color:{color}; padding:2px 8px; border-radius:4px; font-weight:bold;">{row['State']}</span>
            </div>
            <div style="margin-top:8px; font-size:14px;">
                <b>Signal:</b> {row['Signal']}<br>
                <b>Status:</b> {row['Wall']}
            </div>
        </div>
        """, unsafe_allow_html=True)
