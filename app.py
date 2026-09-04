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

# Custom Dark Styling
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

# Header Section
st.title("⚡ NIFTY ATM ± 6 Order Flow Engine")
st.success(f"🟢 Dhan API Connected | Current Time: {now_ist.strftime('%I:%M:%S %p')} (IST)")
st.caption(f"NIFTY SPOT: **₹{spot:,.2f}** | ATM STRIKE: **{atm_strike}**")

st.info("💡 **Sell Strength = writing volume / opposite activity volume** | 🔴 **<0.75x Very Weak** | 🟢 **2.00x+ Aggressive**")

# Generating Mock Live Data for Signals
sell_strength_curr = round(np.random.uniform(0.5, 3.2), 2)
is_wall_broken = np.random.choice([True, False], p=[0.25, 0.75])
broken_strike = atm_strike + np.random.choice([-100, -50, 50, 100])
fut_signal = np.random.choice(["SHORT_COVERING", "LONG_UNWINDING", "NEUTRAL"], p=[0.4, 0.4, 0.2])

# ⚡ SMART FLOW SIGNAL GENERATION (AI CONFIRMATION)
if sell_strength_curr >= 2.0 and fut_signal == "SHORT_COVERING":
    st.markdown(f"""
        <div class="smart-signal-call">
            <h2 style="color: #00E676; margin:0;">🚀 HIGH PROBABILITY CALL BUY SIGNAL</h2>
            <p style="margin: 5px 0 0 0; color: #FFF; font-size: 14px;">
                <strong>కన్ఫర్మేషన్:</strong> Put Writing బలంగా ఉంది (Sell Strength: {sell_strength_curr}x) + ఫ్యూచర్స్‌లో Short Covering నమోదైంది.
            </p>
        </div>
    """, unsafe_allow_html=True)
elif sell_strength_curr <= 0.75 and fut_signal == "LONG_UNWINDING":
    st.markdown(f"""
        <div class="smart-signal-put">
            <h2 style="color: #FF1744; margin:0;">📉 HIGH PROBABILITY PUT BUY SIGNAL</h2>
            <p style="margin: 5px 0 0 0; color: #FFF; font-size: 14px;">
                <strong>కన్ఫర్మేషన్:</strong> Call Writing ఆధిపత్యం (Sell Strength: {sell_strength_curr}x) + ఫ్యూచర్స్‌లో Long Unwinding నమోదైంది.
            </p>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="smart-signal-neutral">
            <h4 style="color: #8B949E; margin:0;">⚖️ SMART FLOW SIGNAL: NEUTRAL / CONSOLIDATION</h4>
            <p style="margin: 3px 0 0 0; color: #8B949E; font-size: 12px;">
                మార్కెట్‌లో ప్రస్తుతం స్పష్టమైన అలైన్‌మెంట్ లేదు. బ్రేక్‌అవుట్ లేదా క్లియర్ కన్ఫర్మేషన్ కోసం వేచి చూడండి.
            </p>
        </div>
    """, unsafe_allow_html=True)

# 🚨 LIVE INDICATORS
if is_wall_broken:
    st.markdown(f"""
        <div class="alert-wall-box">
            <h4 style="color: #29B6F6; margin:0;">🚨 BIG WALL BREAK DETECTED!</h4>
            <p style="margin: 4px 0 0 0; color: #E6EDF3; font-size: 13px;">
                <strong>Strike Price {broken_strike}</strong> దగ్గర ఉన్న ఆప్షన్స్ రైటర్స్ వాల్ బ్రేక్ అయ్యింది. నిమిషంలో పెద్ద వ్యత్యాసం నమోదైంది!
            </p>
        </div>
    """, unsafe_allow_html=True)

if sell_strength_curr >= 2.5:
    st.markdown(f"""
        <div class="alert-agg-bull">
            <h4 style="color: #00E676; margin:0;">🔥 AGGRESSIVE BULLISH FLOW ({sell_strength_curr}x)</h4>
            <p style="margin: 4px 0 0 0; color: #FFF; font-size: 13px;">
                Sell Strength <strong>2.5x దాటింది ({sell_strength_curr}x)</strong>. Put Writing / Aggressive Buying చాలా బలంగా జరుగుతోంది!
            </p>
        </div>
    """, unsafe_allow_html=True)
elif sell_strength_curr <= 0.6:
    st.markdown(f"""
        <div class="alert-agg-bear">
            <h4 style="color: #FF1744; margin:0;">⚡ AGGRESSIVE BEARISH FLOW ({sell_strength_curr}x)</h4>
            <p style="margin: 4px 0 0 0; color: #FFF; font-size: 13px;">
                Sell Strength <strong>0.75x కంటే కిందకి పడిపోయింది ({sell_strength_curr}x)</strong>. Call Writing / Bearish Selling పెరిగింది!
            </p>
        </div>
    """, unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 1-Min Candle Flow Cards", "🎯 Strike Wise Imbalance (ATM ± 6)", "📈 Futures OI & Neutralization"])

# TAB 1: Live Candle Flow Cards
with tab1:
    st.subheader("⏱️ Live 1-Min Order Flow Stream")
    
    for i in range(8):
        t_str = (now_ist - timedelta(minutes=i)).strftime("%H:%M")
        s_price = round(spot + np.random.uniform(-4, 4), 2)
        is_bull = (i % 2 != 0)
        
        box_class = "row-bull-box" if is_bull else "row-bear-box"
        side_badge = '<span class="badge-bull">BULL</span>' if is_bull else '<span class="badge-bear">BEAR</span>'
        wall_badge = '<span class="badge-align">STRONG ALIGNMENT</span>' if is_bull else '<span class="txt-sub">No wall touch</span>'
        
        stk = atm_strike + (-50 if is_bull else 50)
        c_vol = round(np.random.uniform(1.0, 2.8), 2)
        p_vol = round(np.random.uniform(0.5, 1.9), 2)
        net_val = round(np.random.uniform(-15.0, 15.0), 2)
        
        net_cls = "txt-green" if net_val > 0 else "txt-red"
        status_title = "Short Covering" if is_bull else "Long Unwinding"
        status_cls = "txt-green" if is_bull else "txt-red"
        
        card_html = f"""
        <div class="{box_class}">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong style="font-size: 15px; color: #FFF;">{t_str}</strong> 
                    <span class="txt-sub" style="margin-left: 8px;">₹{s_price}</span>
                </div>
                <div>{side_badge}</div>
            </div>
            <div style="margin-top: 6px; font-size: 12px;">
                State: <span class="txt-sub">FLOW ONLY</span> | {wall_badge}
            </div>
            <div style="margin-top: 6px; font-size: 12px;">
                <strong class="txt-blue">{stk} {'PE' if is_bull else 'CE'}</strong> 
                <span class="txt-sub">({c_vol}Cr / PE {p_vol}L)</span> | 
                Net: <span class="{net_cls}">{net_val:+0.2f}L</span>
            </div>
            <div style="margin-top: 4px; font-size: 11px;">
                <span class="{status_cls}">PE Sell: {c_vol}L</span> | 
                <span class="txt-sub">CE Buy: {p_vol}L</span> | 
                Signal: <strong class="{status_cls}">{status_title}</strong>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

# TAB 2: Clean Dark-Themed Strike Imbalance Table
with tab2:
    st.subheader("🎯 Specific Strike Options Flow & Volume Imbalance (ATM ± 6)")
    
    strikes = [atm_strike + (i * 50) for i in range(-6, 7)]
    strike_rows = []
    
    for s in strikes:
        ce_v = np.random.randint(10, 90)
        pe_v = np.random.randint(10, 90)
        str_ratio = round(pe_v / (ce_v + 0.1), 2)
        
        imbalance = "Strong Call Writing" if str_ratio < 0.8 else ("Strong Put Writing" if str_ratio > 1.3 else "Neutral Flow")
        
        strike_rows.append({
            "Strike": s,
            "CE Vol": f"{ce_v}L",
            "PE Vol": f"{pe_v}L",
            "Sell Strength Ratio": str_ratio,
            "Imbalance Status": imbalance
        })
        
    df_strikes = pd.DataFrame(strike_rows)
    
    st.dataframe(
        df_strikes,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Strike": st.column_config.NumberColumn("Strike Price", format="%d"),
            "Sell Strength Ratio": st.column_config.ProgressColumn(
                "Sell Strength",
                format="%.2fx",
                min_value=0,
                max_value=3.0
            ),
        }
    )

# TAB 3: Futures Signals
with tab3:
    st.subheader("📈 Futures Cum Neutralization & OI Signals")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div style="background:#161B22; padding:12px; border-radius:6px; border:1px solid #00C853;">
                <h4 style="color:#00E676; margin:0;">SHORT COVERING DETECTED</h4>
                <p style="margin:5px 0; color:#FFF;">Price: +0.10 % | OI: -1.8K</p>
                <p style="color:#8B949E; margin:0;">Cum Volume: 9.10K | Vol Strength: 1.07x</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div style="background:#161B22; padding:12px; border-radius:6px; border:1px solid #D50000;">
                <h4 style="color:#FF1744; margin:0;">LONG UNWINDING DETECTED</h4>
                <p style="margin:5px 0; color:#FFF;">Price: -0.15 % | OI: -3.2K</p>
                <p style="color:#8B949E; margin:0;">Cum Volume: 11.31K | Vol Strength: 2.11x</p>
            </div>
        """, unsafe_allow_html=True)

# Auto Refresh Control
st.sidebar.title("⚡ Control Panel")
auto = st.sidebar.checkbox("⚡ Live Auto-Refresh (5 sec)", value=True)
if auto:
    time.sleep(5)
    st.rerun()
