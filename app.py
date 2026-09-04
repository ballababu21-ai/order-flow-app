import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# Page Config
st.set_page_config(
    page_title="NIFTY Ultimate Institutional Pro Terminal",
    page_icon="⚡",
    layout="wide"
)

ist = ZoneInfo("Asia/Kolkata")
now_ist = datetime.now(ist)

# Custom Dark Styling & Mobile Fixes
st.markdown("""
    <style>
    .stApp { background-color: #0E1117 !important; color: #FFFFFF !important; }
    
    .mega-bull-box {
        background: linear-gradient(135deg, rgba(0, 200, 83, 0.2), rgba(0, 230, 118, 0.05));
        border: 2px solid #00C853;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 12px;
        text-align: center;
    }
    .mega-bear-box {
        background: linear-gradient(135deg, rgba(213, 0, 0, 0.2), rgba(255, 23, 68, 0.05));
        border: 2px solid #D50000;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 12px;
        text-align: center;
    }
    .gex-box {
        background: linear-gradient(135deg, rgba(156, 39, 176, 0.2), rgba(33, 150, 243, 0.1));
        border: 2px solid #AB47BC;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 12px;
        text-align: center;
    }
    .trap-alert-box {
        background: linear-gradient(135deg, rgba(255, 152, 0, 0.2), rgba(213, 0, 0, 0.2));
        border: 2px solid #FF9800;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 12px;
    }
    .val-box {
        background: rgba(41, 182, 246, 0.1);
        border: 1px solid #29B6F6;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
    }
    .vwap-box {
        background: linear-gradient(135deg, rgba(41, 182, 246, 0.15), rgba(33, 150, 243, 0.05));
        border: 1px solid #29B6F6;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 12px;
    }
    .badge-bull { background-color: #00C853; color: #000; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; }
    .badge-bear { background-color: #D50000; color: #FFF; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; }
    .txt-green { color: #00E676; font-weight: bold; }
    .txt-red { color: #FF1744; font-weight: bold; }
    .txt-blue { color: #29B6F6; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Live Data Simulation Variables
spot = 24225.50
fut = 24244.00
atm_strike = round(spot / 50) * 50
zero_gamma_line = atm_strike - 25
vah = atm_strike + 75
val = atm_strike - 75
poc = atm_strike
vwap_val = 24215.50
sd1_upper = vwap_val + 42.0
sd2_upper = vwap_val + 84.0
sd1_lower = vwap_val - 42.0
sd2_lower = vwap_val - 84.0
cDelta_val = np.random.randint(-1500, 1800)
is_bullish_mtf = np.random.choice([True, False])

# Header Section
st.title("⚡ NIFTY (MTF + OI + POC + GEX) Terminal")
st.success(f"🟢 Connected | {now_ist.strftime('%I:%M:%S %p')} IST")
st.caption(f"SPOT: **₹{spot:,.2f}** | FUT: **₹{fut:,.2f}** | ATM: **{atm_strike}**")

# Top Banner MTF Status
if is_bullish_mtf:
    st.markdown("""
        <div class="mega-bull-box">
            <h3 style="color: #00C853; margin:0;">🚀 1m + 3m + 5m MEGA BULLISH</h3>
            <p style="margin: 4px 0 0 0; color: #FFF; font-size: 13px;">అన్ని టైమ్‌ఫ్రేమ్‌లు బయింగ్ వైపు అలైన్ అయ్యాయి!</p>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="mega-bear-box">
            <h3 style="color: #FF1744; margin:0;">📉 1m + 3m + 5m MEGA BEARISH</h3>
            <p style="margin: 4px 0 0 0; color: #FFF; font-size: 13px;">అన్ని టైమ్‌ఫ్రేమ్‌లు సెల్లింగ్ వైపు అలైన్ అయ్యాయి!</p>
        </div>
    """, unsafe_allow_html=True)

# Multi-Tab Architecture (Including Flow Cards, MTF Matrix, Win Probability)
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "📊 Flow Cards", 
    "⏳ MTF Matrix", 
    "🏆 Win Probability",
    "🎯 Strike Flow", 
    "📈 Futures & OI",
    "📌 Volume POC",
    "🔮 Gamma & Traps", 
    "📍 VWAP & SD",
    "🌊 Cum. Delta"
])

with tab1:
    st.subheader("⏱️ Live Order Flow")
    order_flows = [
        {"Time": "13:01", "Price": "₹24,228.84", "Type": "BEAR", "Details": "Strike Flow: 24300 CE (55.5Cr / PE 81.7Cr)"},
        {"Time": "13:00", "Price": "₹24,224.17", "Type": "BULL", "Details": "Strike Flow: 24200 PE (75.8Cr / PE 18.1Cr)"},
        {"Time": "12:59", "Price": "₹24,227.04", "Type": "BEAR", "Details": "Strike Flow: 24300 CE (73.6Cr / PE 71.0Cr)"},
        {"Time": "12:58", "Price": "₹24,224.58", "Type": "BULL", "Details": "Strike Flow: 24200 PE (60.0Cr / PE 75.7Cr)"}
    ]
    for f in order_flows:
        badge = '<span class="badge-bear">BEAR</span>' if f["Type"] == "BEAR" else '<span class="badge-bull">BULL</span>'
        st.markdown(f"""
            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; padding: 10px; margin-bottom: 8px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <strong>{f['Time']} ({f['Price']})</strong> {badge}
                </div>
                <p style="margin: 4px 0 0 0; font-size: 12px; color: #aaa;">{f['Details']}</p>
            </div>
        """, unsafe_allow_html=True)

with tab2:
    st.subheader("⏳ Multi-Timeframe (1m, 3m, 5m) Matrix")
    mtf_data = [
        {"Timeframe": "1-Min", "Trend": "BULLISH" if is_bullish_mtf else "BEARISH", "Role": "Quick Scalping Trigger"},
        {"Timeframe": "3-Min", "Trend": "BULLISH" if is_bullish_mtf else "BEARISH", "Role": "Momentum Confirmation"},
        {"Timeframe": "5-Min", "Trend": "BULLISH" if is_bullish_mtf else "BEARISH", "Role": "Intraday Trend Anchor"}
    ]
    st.dataframe(pd.DataFrame(mtf_data), use_container_width=True, hide_index=True)
    st.info("💡 **రూల్:** 1m, 3m, 5m అన్నీ ఒకే వైపు ఉంటేనే ట్రేడ్ తీసుకోవడం సురక్షితం.")

with tab3:
    st.subheader("🏆 Strike Ranking & Win Probability")
    st.caption("డెల్టా మరియు విన్ ప్రాబబిలిటీ ఆధారంగా బెస్ట్ స్ట్రైక్స్:")
    ranking_data = [
        {"Strike": "24100 (ITM 150 pts)", "Win Probability": "68%", "Delta": "0.8", "Status": "Rank 1 (Best) - High Delta & Low Decay"},
        {"Strike": "24150 (ITM 100 pts)", "Win Probability": "68%", "Delta": "0.7", "Status": "Rank 1 (Best) - High Delta & Low Decay"},
        {"Strike": "24200 (ITM 50 pts)", "Win Probability": "68%", "Delta": "0.6", "Status": "Rank 1 (Best) - Balanced"},
        {"Strike": "24250 (ATM)", "Win Probability": "52%", "Delta": "0.5", "Status": "Rank 2 (High Momentum)"}
    ]
    st.dataframe(pd.DataFrame(ranking_data), use_container_width=True, hide_index=True)

with tab4:
    st.subheader("🎯 Specific Strike Imbalance")
    strikes = [atm_strike + (i * 50) for i in range(-4, 5)]
    strike_rows = [{"Strike": s, "CE Vol": f"{np.random.randint(15, 85)}L", "PE Vol": f"{np.random.randint(15, 85)}L", "Ratio": round(np.random.uniform(0.7, 1.7), 2)} for s in strikes]
    st.dataframe(pd.DataFrame(strike_rows), use_container_width=True, hide_index=True)

with tab5:
    st.subheader("📈 Futures & Open Interest (OI)")
    st.markdown("""
        <div class="val-box">
            <h4 style="color: #29B6F6; margin:0 0 4px 0;">⚡ LIVE OI BUILDUP TRACKER</h4>
            <p style="margin: 0; font-size: 13px;">Current Market Classification: <strong class="txt-blue">SHORT COVERING</strong></p>
            <p style="margin: 4px 0 0 0; font-size: 12px; color: #ccc;">Price Up + OI Down: షార్ట్ సెల్లర్లు భయపడి పొజిషన్స్ కట్ చేసుకుంటున్నారు (Rapid Upside Spike).</p>
        </div>
    """, unsafe_allow_html=True)

with tab6:
    st.subheader("📌 Volume POC (Point of Control)")
    st.markdown(f"""
        <div class="val-box">
            <h4 style="color: #29B6F6; margin:0 0 4px 0;">🎯 Volume POC Strike: {poc}</h4>
            <p style="margin: 0; font-size: 13px;">ఈ స్ట్రిక్ వద్ద అత్యధిక ట్రేడింగ్ వాల్యూమ్ నమోదైంది. ఇది కీలకమైన సపోర్ట్/రెసిస్టెన్స్‌లా పనిచేస్తుంది.</p>
        </div>
    """, unsafe_allow_html=True)
    poc_rows = [
        {"Zone": "Above POC (Resistance)", "Status": "Stp > 24300", "Action": "Look for Rejection / Put Entry"},
        {"Zone": "At POC (Fair Value)", "Status": f"Range {poc} ± 25", "Action": "Consolidation Zone (Avoid)"},
        {"Zone": "Below POC (Support)", "Status": "Stp < 24200", "Action": "Look for Support Bounce"}
    ]
    st.dataframe(pd.DataFrame(poc_rows), use_container_width=True, hide_index=True)

with tab7:
    st.subheader("🔮 Gamma Exposure & OI Traps")
    st.markdown(f"""
        <div class="gex-box">
            <h4 style="color: #AB47BC; margin:0;">Zero Gamma Line: {zero_gamma_line}</h4>
            <p style="margin: 4px 0 0 0; font-size: 13px;">మార్కెట్ ఈ లెవెల్ పైన ఉంటే వొలటైలిటీ కంట్రోల్‌లో ఉంటుంది!</p>
        </div>
    """, unsafe_allow_html=True)
    trap_rows = [
        {"Strike": atm_strike - 50, "Writer Type": "Put Writers", "OI Action": "Unwinding (-18.4L)", "Trap Status": "🚨 TRAPPED (Bullish Trigger)"},
        {"Strike": atm_strike + 50, "Writer Type": "Call Writers", "OI Action": "Fresh Addition (+22.1L)", "Trap Status": "Strong Ceiling"}
    ]
    st.dataframe(pd.DataFrame(trap_rows), use_container_width=True, hide_index=True)

with tab8:
    st.subheader("📍 VWAP & Standard Deviation Bands")
    st.markdown(f"""
        <div class="vwap-box">
            <p style="margin: 3px 0; font-size: 13px;">+2 SD Upper Band: <strong class="txt-red">₹{sd2_upper:,.2f}</strong></p>
            <p style="margin: 3px 0; font-size: 13px;">VWAP Fair Value: <strong class="txt-blue">₹{vwap_val:,.2f}</strong></p>
            <p style="margin: 3px 0; font-size: 13px;">-2 SD Lower Band: <strong class="txt-green">₹{sd2_lower:,.2f}</strong></p>
        </div>
    """, unsafe_allow_html=True)

with tab9:
    st.subheader("🌊 Cumulative Delta (CDELTA)")
    st.metric(label="Net Cumulative Delta", value=f"{cDelta_val:+d} Contracts", delta="Aggressive Momentum")

# Auto Refresh Control Panel
st.sidebar.title("⚡ Control Panel")
auto = st.sidebar.checkbox("⚡ Live Auto-Refresh (5 sec)", value=True)
if auto:
    time.sleep(5)
    st.rerun()
