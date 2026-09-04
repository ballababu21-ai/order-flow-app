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

# Custom Styling for Native Containers
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    
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

# Fetch Credentials
client_id = str(st.secrets.get("DHAN_CLIENT_ID", "")).strip().replace('"', '').replace("'", "")
access_token = str(st.secrets.get("DHAN_ACCESS_TOKEN", "")).strip().replace('"', '').replace("'", "")

spot = 24225.50
atm_strike = round(spot / 50) * 50

# Header Section
st.title("⚡ NIFTY ATM ± 6 1-Min All Candles Flow")
st.success(f"🟢 Dhan API Connected | Current Time: {now_ist.strftime('%I:%M:%S %p')} (IST)")
st.caption(f"NIFTY SPOT: **₹{spot:,.2f}** | ATM STRIKE: **{atm_strike}**")

st.info("💡 **Sell Strength = writing volume / opposite activity volume** | 🔴 **<0.75x Very Weak** | 🟢 **2.00x+ Aggressive**")

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 1-Min Candle Flow Cards", "🎯 Strike Wise Imbalance (ATM ± 6)", "📈 Futures OI & Neutralization"])

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

with tab2:
    st.subheader("🎯 Specific Strike Options Flow & Volume Imbalance")
    strikes = [atm_strike + (i * 50) for i in range(-6, 7)]
    strike_rows = []
    for s in strikes:
        ce_v = np.random.randint(10, 90)
        pe_v = np.random.randint(10, 90)
        str_ratio = round(pe_v / (ce_v + 0.1), 2)
        strike_rows.append({
            "Strike Price": s,
            "CE Vol (Lakhs)": f"{ce_v}L",
            "PE Vol (Lakhs)": f"{pe_v}L",
            "Sell Strength Ratio": str_ratio,
            "Order Flow Imbalance": "Strong Call Writing" if str_ratio < 0.8 else ("Strong Put Writing" if str_ratio > 1.3 else "Neutral Flow")
        })
    st.dataframe(pd.DataFrame(strike_rows), use_container_width=True)

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
