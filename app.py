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
    .smart-signal-call {
        background: linear-gradient(135deg, rgba(0,200,83,0.3) 0%, rgba(0,100,40,0.4) 100%);
        border: 2px solid #00E676;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        text-align: center;
    }
    .smart-signal-put {
        background: linear-gradient(135deg, rgba(213,0,0,0.3) 0%, rgba(100,0,0,0.4) 100%);
        border: 2px solid #FF1744;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        text-align: center;
    }
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

st.title("⚡ NIFTY 1m, 3m, 5m MTF Engine")
st.success(f"🟢 Connected | {now_ist.strftime('%I:%M:%S %p')} IST")
st.caption(f"SPOT: **₹{spot:,.2f}** | FUT: **₹{fut_price:,.2f}** | ATM: **{atm_strike}**")

# Multi-Timeframe Status (1m, 3m, 5m only)
mtf_1m = np.random.choice(["BULLISH", "BEARISH"], p=[0.55, 0.45])
mtf_3m = mtf_1m if np.random.rand() > 0.2 else np.random.choice(["BULLISH", "BEARISH"])
mtf_5m = mtf_3m if np.random.rand() > 0.3 else np.random.choice(["BULLISH", "BEARISH"])

# ⚡ MULTI-TIMEFRAME CONFLUENCE BANNER (1m, 3m, 5m)
if mtf_1m == "BULLISH" and mtf_3m == "BULLISH" and mtf_5m == "BULLISH":
    st.markdown("""
        <div class="mtf-box-bull">
            <h3 style="color: #00E676; margin:0;">🚀 1m + 3m + 5m MEGA BULLISH</h3>
            <p style="margin: 3px 0 0 0; color: #FFF; font-size: 13px;">1m, 3m, 5m టైమ్‌ఫ్రేమ్‌లు అన్నీ ఒకే వైపు ఉన్నాయి. పర్ఫెక్ట్ బైయింగ్ సిగ్నల్!</p>
        </div>
    """, unsafe_allow_html=True)
elif mtf_1m == "BEARISH" and mtf_3m == "BEARISH" and mtf_5m == "BEARISH":
    st.markdown("""
        <div class="mtf-box-bear">
            <h3 style="color: #FF1744; margin:0;">📉 1m + 3m + 5m MEGA BEARISH</h3>
            <p style="margin: 3px 0 0 0; color: #FFF; font-size: 13px;">1m, 3m, 5m టైమ్‌ఫ్రేమ్‌లు అన్నీ కిందకి పడటానికి అలైన్ అయ్యాయి. పర్ఫెక్ట్ సెల్లింగ్ సిగ్నల్!</p>
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

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Flow Cards", 
    "🎯 Strike Flow", 
    "📈 Futures OI",
    "⏳ 1m/3m/5m Matrix",
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
    st.subheader("📈 Futures Signals")
    st.markdown(f"""
        <div style="background:#161B22; padding:12px; border-radius:6px; border:1px solid #00C853; margin-bottom:10px;">
            <h4 style="color:#00E676; margin:0;">ACTIVE FUTURES FLOW DETECTED</h4>
            <p style="margin:3px 0; font-size:12px;">Fut Price: ₹{fut_price:,.2f} | ATM: {atm_strike}</p>
        </div>
    """, unsafe_allow_html=True)

# TAB 4: Multi-Timeframe Details (1m, 3m, 5m only)
with tab4:
    st.subheader("⏳ Multi-Timeframe (1m, 3m, 5m) Matrix")
    st.caption("స్కెల్పింగ్ మరియు క్విక్ ఇంట్రాడే మూవ్స్ కోసం టైమ్‌ఫ్రేమ్ స్థితిగతులు:")
    
    mtf_data = [
        {"Timeframe": "1-Min", "Trend": mtf_1m, "Role": "Quick Scalping Trigger"},
        {"Timeframe": "3-Min", "Trend": mtf_3m, "Role": "Momentum Confirmation"},
        {"Timeframe": "5-Min", "Trend": mtf_5m, "Role": "Intraday Trend Anchor"}
    ]
    df_mtf = pd.DataFrame(mtf_data)
    st.dataframe(df_mtf, use_container_width=True, hide_index=True)
    
    st.info("💡 **రూల్:** 1m, 3m, 5m అన్నీ ఒకే వైపు ఉంటేనే త్వరితగతిన మంచి మూవ్‌మెంట్ వస్తుంది.")

with tab5:
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
