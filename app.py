import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# Page Config
st.set_page_config(
    page_title="NIFTY Institutional Pro Terminal (Advanced)",
    page_icon="⚡",
    layout="wide"
)

ist = ZoneInfo("Asia/Kolkata")
now_ist = datetime.now(ist)

# Custom Dark Styling & Mobile Fixes
st.markdown("""
    <style>
    .stApp { background-color: #0E1117 !important; color: #FFFFFF !important; }
    
    .row-bull-box {
        background-color: rgba(0, 200, 83, 0.12);
        border: 1px solid #00C853;
        border-radius: 6px;
        padding: 10px;
        margin-bottom: 8px;
    }
    .row-bear-box {
        background-color: rgba(213, 0, 0, 0.12);
        border: 1px solid #D50000;
        border-radius: 6px;
        padding: 10px;
        margin-bottom: 8px;
    }
    
    .gex-card {
        background: linear-gradient(135deg, rgba(156, 39, 176, 0.15), rgba(33, 150, 243, 0.05));
        border: 1px solid #AB47BC;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
    }
    .trap-card {
        background: linear-gradient(135deg, rgba(255, 152, 0, 0.15), rgba(213, 0, 0, 0.15));
        border: 1px solid #FF9800;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
    }
    .val-box {
        background: rgba(41, 182, 246, 0.1);
        border: 1px solid #29B6F6;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
    }

    .badge-bull { background-color: #00C853; color: #000; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; }
    .badge-bear { background-color: #D50000; color: #FFF; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; }
    .badge-trap { background-color: #FF9800; color: #000; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; }
    
    .txt-green { color: #00E676; font-weight: bold; }
    .txt-red { color: #FF1744; font-weight: bold; }
    .txt-blue { color: #29B6F6; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Market Simulation Variables
spot = 24225.50
atm_strike = round(spot / 50) * 50
fut_price = spot + 18.5
zero_gamma = atm_strike - 25
vah = atm_strike + 75
val_zone = atm_strike - 75
c_delta = np.random.randint(-1500, 1800)

st.title("⚡ NIFTY Pro Terminal (Advanced Engine)")
st.success(f"🟢 Connected | {now_ist.strftime('%I:%M:%S %p')} IST")
st.caption(f"SPOT: **₹{spot:,.2f}** | FUT: **₹{fut_price:,.2f}** | ATM: **{atm_strike}**")

# Tabs including 4 New Advanced Features
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Flow Cards", 
    "🔮 GEX & Zero Gamma", 
    "🌊 C-Delta Divergence",
    "📌 Volume POC (VAH/VAL)",
    "🚨 OI Trap Detector",
    "⏳ MTF Matrix",
    "🏆 Win Probability"
])

with tab1:
    st.subheader("⏱️ Live Order Flow")
    for i in range(3):
        t_str = (now_ist - timedelta(minutes=i)).strftime("%H:%M")
        is_bull = (i % 2 != 0)
        box_class = "row-bull-box" if is_bull else "row-bear-box"
        side_badge = '<span class="badge-bull">BULL</span>' if is_bull else '<span class="badge-bear">BEAR</span>'
        stk = atm_strike + (-50 if is_bull else 50)
        st.markdown(f"""
        <div class="{box_class}">
            <div style="display: flex; justify-content: space-between;">
                <strong>{t_str} (₹{spot})</strong> {side_badge}
            </div>
            <div style="font-size: 12px; margin-top:4px;">
                Strike Flow: <strong class="txt-blue">{stk} {'PE' if is_bull else 'CE'}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.subheader("🔮 Gamma Exposure (GEX) & Zero Gamma Level")
    st.markdown(f"""
        <div class="gex-card">
            <h4 style="color: #AB47BC; margin:0 0 5px 0;">⚡ Zero Gamma Level: {zero_gamma}</h4>
            <p style="margin: 0; font-size: 13px;">మార్కెట్ ఈ లెవెల్ పైన ఉన్నంతవరకు వొలటైలిటీ కంట్రోల్‌లో ఉంటుంది. బిగ్ ప్లేయర్స్ హెడ్జింగ్ జోన్ ఇది.</p>
        </div>
    """, unsafe_allow_html=True)
    gex_data = [
        {"Strike": atm_strike - 50, "Call GEX": "+42Cr", "Put GEX": "-18Cr", "Net Exposure": "Bullish Support"},
        {"Strike": atm_strike, "Call GEX": "+85Cr", "Put GEX": "-72Cr", "Net Exposure": "Neutral Pivot"},
        {"Strike": atm_strike + 50, "Call GEX": "-95Cr", "Put GEX": "+30Cr", "Net Exposure": "Bearish Wall"}
    ]
    st.dataframe(pd.DataFrame(gex_data), use_container_width=True, hide_index=True)

with tab3:
    st.subheader("🌊 Cumulative Delta (C-Delta) & Divergence")
    st.metric(label="Net Cumulative Delta", value=f"{c_delta:+d} Contracts", delta="Momentum Check")
    if c_delta > 0:
        st.success("🟢 **డిల్టా పాజిటివ్:** బయింగ్ ప్రెషర్ బలంగా ఉంది. ప్రైస్ బ్రేక్‌అవుట్ జెన్యూన్ అయ్యే ఛాన్స్ ఉంది.")
    else:
        st.error("🔴 **డెల్టా డైవర్జెన్స్ (Fake Breakout):** ప్రైస్ పైకి వెళ్తున్నప్పటికీ డెల్టా నెగటివ్‌గా ఉంది. ఇది ఫేక్ బ్రేక్‌అవుట్ కావచ్చు!")

with tab4:
    st.subheader("📌 Momentum Volume Profile (VAH / VAL)")
    st.markdown(f"""
        <div class="val-box">
            <h4 style="color: #29B6F6; margin:0 0 5px 0;">📊 Value Area Boundaries</h4>
            <p style="margin: 2px 0; font-size: 13px;">VAH (Value Area High): <strong class="txt-red">₹{vah}</strong></p>
            <p style="margin: 2px 0; font-size: 13px;">POC (Point of Control): <strong class="txt-blue">₹{atm_strike}</strong></p>
            <p style="margin: 2px 0; font-size: 13px;">VAL (Value Area Low): <strong class="txt-green">₹{val_zone}</strong></p>
        </div>
    """, unsafe_allow_html=True)
    st.info("💡 **రూల్:** ప్రైస్ VAH దాటితే బయింగ్ మొమెంటమ్, VAL కిందకి వెళితే సెల్లింగ్ ప్రెషర్ పెరుగుతుంది.")

with tab5:
    st.subheader("🚨 OI Trap Detector (Short/Long Traps)")
    st.markdown("""
        <div class="trap-card">
            <h4 style="color: #FF9800; margin:0 0 5px 0;">⚠️ PUT WRITERS TRAPPED AT 24200</h4>
            <p style="margin: 0; font-size: 13px;">పుట్ రైటర్లు ఇరుక్కుపోయారు. మార్కెట్ షార్ట్ కవరింగ్ ఇచ్చి వేగంగా పైకి వెళ్లే అవకాశం ఉంది!</p>
        </div>
    """, unsafe_allow_html=True)
    trap_rows = [
        {"Strike": atm_strike - 50, "Writer": "Put Writers", "Status": "🚨 TRAPPED (Short Covering Expected)", "Action": "Look for Call Entry"},
        {"Strike": atm_strike + 50, "Writer": "Call Writers", "Status": "Safe / Hedged", "Action": "Watch for Resistance"}
    ]
    st.dataframe(pd.DataFrame(trap_rows), use_container_width=True, hide_index=True)

with tab6:
    st.subheader("⏳ Multi-Timeframe (1m, 3m, 5m) Matrix")
    mtf_data = [
        {"Timeframe": "1-Min", "Trend": "BULLISH", "Role": "Quick Scalping Trigger"},
        {"Timeframe": "3-Min", "Trend": "BULLISH", "Role": "Momentum Confirmation"},
        {"Timeframe": "5-Min", "Trend": "BULLISH", "Role": "Intraday Trend Anchor"}
    ]
    st.dataframe(pd.DataFrame(mtf_data), use_container_width=True, hide_index=True)

with tab7:
    st.subheader("🏆 Strike Ranking & Win Probability")
    ranking_data = [
        {"Strike": f"{atm_strike - 50} (ITM)", "Win Probability": "68%", "Delta": "0.6", "Status": "Rank 1 (Best) - Balanced"},
        {"Strike": f"{atm_strike} (ATM)", "Win Probability": "52%", "Delta": "0.5", "Status": "Rank 2 (High Momentum)"}
    ]
    st.dataframe(pd.DataFrame(ranking_data), use_container_width=True, hide_index=True)

# Auto Refresh Control
st.sidebar.title("⚡ Control Panel")
auto = st.sidebar.checkbox("⚡ Live Auto-Refresh (5 sec)", value=True)
if auto:
    time.sleep(5)
    st.rerun()
