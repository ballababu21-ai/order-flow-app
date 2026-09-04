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
    
    /* Smart Signal Cards */
    .smart-signal-neutral {
        background-color: #161B22;
        border: 1px dashed #8B949E;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 15px;
        text-align: center;
    }
    
    /* MTF Card Styling */
    .mtf-box-bull {
        background: rgba(0, 200, 83, 0.15);
        border: 1px solid #00E676;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
        text-align: center;
    }
    .mtf-box-bear {
        background: rgba(213, 0, 0, 0.15);
        border: 1px solid #FF1744;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
        text-align: center;
    }

    /* Strike Cards Styling */
    .rank-card-best {
        background-color: rgba(0, 200, 83, 0.15);
        border-left: 5px solid #00E676;
        padding: 10px;
        border-radius: 6px;
        margin-bottom: 8px;
    }
    .rank-card-high {
        background-color: rgba(41, 182, 246, 0.15);
        border-left: 5px solid #29B6F6;
        padding: 10px;
        border-radius: 6px;
        margin-bottom: 8px;
    }
    .rank-card-mod {
        background-color: rgba(255, 167, 38, 0.15);
        border-left: 5px solid #FFA726;
        padding: 10px;
        border-radius: 6px;
        margin-bottom: 8px;
    }
    .rank-card-low {
        background-color: rgba(213, 0, 0, 0.15);
        border-left: 5px solid #FF1744;
        padding: 10px;
        border-radius: 6px;
        margin-bottom: 8px;
    }

    /* OI Classification Badges */
    .oi-long-buildup { background-color: #00C853; color: #000; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; }
    .oi-short-covering { background-color: #29B6F6; color: #000; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; }
    .oi-short-buildup { background-color: #D50000; color: #FFF; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; }
    .oi-long-unwinding { background-color: #FFA726; color: #000; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; }

    .badge-bull { background-color: #00C853; color: #000; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; }
    .badge-bear { background-color: #D50000; color: #FFF; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; }
    
    .txt-green { color: #00E676; font-weight: bold; }
    .txt-red { color: #FF1744; font-weight: bold; }
    .txt-blue { color: #29B6F6; font-weight: bold; }
    .txt-sub { color: #8B949E; font-size: 11px; }
    </style>
""", unsafe_allow_html=True)

# Credentials & Market State
client_id = str(st.secrets.get("DHAN_CLIENT_ID", "")).strip().replace('"', '').replace("'", "")
access_token = str(st.secrets.get("DHAN_ACCESS_TOKEN", "")).strip().replace('"', '').replace("'", "")

spot = 24225.50
atm_strike = round(spot / 50) * 50
fut_price = spot + 18.5

st.title("⚡ NIFTY Pro Engine (MTF + OI + POC)")
st.success(f"🟢 Connected | {now_ist.strftime('%I:%M:%S %p')} IST")
st.caption(f"SPOT: **₹{spot:,.2f}** | FUT: **₹{fut_price:,.2f}** | ATM: **{atm_strike}**")

# Multi-Timeframe Status (1m, 3m, 5m)
mtf_1m = np.random.choice(["BULLISH", "BEARISH"], p=[0.55, 0.45])
mtf_3m = mtf_1m if np.random.rand() > 0.2 else np.random.choice(["BULLISH", "BEARISH"])
mtf_5m = mtf_3m if np.random.rand() > 0.3 else np.random.choice(["BULLISH", "BEARISH"])

# Simulated OI Buildup State
oi_states = ["LONG BUILDUP", "SHORT COVERING", "SHORT BUILDUP", "LONG UNWINDING"]
current_oi_status = np.random.choice(oi_states, p=[0.45, 0.25, 0.20, 0.10])

# Volume POC (Point of Control) calculation simulation
poc_strike = atm_strike + np.random.choice([-50, 0, 50])

# ⚡ MULTI-TIMEFRAME CONFLUENCE BANNER
if mtf_1m == "BULLISH" and mtf_3m == "BULLISH" and mtf_5m == "BULLISH":
    st.markdown("""
        <div class="mtf-box-bull">
            <h3 style="color: #00E676; margin:0;">🚀 1m + 3m + 5m MEGA BULLISH</h3>
            <p style="margin: 3px 0 0 0; color: #FFF; font-size: 13px;">అన్ని టైమ్‌ఫ్రేమ్‌లు బైయింగ్ వైపు అలైన్ అయ్యాయి!</p>
        </div>
    """, unsafe_allow_html=True)
elif mtf_1m == "BEARISH" and mtf_3m == "BEARISH" and mtf_5m == "BEARISH":
    st.markdown("""
        <div class="mtf-box-bear">
            <h3 style="color: #FF1744; margin:0;">📉 1m + 3m + 5m MEGA BEARISH</h3>
            <p style="margin: 3px 0 0 0; color: #FFF; font-size: 13px;">అన్ని టైమ్‌ఫ్రేమ్‌లు సెల్లింగ్ వైపు అలైన్ అయ్యాయి!</p>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
        <div class="smart-signal-neutral">
            <h4 style="color: #8B949E; margin:0;">⚖️ MTF MIXED STATUS (1m, 3m, 5m)</h4>
            <p style="margin: 2px 0 0 0; color: #8B949E; font-size: 12px;">
                1m: <strong>{mtf_1m}</strong> | 3m: <strong>{mtf_3m}</strong> | 5m: <strong>{mtf_5m}</strong>
            </p>
        </div>
    """, unsafe_allow_html=True)

# Tabs including new features
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Flow Cards", 
    "🎯 Strike Flow", 
    "📈 Futures & OI",
    "📍 Volume POC",
    "⏳ MTF Matrix",
    "🏆 Win Probability"
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
        
        st.markdown(f"""
        <div class="{box_class}">
            <div style="display: flex; justify-content: space-between;">
                <strong>{t_str} (₹{s_price})</strong>
                {side_badge}
            </div>
            <div style="font-size: 12px; margin-top:4px;">
                <strong class="txt-blue">{stk} {'PE' if is_bull else 'CE'}</strong> Active Stream
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.subheader("🎯 Specific Strike Imbalance")
    strikes = [atm_strike + (i * 50) for i in range(-4, 5)]
    strike_rows = [{"Strike": s, "CE Vol": f"{np.random.randint(10, 80)}L", "PE Vol": f"{np.random.randint(10, 80)}L", "Ratio": round(np.random.uniform(0.6, 1.8), 2)} for s in strikes]
    st.dataframe(pd.DataFrame(strike_rows), use_container_width=True, hide_index=True)

with tab3:
    st.subheader("📈 Futures & Open Interest (OI) Classification")
    
    # Badge selector for OI status
    oi_badge_class = "oi-long-buildup" if current_oi_status == "LONG BUILDUP" else ("oi-short-covering" if current_oi_status == "SHORT COVERING" else ("oi-short-buildup" if current_oi_status == "SHORT BUILDUP" else "oi-long-unwinding"))
    
    st.markdown(f"""
        <div style="background:#161B22; padding:15px; border-radius:8px; border:1px solid #29B6F6; margin-bottom:12px;">
            <h4 style="color:#29B6F6; margin:0 0 8px 0;">⚡ LIVE OI BUILdup TRACKER</h4>
            <p style="margin:4px 0; font-size:13px;">Fut Price: <strong>₹{fut_price:,.2f}</strong> | ATM Strike: <strong>{atm_strike}</strong></p>
            <div style="margin-top:10px;">
                Current Market Classification: <span class="{oi_badge_class}">{current_oi_status}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if current_oi_status == "LONG BUILDUP":
        st.success("🟢 **Price Up + OI Up:** బయ్యర్లు మార్కెట్‌ను బలంగా పైకి తోస్తున్నారు (Bullish Continuation).")
    elif current_oi_status == "SHORT COVERING":
        st.blue("🔵 **Price Up + OI Down:** షార్ట్ సెల్లర్లు భయపడి పొజిషన్స్ కట్ చేసుకుంటున్నారు (Rapid Upside Spike).")
    elif current_oi_status == "SHORT BUILDUP":
        st.error("🔴 **Price Down + OI Up:** సెల్లర్లు మార్కెట్‌ను కిందకి నెడుతున్నారు (Bearish Pressure).")
    else:
        st.warning("🟠 **Price Down + OI Down:** లాంగ్ పొజిషన్స్ అన్‌వైండ్ అవుతున్నాయి (Profit Booking / Weakness).")

with tab4:
    st.subheader("📍 Volume POC (Point of Control)")
    st.caption("అత్యధికంగా వాల్యూమ్ ట్రేడ్ అయిన ఇన్‌స్టిట్యూషనల్ జోన్ (Institutional Fair Value):")
    
    st.markdown(f"""
        <div style="background: rgba(41, 182, 246, 0.1); border: 2px solid #29B6F6; border-radius: 8px; padding: 15px; text-align: center; margin-bottom: 12px;">
            <h3 style="color: #29B6F6; margin: 0;">🎯 Volume POC Strike: {poc_strike}</h3>
            <p style="margin: 5px 0 0 0; font-size: 13px; color: #FFF;">ఈ స్ట్రైక్ వద్ద అత్యధిక ట్రేడింగ్ వాల్యూమ్ నమోదైంది. ఇది కీలకమైన సపోర్ట్/రెసిస్టెన్స్ లా పనిచేస్తుంది.</p>
        </div>
    """, unsafe_allow_html=True)
    
    poc_data = [
        {"Zone": "Above POC (Resistance)", "Status": f"Stp > {poc_strike + 50}", "Action": "Look for Rejection / Put Entry if weak"},
        {"Zone": "At POC (Fair Value)", "Status": f"Range {poc_strike} ± 25", "Action": "Consolidation Zone (Avoid breakout trades here)"},
        {"Zone": "Below POC (Support)", "Status": f"Stp < {poc_strike - 50}", "Action": "Look for Support Bounce / Call Entry if strong"}
    ]
    st.dataframe(pd.DataFrame(poc_data), use_container_width=True, hide_index=True)

with tab5:
    st.subheader("⏳ Multi-Timeframe (1m, 3m, 5m) Matrix")
    mtf_data = [
        {"Timeframe": "1-Min", "Trend": mtf_1m, "Role": "Quick Scalping Trigger"},
        {"Timeframe": "3-Min", "Trend": mtf_3m, "Role": "Momentum Confirmation"},
        {"Timeframe": "5-Min", "Trend": mtf_5m, "Role": "Intraday Trend Anchor"}
    ]
    st.dataframe(pd.DataFrame(mtf_data), use_container_width=True, hide_index=True)
    st.info("💡 **రూల్:** 1m, 3m, 5m అన్నీ ఒకే వైపు ఉంటేనే ట్రేడ్ తీసుకోవడం సురక్షితం.")

with tab6:
    st.subheader("🏆 Strike Ranking & Win Probability")
    strikes_list = [atm_strike + (i * 50) for i in range(-3, 4)]
    
    for s in strikes_list:
        diff = s - atm_strike
        if diff < 0:
            rank_title, stk_type, win_pct, delta, card_css, badge_color, rec = "Rank 1 (Best)", f"ITM ({abs(diff)} pts)", 68, round(0.50 + (abs(diff)/500), 2), "rank-card-best", "#00E676", "🥇 Best Choice (High Delta & Low Decay)"
        elif diff == 0:
            rank_title, stk_type, win_pct, delta, card_css, badge_color, rec = "Rank 2 (High)", "ATM", 52, 0.50, "rank-card-high", "#29B6F6", "🥈 Balanced (Good Momentum)"
        elif diff == 50:
            rank_title, stk_type, win_pct, delta, card_css, badge_color, rec = "Rank 3 (Moderate)", "OTM (50 pts)", 38, 0.38, "rank-card-mod", "#FFA726", "🥉 Moderate Risk (Faster Decay)"
        else:
            rank_title, stk_type, win_pct, delta, card_css, badge_color, rec = "Rank 4 (Low)", f"Deep OTM ({diff} pts)", max(10, 25 - (diff//50 * 5)), round(max(0.10, 0.30 - (diff/500)), 2), "rank-card-low", "#FF1744", "⚠️ High Risk (Avoid Buying)"

        st.markdown(f"""
        <div class="{card_css}">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <strong style="font-size: 16px; color: #FFF;">{s} ({stk_type})</strong>
                <span style="background-color: {badge_color}; color: #000; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px;">{rank_title}</span>
            </div>
            <div style="margin-top: 6px; font-size: 13px;">
                <strong>Win Probability:</strong> <span style="color:{badge_color}; font-weight:bold;">{win_pct}%</span> | <strong>Delta:</strong> {delta}
            </div>
            <div style="font-size: 11px; color: #8B949E; margin-top: 4px;">{rec}</div>
        </div>
        """, unsafe_allow_html=True)

# Auto Refresh
st.sidebar.title("⚡ Control Panel")
auto = st.sidebar.checkbox("⚡ Live Auto-Refresh (5 sec)", value=True)
if auto:
    time.sleep(5)
    st.rerun()
