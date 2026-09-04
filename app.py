import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime
from zoneinfo import ZoneInfo

st.set_page_config(
    page_title="NIFTY Simulated Pro Terminal",
    page_icon="⚡",
    layout="wide"
)

ist = ZoneInfo("Asia/Kolkata")
now_ist = datetime.now(ist)

st.markdown("""
    <style>
    .stApp { background-color: #0E1117 !important; color: #FFFFFF !important; }
    .card-bull {
        background: linear-gradient(135deg, rgba(0, 200, 83, 0.12), rgba(0, 230, 118, 0.02));
        border: 1px solid #00C853;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
    }
    .card-bear {
        background: linear-gradient(135deg, rgba(213, 0, 0, 0.12), rgba(255, 23, 68, 0.02));
        border: 1px solid #D50000;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
    }
    .badge-bull { background-color: #00C853; color: #000; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; }
    .badge-bear { background-color: #D50000; color: #FFF; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; }
    .badge-alignment { background-color: #29B6F6; color: #000; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; }
    .txt-green { color: #00E676; font-weight: bold; }
    .txt-red { color: #FF1744; font-weight: bold; }
    .txt-blue { color: #29B6F6; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Simulated live random data generation
base_spot = 24225.50
random_offset = np.random.uniform(-10, 10)
spot = round(base_spot + random_offset, 2)
atm_strike = round(spot / 50) * 50

st.title("⚡ NIFTY Pro Terminal (Smart Simulation Mode)")
st.success(f"🟢 సిమ్యులేటెడ్ లైవ్ మోడ్ యాక్టివ్! | {now_ist.strftime('%I:%M:%S %p')} IST")
st.caption(f"NIFTY 50 SPOT: **₹{spot:,.2f}** | ATM STRIKE: **{atm_strike}**")

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 1-Min Candle Flow", 
    "🎯 Strike Wise Imbalance", 
    "⏳ MTF Matrix",
    "🏆 Win Probability"
])

current_time_str = now_ist.strftime('%H:%M')

with tab1:
    st.subheader("⏱️ 1-Min All Candles Flow (Wall Touch & Alignment)")
    
    simulated_flows = [
        {"Time": current_time_str, "Price": f"₹{spot}", "Type": np.random.choice(["BULL", "BEAR"]), "State": np.random.choice(["STRONG ALIGNMENT", "No wall touch", "WALL TOUCH (+2 SD)"]), "CE": round(np.random.uniform(1.0, 5.0), 2), "PE": round(np.random.uniform(50.0, 90.0), 2)},
        {"Time": "12:44", "Price": "₹24220.20", "Type": "BULL", "State": "STRONG ALIGNMENT", "CE": 2.67, "PE": 1.11},
        {"Time": "12:43", "Price": "₹24218.10", "Type": "BULL", "State": "STRONG ALIGNMENT", "CE": 64.8, "PE": 18.7},
        {"Time": "12:42", "Price": "₹24215.00", "Type": "BEAR", "State": "No wall touch", "CE": 53.1, "PE": 76.7}
    ]
    
    for f in simulated_flows:
        if f["Type"] == "BULL":
            card_class = "card-bull"
            badge = '<span class="badge-bull">BULL</span>'
        else:
            card_class = "card-bear"
            badge = '<span class="badge-bear">BEAR</span>'
            
        state_badge = f'<span class="badge-alignment">{f["State"]}</span>' if "ALIGNMENT" in f["State"] or "TOUCH" in f["State"] else f'<span style="color: #888; font-size: 12px;">State: {f["State"]}</span>'
        
        st.markdown(f"""
            <div class="{card_class}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <strong style="font-size: 16px;">{f['Time']} &nbsp; <span style="color: #ddd;">{f['Price']}</span></strong> 
                    {badge}
                </div>
                <div style="margin: 6px 0 4px 0;">{state_badge}</div>
                <p style="margin: 0; font-size: 13px; color: #00E676;">Strike Flow: {atm_strike} CE ({f['CE']}Cr / PE {f['PE']}Cr)</p>
            </div>
        """, unsafe_allow_html=True)

with tab2:
    st.subheader("🎯 Strike Wise Imbalance (ATM ± 6)")
    strikes = [atm_strike + (i * 50) for i in range(-5, 6)]
    strike_rows = [{"Strike": s, "CE Vol": f"{np.random.randint(15, 85)}L", "PE Vol": f"{np.random.randint(15, 85)}L", "Ratio": round(np.random.uniform(0.7, 1.7), 2)} for s in strikes]
    st.dataframe(pd.DataFrame(strike_rows), use_container_width=True, hide_index=True)

with tab3:
    st.subheader("⏳ Multi-Timeframe (1m, 3m, 5m) Matrix")
    mtf_data = [
        {"Timeframe": "1-Min", "Trend": "BULLISH", "Role": "Quick Scalping Trigger"},
        {"Timeframe": "3-Min", "Trend": "BULLISH", "Role": "Momentum Confirmation"},
        {"Timeframe": "5-Min", "Trend": "BULLISH", "Role": "Intraday Trend Anchor"}
    ]
    st.dataframe(pd.DataFrame(mtf_data), use_container_width=True, hide_index=True)

with tab4:
    st.subheader("🏆 Win Probability & Strike Ranking")
    ranking_data = [
        {"Strike": f"{atm_strike - 150} (ITM)", "Win Probability": "68%", "Delta": "0.8", "Status": "Rank 1 (Best) - High Delta & Low Decay"},
        {"Strike": f"{atm_strike - 50} (ITM)", "Win Probability": "68%", "Delta": "0.6", "Status": "Rank 1 (Best) - Balanced"},
        {"Strike": f"{atm_strike} (ATM)", "Win Probability": "52%", "Delta": "0.5", "Status": "Rank 2 (High Momentum)"}
    ]
    st.dataframe(pd.DataFrame(ranking_data), use_container_width=True, hide_index=True)

# Auto Refresh Control Panel
st.sidebar.title("⚡ Control Panel")
auto = st.sidebar.checkbox("⚡ Live Auto-Refresh (3 sec)", value=True)
if auto:
    time.sleep(3)
    st.rerun()
