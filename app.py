import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# Page Config
st.set_page_config(
    page_title="NIFTY Institutional Pro Terminal",
    page_icon="⚡",
    layout="wide"
)

ist = ZoneInfo("Asia/Kolkata")
now_ist = datetime.now(ist)

# Custom Dark Styling & Mobile Fixes
st.markdown("""
    <style>
    .stApp { background-color: #0E1117 !important; color: #FFFFFF !important; }
    
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
    .delta-trap-box {
        background: linear-gradient(135deg, rgba(255, 152, 0, 0.15), rgba(213, 0, 0, 0.15));
        border: 2px solid #FFA726;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 12px;
        text-align: center;
    }
    .badge-bull { background-color: #00C853; color: #000; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; }
    .badge-bear { background-color: #D50000; color: #FFF; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; }
    .txt-green { color: #00E676; font-weight: bold; }
    .txt-red { color: #FF1744; font-weight: bold; }
    .txt-blue { color: #29B6F6; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Live Data Simulation Variables
spot = 24240.00
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
is_divergence = np.random.choice([True, False], p=[0.35, 0.65])

# Header Section
st.title("⚡ NIFTY Institutional Pro Terminal")
st.success(f"🟢 Connected | {now_ist.strftime('%I:%M:%S %p')} IST")
st.caption(f"SPOT: **₹{spot:,.2f}** | VWAP: **₹{vwap_val:,.2f}** | Zero Gamma: **{zero_gamma_line}** | ATM: **{atm_strike}**")

# Top Banner Alerts (Gamma & Divergence)
st.markdown(f"""
    <div class="gex-box">
        <h3 style="color: #AB47BC; margin:0;">🔮 Zero Gamma Level & GEX Matrix</h3>
        <p style="margin: 5px 0 0 0; color: #FFF; font-size: 13px;">
            Zero Gamma Line: <strong class="txt-blue">{zero_gamma_line}</strong> | 
            మార్కెట్ ఈ లెవెల్ పైన ఉంటే వొలటైలిటీ కంట్రోల్‌లో ఉంటుంది, కిందకి వెళ్తే వైల్డ్ స్పైక్స్ వస్తాయి!
        </p>
    </div>
""", unsafe_allow_html=True)

if is_divergence:
    st.markdown(f"""
        <div class="delta-trap-box">
            <h4 style="color: #FFA726; margin:0;">⚠️ CUMULATIVE DELTA DIVERGENCE DETECTED!</h4>
            <p style="margin: 4px 0 0 0; color: #FFF; font-size: 13px;">ప్రైస్ ఒక వైపు వెళ్తుంటే, అగ్రెసివ్ డెల్టా (CDELTA: <strong>{cDelta_val:+d}</strong>) వ్యతిరేక దిశలో ఉంది. స్మార్ట్ మనీ ట్రాప్ జరిగే ఛాన్స్ ఉంది!</p>
        </div>
    """, unsafe_allow_html=True)

# Multi-Tab Architecture
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🔮 Gamma Exposure", 
    "🪤 OI Unwinding Traps", 
    "📊 Volume Profile",
    "📍 VWAP & SD Bands",
    "🌊 Cumulative Delta",
    "🎯 Strike Flow",
    "⚡ IV & Skew"
])

with tab1:
    st.subheader("🔮 Gamma Exposure (Dealer Hedging Impact)")
    st.caption("మార్కెట్ మేకర్స్ (Dealers) ఏ స్ట్రైక్స్ వద్ద హెడ్జింగ్ కోసం ఒత్తిడి తెస్తున్నారో చూపే మ్యాపింగ్:")
    
    gex_data = [
        {"Strike": atm_strike - 100, "Net GEX": "-1,450 Cr", "Dealer State": "Short Gamma (High Volatility Zone)"},
        {"Strike": atm_strike - 50, "Net GEX": "-620 Cr", "Dealer State": "Transition Zone"},
        {"Strike": atm_strike, "Net GEX": "+3,800 Cr", "Dealer State": "Long Gamma (Pinning Effect / Support)"},
        {"Strike": atm_strike + 50, "Net GEX": "+2,100 Cr", "Dealer State": "Long Gamma (Resistance Wall)"},
        {"Strike": atm_strike + 100, "Net GEX": "+4,500 Cr", "Dealer State": "Heavy Call Wall (Cap)"}
    ]
    st.dataframe(pd.DataFrame(gex_data), use_container_width=True, hide_index=True)
    st.info("💡 **GEX టిప్:** పాజిటివ్ GEX ఉన్నప్పుడు మార్కెట్ ఒక రేంజ్‌లో లాక్ అవుతుంది. నెగటివ్ GEXలోకి వెళ్తే అకస్మాత్తుగా మూవ్‌మెంట్ మారుతుంది.")

with tab2:
    st.subheader("🪤 OI Unwinding & Seller Trap Detector")
    
    st.markdown("""
        <div class="trap-alert-box">
            <h4 style="color: #FF9800; margin:0 0 4px 0;">⚠️ ACTIVE SELLER TRAP DETECTED NEAR 24200 PE</h4>
            <p style="margin: 0; color: #FFF; font-size: 13px;">పుట్ రైటర్లు భారీగా ట్రాప్ అయ్యి పొజిషన్స్ కట్ చేసుకుంటున్నారు. షార్ట్ కవరింగ్ ద్వారా మార్కెట్ పైకి దూసుకుపోయే ఛాన్స్ ఉంది!</p>
        </div>
    """, unsafe_allow_html=True)
    
    trap_rows = [
        {"Strike": atm_strike - 50, "Writer Type": "Put Writers (Support)", "OI Action": "Unwinding (-18.4L)", "Trap Status": "🚨 TRAPPED (Bullish Trigger)"},
        {"Strike": atm_strike, "Writer Type": "Straddle Writers", "OI Action": "Aggressive Shifting", "Trap Status": "Neutral Range Bound"},
        {"Strike": atm_strike + 50, "Writer Type": "Call Writers (Resistance)", "OI Action": "Fresh Addition (+22.1L)", "Trap Status": "Strong Ceiling"}
    ]
    st.dataframe(pd.DataFrame(trap_rows), use_container_width=True, hide_index=True)

with tab3:
    st.subheader("📊 Volume Profile & Value Area (VAH / VAL)")
    st.markdown(f"""
        <div class="val-box">
            <h4 style="color: #29B6F6; margin:0 0 6px 0;">Institutional Value Zones (70% Volume Area)</h4>
            <p style="margin: 3px 0; font-size: 13px;">VAH (Value Area High): <strong class="txt-red">₹{vah}</strong> (Upper Fair Value)</p>
            <p style="margin: 3px 0; font-size: 13px;">POC (Point of Control): <strong class="txt-blue">₹{poc}</strong> (Max Traded Price)</p>
            <p style="margin: 3px 0; font-size: 13px;">VAL (Value Area Low): <strong class="txt-green">₹{val}</strong> (Lower Fair Value)</p>
        </div>
    """, unsafe_allow_html=True)
    st.caption("మార్కెట్ VAH దాటితే బ్రేక్‌అవుట్, VAL కిందకి వెళ్తే బ్రేక్‌డౌన్ ట్రేడ్స్ తీసుకోవచ్చు.")

with tab4:
    st.subheader("📍 VWAP & Standard Deviation (SD) Intelligence")
    st.markdown(f"""
        <div class="vwap-box">
            <h4 style="color: #29B6F6; margin:0 0 8px 0;">Institutional VWAP Boundaries</h4>
            <p style="margin: 4px 0; font-size: 13px;">+2 SD Upper Band: <strong class="txt-red">₹{sd2_upper:,.2f}</strong> (Strong Resistance)</p>
            <p style="margin: 4px 0; font-size: 13px;">+1 SD Upper Band: <strong class="txt-red">₹{sd1_upper:,.2f}</strong> (Trailing Resistance)</p>
            <p style="margin: 4px 0; font-size: 13px;">VWAP Fair Value: <strong class="txt-blue">₹{vwap_val:,.2f}</strong> (Control Line)</p>
            <p style="margin: 4px 0; font-size: 13px;">-1 SD Lower Band: <strong class="txt-green">₹{sd1_lower:,.2f}</strong> (Trailing Support)</p>
            <p style="margin: 4px 0; font-size: 13px;">-2 SD Lower Band: <strong class="txt-green">₹{sd2_lower:,.2f}</strong> (Strong Support / Bounce Zone)</p>
        </div>
    """, unsafe_allow_html=True)
    
    if spot >= sd1_upper:
        st.warning("⚠️ మార్కెట్ VWAP పైకి వెళ్లి +1 SD దాటింది. ఓవర్‌బాట్ జోన్ - ప్రాఫిట్ బుకింగ్ గమనించండి.")
    elif spot <= sd1_lower:
        st.info("💡 మార్కెట్ VWAP కింద -1 SD దగ్గర ఉంది. సపోర్ట్ బౌన్స్ కోసం చూడండి.")
    else:
        st.success("✅ మార్కెట్ VWAP ఫెయిర్ వాల్యూ జోన్‌లో కదులుతోంది.")

with tab5:
    st.subheader("🌊 Order Flow Cumulative Delta (CDELTA)")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Net Cumulative Delta", value=f"{cDelta_val:+d} Contracts", delta="Aggressive Buyers" if cDelta_val > 0 else "Aggressive Sellers")
    with col2:
        st.metric(label="Delta Momentum Rate", value="Fast Accumulation", delta="High Volume")
    with col3:
        st.metric(label="Institutional Block Trades", value="Active", delta="Neutral Zone")

    st.markdown("---")
    st.markdown("### 📊 Recent Order Flow Delta Ticks")
    delta_ticks = [
        {"Time": "13:03", "Price": spot + 2, "Delta Tick": "+240 (Buy)", "Execution State": "Aggressive Buying at VWAP"},
        {"Time": "13:02", "Price": spot - 1, "Delta Tick": "-180 (Sell)", "Execution State": "Limit Wall Absorption"},
        {"Time": "13:01", "Price": spot + 4, "Delta Tick": "+410 (Buy)", "Execution State": "Breakout Push"},
        {"Time": "13:00", "Price": spot - 3, "Delta Tick": "-320 (Sell)", "Execution State": "Supply Zone Rejection"}
    ]
    st.dataframe(pd.DataFrame(delta_ticks), use_container_width=True, hide_index=True)

with tab6:
    st.subheader("🎯 Specific Strike Imbalance")
    strikes = [atm_strike + (i * 50) for i in range(-4, 5)]
    strike_rows = [{"Strike": s, "CE Vol": f"{np.random.randint(15, 85)}L", "PE Vol": f"{np.random.randint(15, 85)}L", "Ratio": round(np.random.uniform(0.7, 1.6), 2)} for s in strikes]
    st.dataframe(pd.DataFrame(strike_rows), use_container_width=True, hide_index=True)

with tab7:
    st.subheader("⚡ Implied Volatility (IV) & Skew Monitor")
    st.info("📉 **ATM IV:** 13.40% | Put Skew active on downside strikes.")

# Auto Refresh Control Panel
st.sidebar.title("⚡ Control Panel")
auto = st.sidebar.checkbox("⚡ Live Auto-Refresh (5 sec)", value=True)
if auto:
    time.sleep(5)
    st.rerun()
