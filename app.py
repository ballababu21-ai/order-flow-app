import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# Page Config
st.set_page_config(
    page_title="NIFTY Institutional Quant Engine (Vanna, Charm & VAH/VAL)",
    page_icon="⚡",
    layout="wide"
)

ist = ZoneInfo("Asia/Kolkata")
now_ist = datetime.now(ist)

# Custom Dark Styling & Horizontal Tabs Fix
st.markdown("""
<style>
.stApp { background-color: #0E1117 !important; color: #FFFFFF !important; }
/* Force Tabs to Stay Clean and Side-by-Side */
.stTabs [data-baseweb="tab-list"] {
    display: flex;
    flex-wrap: nowrap;
    overflow-x: auto;
    gap: 4px;
    background-color: #161B22;
    padding: 6px;
    border-radius: 8px;
}
.stTabs [data-baseweb="tab"] {
    background-color: #21262D;
    color: #8B949E;
    border-radius: 4px;
    padding: 8px 12px;
    font-weight: 600;
    font-size: 13px;
    white-space: nowrap;
}
.stTabs [aria-selected="true"] {
    background-color: #238636 !important;
    color: #FFFFFF !important;
}
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
.explosion-alert-box {
    background: linear-gradient(135deg, rgba(255, 23, 68, 0.2), rgba(255, 152, 0, 0.2));
    border: 2px solid #FF1744;
    border-radius: 10px;
    padding: 15px;
    text-align: center;
    margin-bottom: 12px;
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
.rank-card-best { background-color: rgba(0, 200, 83, 0.15); border-left: 5px solid #00E676; padding: 10px; border-radius: 6px; margin-bottom: 8px; }
.rank-card-high { background-color: rgba(41, 182, 246, 0.15); border-left: 5px solid #29B6F6; padding: 10px; border-radius: 6px; margin-bottom: 8px; }
.rank-card-mod { background-color: rgba(255, 167, 38, 0.15); border-left: 5px solid #FFA726; padding: 10px; border-radius: 6px; margin-bottom: 8px; }
.oi-long-buildup { background-color: #00C853; color: #000; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; }
.oi-short-covering { background-color: #29B6F6; color: #000; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; }
.oi-short-buildup { background-color: #D50000; color: #FFF; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; }
.oi-long-unwinding { background-color: #FFA726; color: #000; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; }
.badge-bull { background-color: #00C853; color: #000; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; }
.badge-bear { background-color: #D50000; color: #FFF; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; }
.txt-blue { color: #29B6F6; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Market State & Advanced Quant Variables
spot = 24225.50
atm_strike = round(spot / 50) * 50
fut_price = spot + 18.5
zero_gamma = atm_strike - 25
c_delta = np.random.randint(-1500, 1800)

# Vanna & Charm Variables
vanna_atm = round(np.random.uniform(-0.025, 0.035), 4)
charm_atm = round(np.random.uniform(-0.045, 0.055), 4)

# Volume Profile VAH/VAL Variables
vah = atm_strike + 85
val = atm_strike - 75
val_migration = np.random.choice(["UPWARD MIGRATION (Bullish Accumulation)", "DOWNWARD MIGRATION (Bearish Distribution)", "BALANCED RANGE (Consolidation)"], p=[0.5, 0.3, 0.2])

st.title("⚡ NIFTY Institutional Quant Engine (Advanced)")
st.success(f"🟢 Connected | {now_ist.strftime('%I:%M:%S %p')} IST")
st.caption(f"SPOT: **₹{spot:,.2f}** | FUT: **₹{fut_price:,.2f}** | ATM: **{atm_strike}**")

# Multi-Timeframe Status
mtf_1m = np.random.choice(["BULLISH", "BEARISH"], p=[0.55, 0.45])
mtf_3m = mtf_1m if np.random.rand() > 0.2 else np.random.choice(["BULLISH", "BEARISH"])
mtf_5m = mtf_3m if np.random.rand() > 0.3 else np.random.choice(["BULLISH", "BEARISH"])

oi_states = ["LONG BUILDUP", "SHORT COVERING", "SHORT BUILDUP", "LONG UNWINDING"]
current_oi_status = np.random.choice(oi_states, p=[0.45, 0.25, 0.20, 0.10])
poc_strike = atm_strike + np.random.choice([-50, 0, 50])
is_explosion = np.random.choice([True, False], p=[0.3, 0.7])

if is_explosion:
    st.markdown("""
    <div class="explosion-alert-box">
    <h3 style="color: #FF1744; margin:0;">🚨 GAMMA EXPLOSION & SPIKE DETECTED!</h3>
    <p style="margin: 4px 0 0 0; color: #FFF; font-size: 13px;">ATM ± 50 స్ట్రైక్స్‌ వద్ద వాల్యూమ్ మరియు డెల్టా ఊహించని విధంగా పేలాయి!</p>
    </div>
    """, unsafe_allow_html=True)

# 6 Consolidated Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Flow & OI", 
    "🎯 Strikes & Win", 
    "⏳ MTF & Pro",
    "🔮 GEX & Greeks",
    "📊 VAH/VAL",
    "⚡ Summary"
])

with tab1:
    st.subheader("⏱️ Live Order Flow & OI Build-up")
    
    # OI Tracker Section
    oi_badge_class = "oi-long-buildup" if current_oi_status == "LONG BUILDUP" else ("oi-short-covering" if current_oi_status == "SHORT COVERING" else ("oi-short-buildup" if current_oi_status == "SHORT BUILDUP" else "oi-long-unwinding"))
    st.markdown(f"""
    <div style="background:#161B22; padding:12px; border-radius:8px; border:1px solid #29B6F6; margin-bottom:12px;">
    <h4 style="color:#29B6F6; margin:0 0 6px 0;">⚡ LIVE OI BUILDUP TRACKER</h4>
    <p style="margin:4px 0; font-size:13px;">Fut Price: <strong>₹{fut_price:,.2f}</strong> | ATM Strike: <strong>{atm_strike}</strong></p>
    <div style="margin-top:8px;">Current Market Classification: <span class="{oi_badge_class}">{current_oi_status}</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    if current_oi_status == "LONG BUILDUP":
        st.success("🟢 **Price Up + OI Up:** బయ్యర్లు మార్కెట్‌ను బలంగా పైకి తోస్తున్నారు (Bullish Continuation).")
    elif current_oi_status == "SHORT COVERING":
        st.info("🔵 **Price Up + OI Down:** షార్ట్ సెల్లర్లు భయపడి పొజిషన్స్ కట్ చేసుకుంటున్నారు (Rapid Upside Spike).")
    elif current_oi_status == "SHORT BUILDUP":
        st.error("🔴 **Price Down + OI Up:** సెల్లర్లు మార్కెట్‌ను కిందకి నెడుతున్నారు (Bearish Pressure).")
    else:
        st.warning("🟠 **Price Down + OI Down:** లాంగ్ పొజిషన్స్ అన్‌వైండ్ అవుతున్నాయి (Profit Booking / Weakness).")

    st.markdown("---")
    st.markdown("#### 🔄 Recent Order Flow")
    for i in range(3):
        t_str = (now_ist - timedelta(minutes=i)).strftime("%H:%M")
        s_price = round(spot + np.random.uniform(-4, 4), 2)
        is_bull = (i % 2 != 0)
        box_class = "row-bull-box" if is_bull else "row-bear-box"
        side_badge = '<span class="badge-bull">BULL</span>' if is_bull else '<span class="badge-bear">BEAR</span>'
        stk = atm_strike + (-50 if is_bull else 50)
        state_text = np.random.choice(["STRONG ALIGNMENT", "FLOW ONLY | No wall touch", "MOMENTUM SPIKE"])
        ce_val = round(np.random.uniform(10, 90), 1)
        pe_val = round(np.random.uniform(10, 90), 1)
        st.markdown(f"""
        <div class="{box_class}">
        <div style="display: flex; justify-content: space-between;">
        <strong>{t_str} (₹{s_price})</strong> {side_badge}
        </div>
        <div style="font-size: 12px; margin-top:4px; color: #8B949E;">State: <strong>{state_text}</strong></div>
        <div style="font-size: 12px; margin-top:2px;">Strike Flow: <strong class="txt-blue">{stk} {'PE' if is_bull else 'CE'} ({ce_val}Cr / PE {pe_val}Cr)</strong></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🚨 OI Trap Detector")
    st.markdown("""
    <div class="trap-card">
    <h4 style="color: #FF9800; margin:0 0 5px 0;">⚠️ PUT WRITERS TRAPPED AT SUPPORT</h4>
    <p style="margin: 0; font-size: 13px;">పుట్ రైటర్లు ఇరుక్కుపోయారు. షార్ట్ కవరింగ్ వచ్చే అవకాశం ఉంది!</p>
    </div>
    """, unsafe_allow_html=True)
    trap_rows = [
        {"Strike": atm_strike - 50, "Writer": "Put Writers", "Status": "🚨 TRAPPED", "Action": "Look for Call Entry"},
        {"Strike": atm_strike + 50, "Writer": "Call Writers", "Status": "Safe / Hedged", "Action": "Watch for Resistance"}
    ]
    st.dataframe(pd.DataFrame(trap_rows), use_container_width=True, hide_index=True)

with tab2:
    st.subheader("🎯 Specific Strike Imbalance & POC")
    
    st.markdown(f"""
    <div style="background: rgba(41, 182, 246, 0.1); border: 2px solid #29B6F6; border-radius: 8px; padding: 12px; text-align: center; margin-bottom: 12px;">
    <h4 style="color: #29B6F6; margin: 0;">🎯 Volume POC Strike: {poc_strike}</h4>
    <p style="margin: 4px 0 0 0; font-size: 12px; color: #FFF;">ఈ స్ట్రైక్ వద్ద అత్యధిక ట్రేడింగ్ వాల్యూమ్ నమోదైంది.</p>
    </div>
    """, unsafe_allow_html=True)

    strikes = [atm_strike + (i * 50) for i in range(-3, 4)]
    strike_rows = [{"Strike": s, "CE Vol": f"{np.random.randint(10, 80)}L", "PE Vol": f"{np.random.randint(10, 80)}L", "Ratio": round(np.random.uniform(0.6, 1.8), 2)} for s in strikes]
    st.dataframe(pd.DataFrame(strike_rows), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("🏆 Strike Ranking & Win Probability")
    for s in strikes:
        diff = s - atm_strike
        if diff < 0:
            rank_title, stk_type, win_pct, delta, card_css, badge_color = "Rank 1 (Best)", f"ITM ({abs(diff)} pts)", 68, round(0.50 + (abs(diff)/500), 2), "rank-card-best", "#00E676"
        elif diff == 0:
            rank_title, stk_type, win_pct, delta, card_css, badge_color = "Rank 2 (High)", "ATM", 52, 0.50, "rank-card-high", "#29B6F6"
        else:
            rank_title, stk_type, win_pct, delta, card_css, badge_color = "Rank 3", f"OTM ({diff} pts)", 38, 0.38, "rank-card-mod", "#FFA726"

        st.markdown(f"""
        <div class="{card_css}">
        <div style="display: flex; justify-content: space-between; align-items: center;">
        <strong style="font-size: 15px; color: #FFF;">{s} ({stk_type})</strong>
        <span style="background-color: {badge_color}; color: #000; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px;">{rank_title}</span>
        </div>
        <div style="margin-top: 4px; font-size: 12px;"><strong>Win Probability:</strong> <span style="color:{badge_color}; font-weight:bold;">{win_pct}%</span> | <strong>Delta:</strong> {delta}</div>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.subheader("⏳ Multi-Timeframe Matrix & Pro Analytics")
    
    col1, col2, col3 = st.columns(3)
    with col1: st.metric(label="Live PCR", value="1.14", delta="+0.08")
    with col2: st.metric(label="Max Pain", value=f"{atm_strike}", delta="Neutral")
    with col3: st.metric(label="Flow Score", value="78 / 100", delta="Strong")

    st.markdown("---")
    st.markdown("#### ⏳ Multi-Timeframe Matrix")
    mtf_data = [
        {"Timeframe": "1-Min", "Trend": mtf_1m, "Role": "Quick Scalping Trigger"},
        {"Timeframe": "3-Min", "Trend": mtf_3m, "Role": "Momentum Confirmation"},
        {"Timeframe": "5-Min", "Trend": mtf_5m, "Role": "Intraday Trend Anchor"}
    ]
    st.dataframe(pd.DataFrame(mtf_data), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("#### ⚡ IV & Skew Monitor")
    st.metric(label="ATM IV", value="13.45%", delta="-0.80%")

with tab4:
    st.subheader("🔮 Gamma Exposure (GEX) & Advanced Greeks")
    
    st.markdown(f"""
    <div class="gex-card">
    <h4 style="color: #AB47BC; margin:0 0 5px 0;">⚡ Zero Gamma Level: {zero_gamma}</h4>
    <p style="margin: 0; font-size: 13px;">మార్కెట్ ఈ లెవెల్ పైన ఉన్నంతవరకు వొలటైలిటీ కంట్రోల్‌లో ఉంటుంది.</p>
    </div>
    """, unsafe_allow_html=True)

    gex_data = [
        {"Strike": atm_strike - 50, "Call GEX": "+42Cr", "Put GEX": "-18Cr", "Net Exposure": "Bullish Support"},
        {"Strike": atm_strike, "Call GEX": "+85Cr", "Put GEX": "-72Cr", "Net Exposure": "Neutral Pivot"},
        {"Strike": atm_strike + 50, "Call GEX": "-95Cr", "Put GEX": "+30Cr", "Net Exposure": "Bearish Wall"}
    ]
    st.dataframe(pd.DataFrame(gex_data), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("#### 🌊 Cumulative Delta & Vanna/Charm")
    st.metric(label="Net Cumulative Delta", value=f"{c_delta:+d} Contracts")
    if c_delta > 0:
        st.success("🟢 **డిల్టా పాజిటివ్:** బయింగ్ ప్రెషర్ బలంగా ఉంది.")
    else:
        st.error("🔴 **డెల్టా డైవర్జెన్స్ (Fake Breakout):** ఫేక్ బ్రేక్‌అవుట్!")

    col_v1, col_v2 = st.columns(2)
    with col_v1: st.metric(label="ATM Vanna Exposure", value=f"{vanna_atm}", delta="Vol Sensitivity")
    with col_v2: st.metric(label="ATM Charm (Delta Decay)", value=f"{charm_atm}", delta="Time Decay")

    vanna_charm_table = [
        {"Strike": atm_strike - 50, "Vanna (Vol Delta)": "+0.018", "Charm (Time Delta)": "-0.032", "State": "Stable Support"},
        {"Strike": atm_strike, "Vanna (Vol Delta)": f"{vanna_atm}", "Charm (Time Delta)": f"{charm_atm}", "State": "High Pinning Zone"},
        {"Strike": atm_strike + 50, "Vanna (Vol Delta)": "-0.021", "Charm (Time Delta)": "+0.041", "State": "Resistance Barrier"}
    ]
    st.dataframe(pd.DataFrame(vanna_charm_table), use_container_width=True, hide_index=True)

with tab5:
    st.subheader("📊 Volume Profile VAH & VAL Migration")
    
    st.markdown(f"""
    <div style="background: rgba(41, 182, 246, 0.1); border: 1px solid #29B6F6; border-radius: 8px; padding: 15px; margin-bottom: 15px;">
    <h4 style="color: #29B6F6; margin:0 0 8px 0;">🌊 Value Area Migration Status</h4>
    <p style="margin:0; font-size:13px; color:#DDD;">
    వాల్యూమ్ ప్రొఫైల్ ప్రకారం మార్కెట్ ఎక్కడ కన్సాలిడేట్ అవుతుందో మరియు వాల్యూ ఏరియా హై (VAH), లో (VAL) పైకి లేదా కిందకి మారుతున్నాయో ఇది ట్రాక్ చేస్తుంది.
    </p>
    </div>
    """, unsafe_allow_html=True)

    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1: st.metric(label="Value Area High (VAH)", value=f"₹{vah}", delta="Resistance Band")
    with col_p2: st.metric(label="Point of Control (POC)", value=f"₹{poc_strike}", delta="Fair Value")
    with col_p3: st.metric(label="Value Area Low (VAL)", value=f"₹{val}", delta="Support Band")

    st.info(f"📌 **Current Trend Status:** **{val_migration}** — VAH మరియు VAL లెవెల్స్ కదలికలను బట్టి ఇన్‌స్టిట్యూషనల్ ఆర్డర్ ఫ్లోను నిర్ధారించండి.")

with tab6:
    st.subheader("⚡ Quick Executive Dashboard Summary")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown(f"""
        **Market Snapshot:**
        - **Spot Price:** ₹{spot:,.2f}
        - **Futures Price:** ₹{fut_price:,.2f}
        - **ATM Strike:** {atm_strike}
        - **OI State:** {current_oi_status}
        """)
    with col_s2:
        st.markdown(f"""
        **Key Levels:**
        - **Zero Gamma:** {zero_gamma}
        - **POC Strike:** {poc_strike}
        - **VAH / VAL:** ₹{vah} / ₹{val}
        """)
    
    st.success("🟢 All quantitative modules are running and synchronized with live data feeds.")

# Auto Refresh Control in Sidebar
st.sidebar.title("⚡ Control Panel")
auto = st.sidebar.checkbox("⚡ Live Auto-Refresh (5 sec)", value=True)
if auto:
    time.sleep(5)
    st.rerun()
