import streamlit as st
import json
import urllib.request
from datetime import datetime, timedelta, timezone

st.set_page_config(page_title="Live Market Tracker", layout="centered")

# Auto Refresh every 10 seconds
st.markdown("<meta http-equiv='refresh' content='10'>", unsafe_allow_html=True)

st.markdown("""
    <style>
    .metric-card {
        background-color: #1e222d;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 12px;
        color: white;
    }
    .bullish { border-left: 5px solid #26a69a; }
    .bearish { border-left: 5px solid #ef5350; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Live Market Tracker")

def fetch_symbol_data(symbol, name):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1m&range=1d"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode())
        
        meta = data['chart']['result'][0]['meta']
        latest_price = round(meta['regularMarketPrice'], 2)
        previous_close = round(meta['chartPreviousClose'], 2)
        price_change = round(latest_price - previous_close, 2)
        
        # Indian Standard Time (IST: UTC+5:30)
        ist_offset = timezone(timedelta(hours=5, minutes=30))
        curr_time = datetime.now(ist_offset).strftime("%I:%M:%S %p")
        
        state = "BULL" if price_change >= 0 else "BEAR"
        signal = "STRONG TREND" if abs(price_change) > 50 else "SIDEWAYS / FLOW ONLY"
        wall = f"Prev Close: {previous_close} | Change: {price_change}"

        return {"Time": curr_time, "Symbol": f"{name} ({latest_price})", "State": state, "Signal": signal, "Wall": wall}
    except Exception as e:
        return None

# Fetching Nifty & Sensex Data
nifty_data = fetch_symbol_data("%5NSEI", "NIFTY SPOT")
sensex_data = fetch_symbol_data("%5BSESN", "SENSEX")

symbols_data = [d for d in [nifty_data, sensex_data] if d is not None]

if not symbols_data:
    st.info("Market Data Loading...")
else:
    for row in symbols_data:
        card_class = "bullish" if row["State"] == "BULL" else "bearish"
        color = "#26a69a" if row["State"] == "BULL" else "#ef5350"
        
        st.markdown(f"""
        <div class="metric-card {card_class}">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <b style="font-size: 15px;">{row['Time']} | {row['Symbol']}</b>
                <span style="background-color:{color}; padding:2px 8px; border-radius:4px; font-weight:bold;">{row['State']}</span>
            </div>
            <div style="margin-top:8px; font-size:14px;">
                <b>Signal:</b> {row['Signal']}<br>
                <b>Status:</b> {row['Wall']}
            </div>
        </div>
        """, unsafe_allow_html=True)


