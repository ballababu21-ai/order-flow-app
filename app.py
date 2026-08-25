import streamlit as st
import json
import urllib.request
import datetime

st.set_page_config(page_title="Live Nifty Tracker", layout="centered")

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

def fetch_nifty_data():
    try:
        url = "https://query1.finance.yahoo.com/v8/finance/chart/%5ENSEI?interval=1m&range=1d"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode())
        
        result = data['chart']['result'][0]
        meta = result['meta']
        
        latest_price = round(meta['regularMarketPrice'], 2)
        previous_close = round(meta['chartPreviousClose'], 2)
        price_change = round(latest_price - previous_close, 2)
        curr_time = datetime.datetime.now().strftime("%H:%M:%S")
        
        state = "BULL" if price_change >= 0 else "BEAR"
        signal = "STRONG TREND" if abs(price_change) > 50 else "SIDEWAYS / FLOW ONLY"
        wall = f"Prev Close: {previous_close} | Change: {price_change}"

        return [
            {"Time": curr_time, "Strike": f"NIFTY SPOT ({latest_price})", "State": state, "Signal": signal, "Wall": wall}
        ]
    except Exception as e:
        return []

if st.button("🔄 Refresh Market Data"):
    st.rerun()

data = fetch_nifty_data()

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

