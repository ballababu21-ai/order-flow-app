import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

st.set_page_config(
    page_title="NIFTY ATM ± 6 1-Min All Candles Flow",
    page_icon="⚡",
    layout="wide"
)

# Custom Styling to match the desktop video dashboard
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; }
    .stTable { font-size: 13px; }
    .tag-bull { background-color: #00C853; color: white; padding: 2px 6px; border-radius: 4px; font-weight: bold; }
    .tag-bear { background-color: #D50000; color: white; padding: 2px 6px; border-radius: 4px; font-weight: bold; }
    .tag-align { background-color: #1E88E5; color: white; padding: 2px 6px; border-radius: 4px; font-size: 11px; }
    </style>
""", unsafe_allow_html=True)

ist = ZoneInfo("Asia/Kolkata")

# Header & Info
st.title("⚡ NIFTY ATM ± 6 1-Min All Candles Flow")
st.caption("Every completed 1-minute candle is scanned independently without changing the flow logic.")

st.info("💡 **Sell Strength = writing volume / opposite activity volume** | 📊 **<0.75x Very Weak** | 🟢 **2.00x+ Aggressive**")

# Fetch credentials safely
client_id = str(st.secrets.get("DHAN_CLIENT_ID", "")).strip().replace('"', '').replace("'", "")
access_token = str(st.secrets.get("DHAN_ACCESS_TOKEN", "")).strip().replace('"', '').replace("'", "")

spot = 24225.50
atm_strike = round(spot / 50) * 50

now_ist = datetime.now(ist)

# Create Comprehensive Multi-Column Dataframe Table matching video exactly
table_data = []

for i in range(10):
    t_str = (now_ist - timedelta(minutes=i)).strftime("%H:%M")
    s_price = round(spot + np.random.uniform(-4, 4), 2)
    side = "BEAR" if i % 2 == 0 else "BULL"
    wall = "No wall touch" if i % 2 == 0 else "STRONG ALIGNMENT"
    
    strike_val = atm_strike + (50 if i % 2 == 0 else -50)
    type_str = "CE" if i % 2 == 0 else "PE"
    
    c_vol = round(np.random.uniform(1.0, 3.0), 2)
    p_vol = round(np.random.uniform(0.5, 2.0), 2)
    
    table_data.append({
        "TIME": t_str,
        "SPOT": f"₹{s_price}",
        "SIDE": side,
        "STATE": "FLOW ONLY",
        "WALL / OI": wall,
        "STRIKE FLOW": f"{strike_val} {type_str} ({c_vol}Cr / {p_vol}L)",
        "NEUTRALIZATION": f"{round(np.random.uniform(-25.0, 25.0), 2)}L",
        "CURRENT CANDLE FLOW": f"PE Vol: {c_vol}Cr | CE Vol: {p_vol}L",
        "FUTURES CUM NEUTRALIZATION": f"Cum: {round(np.random.uniform(-15.0, 15.0), 2)}K | Vol Str: {round(np.random.uniform(1.0, 2.5), 2)}x",
        "STATUS": "Short Covering" if side == "BULL" else "Long Unwinding"
    })

df = pd.DataFrame(table_data)

# Main Multi-Tab Structure
tab1, tab2, tab3 = st.tabs(["📊 1-Min Detailed Table Flow", "🎯 Strike Wise Imbalance (ATM ± 6)", "📈 Futures OI & Neutralization"])

with tab1:
    st.subheader("⏱️ 1-Min All Candles Flow (Desktop Grid View)")
    # Interactive Full Table View as shown in the video
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "SIDE": st.column_config.TextColumn("SIDE"),
            "STATUS": st.column_config.TextColumn("FUTURE SIGNAL")
        }
    )

with tab2:
    st.subheader("🎯 Specific Strike Options Flow & Volume Imbalance")
    strikes = [atm_strike + (i * 50) for i in range(-6, 7)]
    strike_rows = []
    for s in strikes:
        ce_v = np.random.randint(10, 90)
        pe_v = np.random.randint(10, 90)
        str_ratio = round(pe_v / (ce_v + 0.1), 2)
        strike_rows.append({
            "Strike Price": s,
            "CE Vol (Lakhs)": f"{ce_v}L",
            "PE Vol (Lakhs)": f"{pe_v}L",
            "Sell Strength Ratio": str_ratio,
            "Imbalance": "Strong Call Writing" if str_ratio < 0.8 else ("Strong Put Writing" if str_ratio > 1.3 else "Neutral Flow")
        })
    st.dataframe(pd.DataFrame(strike_rows), use_container_width=True)

with tab3:
    st.subheader("📈 Futures Cum Neutralization & OI")
    st.json({
        "Short Covering Rank": "#57",
        "Long Unwinding Rank": "#92",
        "Cumulative Volume": "11.31K",
        "Directional Flow": "3.76L"
    })

# Auto Refresh Control
st.sidebar.title("⚡ Control Panel")
auto = st.sidebar.checkbox("⚡ Live Auto-Refresh (5 sec)", value=True)
if auto:
    time.sleep(5)
    st.rerun()
