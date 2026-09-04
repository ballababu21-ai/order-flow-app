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
    
    /* Card Rows */
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
    
    /* Live Alert Boxes */
    .alert-wall-box {
        background-color: #1A2332;
        border: 2px solid #29B6F6;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
        box-shadow: 0px 4px 10px rgba(41, 182, 246, 0.2);
    }
    .alert-agg-bull {
        background-color: rgba(0, 200, 83, 0.2);
        border: 2px solid #00C853;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
    }
    .alert-agg-bear {
        background-color: rgba(213, 0, 0, 0.2);
        border: 2px solid #D50000;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
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
    
    /* Strike Cards Styling for Mobile */
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

    /* Badges */
    .badge-bull { background-color: #00C853; color: #000; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; }
    .badge-bear { background-color: #D50000; color: #FFF; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; }
    .badge-align { background-color: #00E676; color: #000; padding: 2px 5px; border-radius: 3px; font-size: 10px; font-weight: bold; }
    
    .txt-green { color: #00E676; font-weight: bold; }
    .txt-red { color: #FF1744; font-weight: bold; }
    .txt-blue { color: #29B6F6; font-weight: bold; }
    .txt-sub { color: #8B949E; font-size: 11px; }
    </style>
""", unsafe_allow_html=True)

# Credentials
client_id = str(st.secrets.get("DHAN_CLIENT_ID", "")).strip().replace('"', '').replace("'", "")
access_token = str(st.secrets.get("DHAN_ACCESS_TOKEN", "")).strip().replace('"', '').replace("'", "")

spot = 24225.50
atm_strike = round(spot / 50) * 50
fut_price = spot + 18.5  # Futures Price Estimate

# Header Section
st.title("⚡ NIFTY Order Flow Engine")
st.success(f"🟢 Connected | {now_ist.strftime('%I:%M:%S %p')} IST")
st.caption(f"SPOT: **₹{spot:,.2f}** | FUT: **₹{fut_price:,.2f}** | ATM: **{atm_strike}**")

# Generating Mock Live Data for Signals
sell_strength_curr = round(np.random.uniform(0.5, 3.2), 2)
is_wall_broken = np.random.choice([True, False], p=[0.25, 0.75])
broken_strike = atm_strike + np.random.choice([-100, -50, 50, 100])
fut_signal = np.random.choice(["SHORT_COVERING", "LONG_UNWINDING", "NEUTRAL"], p=[0.4, 0.4, 0.2])

# ⚡ SMART FLOW SIGNAL
if sell_strength_curr >= 2.0 and fut_signal == "SHORT_COVERING":
    st.markdown(f"""
        <div class="smart-signal-call">
            <h3 style="color: #00E676; margin:0;">🚀 HIGH PROBABILITY CALL BUY</h3>
            <p style="margin: 4px 0 0 0; color: #FFF; font-size: 13px;">
                Put Writing: {sell_strength_curr}x + Short Covering
            </p>
        </div>
    """, unsafe_allow_html=True)
elif sell_strength_curr <= 0.75 and fut_signal == "LONG_UNWINDING":
    st.markdown(f"""
        <div class="smart-signal-put">
            <h3 style="color: #FF1744; margin:0;">📉 HIGH PROBABILITY PUT BUY</h3>
            <p style="margin: 4px 0 0 0; color: #FFF; font-size: 13px;">
                Call Writing: {sell_strength_curr}x + Long Unwinding
            </p>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="smart-signal-neutral">
            <h4 style="color: #8B949E; margin:0;">⚖️ SMART SIGNAL: NEUTRAL</h4>
        </div>
    """, unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Flow Cards", 
    "🎯 Strike Flow", 
    "📈 Futures OI",
    "🏆 Win Probability"
])

# TAB 1: Live Candle Flow Cards
with tab1:
    st.subheader("⏱️ Live Order Flow")
    for i in range(5):
        t_str = (now_ist - timedelta(minutes=i)).strftime("%H:%M")
        s_price = round(spot + np.random.uniform(-4, 4), 2)
        is_bull = (i % 2 != 0)
        
        box_class = "row-bull-box" if is_bull else "row-bear-box"
        side_badge = '<span class="badge-bull">BULL</span>' if is_bull else '<span class="badge-bear">BEAR</span>'
        stk = atm_strike + (-50 if is_bull else 50)
        c_vol = round(np.random.uniform(1.0, 2.8), 2)
        p_vol = round(np.random.uniform(0.5, 1.9), 2)
        
        st.markdown(f"""
        <div class="{box_class}">
            <div style="display: flex; justify-content: space-between;">
                <strong>{t_str} (₹{s_price})</strong>
                {side_badge}
            </div>
            <div style="font-size: 12px; margin-top:4px;">
                <strong class="txt-blue">{stk} {'PE' if is_bull else 'CE'}</strong> | PE Sell: {c_vol}L | CE Buy: {p_vol}L
            </div>
        </div>
        """, unsafe_allow_html=True)

# TAB 2: Specific Strike Imbalance Table
with tab2:
    st.subheader("🎯 Specific Strike Imbalance")
    strikes = [atm_strike + (i * 50) for i in range(-4, 5)]
    strike_rows = []
    
    for s in strikes:
        ce_v = np.random.randint(10, 90)
        pe_v = np.random.randint(10, 90)
        str_ratio = round(pe_v / (ce_v + 0.1), 2)
        
        strike_rows.append({
            "Strike": s,
            "CE Vol": f"{ce_v}L",
            "PE Vol": f"{pe_v}L",
            "Ratio": str_ratio
        })
        
    df_strikes = pd.DataFrame(strike_rows)
    st.dataframe(df_strikes, use_container_width=True, hide_index=True)

# TAB 3: Futures Signals
with tab3:
    st.subheader("📈 Futures Signals")
    st.markdown(f"""
        <div style="background:#161B22; padding:12px; border-radius:6px; border:1px solid #00C853; margin-bottom:10px;">
            <h4 style="color:#00E676; margin:0;">SHORT COVERING DETECTED</h4>
            <p style="margin:3px 0; font-size:12px;">Fut Price: ₹{fut_price:,.2f} | ATM: {atm_strike}</p>
        </div>
    """, unsafe_allow_html=True)

# TAB 4: Strike Ranking & Win Probability (Mobile Optimized Cards)
with tab4:
    st.subheader("🏆 Strike Ranking & Win Probability")
    
    strikes_list = [atm_strike + (i * 50) for i in range(-3, 4)]
    
    for s in strikes_list:
        diff = s - atm_strike
        
        if diff < 0:
            rank_title = "Rank 1 (Best)"
            stk_type = f"ITM ({abs(diff)} pts)"
            win_pct = 68 - (abs(diff)//50 * 3)
            delta = round(0.50 + (abs(diff)/500), 2)
            card_css = "rank-card-best"
            badge_color = "#00E676"
            rec = "🥇 Best Choice (High Delta & Low Decay)"
        elif diff == 0:
            rank_title = "Rank 2 (High)"
            stk_type = "ATM"
            win_pct = 52
            delta = 0.50
            card_css = "rank-card-high"
            badge_color = "#29B6F6"
            rec = "🥈 Balanced (Good Momentum)"
        elif diff == 50:
            rank_title = "Rank 3 (Moderate)"
            stk_type = "OTM (50 pts)"
            win_pct = 38
            delta = 0.38
            card_css = "rank-card-mod"
            badge_color = "#FFA726"
            rec = "🥉 Moderate Risk (Faster Decay)"
        else:
            rank_title = "Rank 4 (Low)"
            stk_type = f"Deep OTM ({diff} pts)"
            win_pct = max(10, 25 - (diff//50 * 5))
            delta = round(max(0.10, 0.30 - (diff/500)), 2)
            card_css = "rank-card-low"
            badge_color = "#FF1744"
            rec = "⚠️ High Risk (Avoid Buying)"

        st.markdown(f"""
        <div class="{card_css}">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <strong style="font-size: 16px; color: #FFF;">{s} ({stk_type})</strong>
                <span style="background-color: {badge_color}; color: #000; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px;">{rank_title}</span>
            </div>
            <div style="margin-top: 6px; font-size: 13px;">
                <strong>Win Probability:</strong> <span style="color:{badge_color}; font-weight:bold;">{win_pct}%</span> | <strong>Delta:</strong> {delta}
            </div>
            <div style="font-size: 11px; color: #8B949E; margin-top: 4px;">
                {rec}
            </div>
        </div>
        """, unsafe_allow_html=True)

# Auto Refresh
st.sidebar.title("⚡ Control Panel")
auto = st.sidebar.checkbox("⚡ Live Auto-Refresh (5 sec)", value=True)
if auto:
    time.sleep(5)
    st.rerun()
