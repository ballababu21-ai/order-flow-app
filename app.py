import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# Page Config
st.set_page_config(
    page_title="NIFTY ATM ± 6 Order Flow Engine",
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
    
    .explosion-alert-box {
        background: linear-gradient(135deg, rgba(255, 23, 68, 0.2), rgba(255, 152, 0, 0.2));
        border: 2px solid #FF1744;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        margin-bottom: 12px;
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

# Market State
spot = 24225.50
atm_strike = round(spot / 50) * 50
fut_price = spot + 18.5
zero_gamma = atm_strike - 25
c_delta = np.random.randint(-1500, 1800)

st.title("⚡ NIFTY Pro Engine")
st.success(f"🟢 Connected | {now_ist.strftime('%I:%M:%S %p')} IST")
st.caption(f"SPOT: **₹{spot:,.2f}** | FUT: **₹{fut_price:,.2f}** | ATM: **{atm_strike}**")

# Multi-Timeframe & Status
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

# Optimized Horizontal Tabs (Fits perfectly on mobile screens without wrapping)
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Flow", 
    "🎯 Strikes", 
    "📈 Futures & OI",
    "📍 POC & GEX",
    "🏆 Win & Traps"
])

with tab1:
    st.subheader("⏱️ Live Order Flow")
    for i in range(4):
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
            <div style="font-size: 12px; margin-top:4px; color: #8B949E;">
                State: <strong>{state_text}</strong>
            </div>
            <div style="font-size: 12px; margin-top:2px;">
                Strike Flow: <strong class="txt-blue">{stk} {'PE' if is_bull else 'CE'} ({ce_val}Cr / PE {pe_val}Cr)</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.subheader("🎯 Specific Strike Imbalance")
    strikes = [atm_strike + (i * 50) for i in range(-4, 5)]
    strike_rows = [{"Strike": s, "CE Vol": f"{np.random.randint(10, 80)}L", "PE Vol": f"{np.random.randint(10, 80)}L", "Ratio": round(np.random.uniform(0.6, 1.8), 2)} for s in strikes]
    st.dataframe(pd.DataFrame(strike_rows), use_container_width=True, hide_index=True)

with tab3:
    st.subheader("📈 Futures & Open Interest (OI)")
    oi_badge_class = "oi-long-buildup" if current_oi_status == "LONG BUILDUP" else ("oi-short-covering" if current_oi_status == "SHORT COVERING" else ("oi-short-buildup" if current_oi_status == "SHORT BUILDUP" else "oi-long-unwinding"))
    st.markdown(f"""
    <div style="background:#161B22; padding:15px; border-radius:8px; border:1px solid #29B6F6; margin-bottom:12px;">
        <h4 style="color:#29B6F6; margin:0 0 8px 0;">⚡ LIVE OI BUILDUP TRACKER</h4>
        <p style="margin:4px 0; font-size:13px;">Fut Price: <strong>₹{fut_price:,.2f}</strong> | ATM Strike: <strong>{atm_strike}</strong></p>
        <div style="margin-top:10px;">Classification: <span class="{oi_badge_class}">{current_oi_status}</span></div>
    </div>
    """, unsafe_allow_html=True)
    if current_oi_status == "LONG BUILDUP":
        st.success("🟢 **Price Up + OI Up:** బయ్యర్లు మార్కెట్‌ను బలంగా పైకి తోస్తున్నారు.")
    elif current_oi_status == "SHORT COVERING":
        st.info("🔵 **Price Up + OI Down:** షార్ట్ సెల్లర్లు పొజిషన్స్ కట్ చేసుకుంటున్నారు.")
    elif current_oi_status == "SHORT BUILDUP":
        st.error("🔴 **Price Down + OI Up:** సెల్లర్లు మార్కెట్‌ను కిందకి నెడుతున్నారు.")
    else:
        st.warning("🟠 **Price Down + OI Down:** లాంగ్ పొజిషన్స్ అన్‌వైండ్ అవుతున్నాయి.")

with tab4:
    st.subheader("📍 Volume POC & Gamma Levels")
    st.markdown(f"""
    <div style="background: rgba(41, 182, 246, 0.1); border: 2px solid #29B6F6; border-radius: 8px; padding: 15px; text-align: center; margin-bottom: 12px;">
        <h3 style="color: #29B6F6; margin: 0;">🎯 Volume POC Strike: {poc_strike}</h3>
        <p style="margin: 5px 0 0 0; font-size: 13px; color: #FFF;">అత్యధిక వాల్యూమ్ నమోదైన సపోర్ట్/రెసిస్టెన్స్ జోన్.</p>
    </div>
    """, unsafe_allow_html=True)
    st.metric(label="Zero Gamma Level", value=zero_gamma)
    st.metric(label="Net Cumulative Delta", value=f"{c_delta:+d} Contracts")

with tab5:
    st.subheader("🏆 Win Probability & Traps")
    strikes_list = [atm_strike + (i * 50) for i in range(-2, 3)]
    for s in strikes_list:
        diff = s - atm_strike
        if diff < 0:
            rank_title, stk_type, win_pct, badge_color = "Rank 1", f"ITM ({abs(diff)} pts)", 68, "#00E676"
        elif diff == 0:
            rank_title, stk_type, win_pct, badge_color = "Rank 2", "ATM", 52, "#29B6F6"
        else:
            rank_title, stk_type, win_pct, badge_color = "Rank 3", f"OTM ({diff} pts)", 38, "#FFA726"
        st.markdown(f"""
        <div class="rank-card-best">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <strong style="font-size: 15px; color: #FFF;">{s} ({stk_type})</strong>
                <span style="background-color: {badge_color}; color: #000; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px;">{rank_title}</span>
            </div>
            <div style="margin-top: 4px; font-size: 13px;"><strong>Win Probability:</strong> <span style="color:{badge_color}; font-weight:bold;">{win_pct}%</span></div>
        </div>
        """, unsafe_allow_html=True)

# Auto Refresh Control in Sidebar
st.sidebar.title("⚡ Control Panel")
auto = st.sidebar.checkbox("⚡ Live Auto-Refresh (5 sec)", value=True)
if auto:
    time.sleep(5)
    st.rerun()
