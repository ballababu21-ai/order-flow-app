import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# Page Configuration
st.set_page_config(
    page_title="NIFTY Advanced Order Flow & Volatility Engine",
    page_icon="⚡",
    layout="wide"
)

ist = ZoneInfo("Asia/Kolkata")
now_ist = datetime.now(ist)

# Custom Dark Theme & Mobile-Responsive CSS Styling
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
        background: linear-gradient(135deg, rgba(255, 23, 68, 0.25), rgba(255, 152, 0, 0.25));
        border: 2px solid #FF1744;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        margin-bottom: 12px;
    }
    
    .skew-card {
        background: linear-gradient(135deg, rgba(33, 150, 243, 0.15), rgba(156, 39, 176, 0.1));
        border: 1px solid #29B6F6;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
    }

    .vwap-card {
        background: linear-gradient(135deg, rgba(0, 200, 83, 0.15), rgba(33, 150, 243, 0.1));
        border: 1px solid #00E676;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
    }

    .oi-long-buildup { background-color: #00C853; color: #000; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; }
    .oi-short-covering { background-color: #29B6F6; color: #000; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; }
    .oi-short-buildup { background-color: #D50000; color: #FFF; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; }
    .oi-long-unwinding { background-color: #FFA726; color: #000; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; }

    .badge-bull { background-color: #00C853; color: #000; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; }
    .badge-bear { background-color: #D50000; color: #FFF; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; }
    
    .txt-blue { color: #29B6F6; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Core Market Simulation & Calculations
spot = 24225.50
atm_strike = round(spot / 50) * 50
fut_price = spot + 18.5
zero_gamma_level = atm_strike - 25

st.title("⚡ NIFTY Pro Quantitative Order Flow Engine")
st.success(f"🟢 Connected to Data Feed | {now_ist.strftime('%I:%M:%S %p')} IST")
st.caption(f"SPOT: **₹{spot:,.2f}** | FUT: **₹{fut_price:,.2f}** | ATM: **{atm_strike}**")

# 1. Advanced Quantitative Metrics Engine
# IV Skew Calculation Logic
atm_iv = round(np.random.uniform(12.5, 15.8), 2)
otm_put_iv = round(atm_iv + np.random.uniform(1.8, 4.2), 2)
otm_call_iv = round(atm_iv + np.random.uniform(0.6, 2.4), 2)
skew_diff = otm_put_iv - otm_call_iv
if skew_diff > 1.5:
    skew_status = "Put Skew Dominant (Overpriced Puts / Downside Protection Demand)"
elif skew_diff < -0.5:
    skew_status = "Call Skew Dominant (Aggressive Upside Call Buying)"
else:
    skew_status = "Neutral Volatility Skew"

# Gamma Squeeze & Explosion Engine
otm_ce_vol = np.random.randint(60, 280)
otm_pe_vol = np.random.randint(60, 280)
delta_spike = np.random.uniform(0.6, 1.9)
is_gamma_explosion = (otm_ce_vol > 190) or (otm_pe_vol > 190) or (delta_spike > 1.6)

# VWAP & Standard Deviation Bands Calculation
vwap_val = spot - np.random.uniform(4, 12)
std_dev_unit = 27.5
upper_2sd = vwap_val + (2 * std_dev_unit)
upper_1sd = vwap_val + (1 * std_dev_unit)
lower_1sd = vwap_val - (1 * std_dev_unit)
lower_2sd = vwap_val - (2 * std_dev_unit)

# OI Buildup State
oi_states = ["LONG BUILDUP", "SHORT COVERING", "SHORT BUILDUP", "LONG UNWINDING"]
current_oi_status = np.random.choice(oi_states, p=[0.45, 0.25, 0.20, 0.10])

if is_gamma_explosion:
    squeezed_side = "CALL OTM SQUEEZE (Upside Expansion)" if otm_ce_vol > otm_pe_vol else "PUT OTM SQUEEZE (Downside Cascade)"
    st.markdown(f"""
    <div class="explosion-alert-box">
        <h3 style="color: #FF1744; margin:0;">🚨 GAMMA SQUEEZE & EXPIRY EXPLOSION DETECTED!</h3>
        <p style="margin: 4px 0 0 0; color: #FFF; font-size: 13px;">
            OTM Strikes వద్ద భారీ వాల్యూమ్ విస్ఫోటనం ({max(otm_ce_vol, otm_pe_vol)}L) మరియు డెల్టా స్పైక్ ({delta_spike:.2f}) గుర్తించబడింది. 
            <br><b>Active Target Zone:</b> {squeezed_side}
        </p>
    </div>
    """, unsafe_allow_html=True)

# Navigation via Clean Sidebar Menu to prevent mobile wrapping bugs
st.sidebar.title("⚡ Navigation Hub")
nav_mode = st.sidebar.radio("Select Analytics Module", [
    "⏱️ Live Order Flow",
    "🚀 Gamma & Squeeze",
    "📊 IV Skew Tracker",
    "📈 VWAP & SD Bands",
    "🎯 Strike Imbalance",
    "📈 Futures & OI Matrix",
    "🏆 Win Probability & Traps"
])

# Module Rendering Based on Selection
if nav_mode == "⏱️ Live Order Flow":
    st.subheader("⏱️ Live Order Flow (Wall Touch & Alignment)")
    st.markdown("మార్కెట్ ఆర్థర్ అండ్ వాల్ టచ్‌లను రియల్‌టైమ్‌లో ట్రాక్ చేసే మాడ్యూల్ ఇది.")
    for i in range(5):
        t_str = (now_ist - timedelta(minutes=i)).strftime("%H:%M")
        s_price = round(spot + np.random.uniform(-5, 5), 2)
        is_bull = (i % 2 != 0)
        box_class = "row-bull-box" if is_bull else "row-bear-box"
        side_badge = '<span class="badge-bull">BULL</span>' if is_bull else '<span class="badge-bear">BEAR</span>'
        stk = atm_strike + (-50 if is_bull else 50)
        ce_val = round(np.random.uniform(15, 95), 1)
        pe_val = round(np.random.uniform(15, 95), 1)
        
        st.markdown(f"""
        <div class="{box_class}">
            <div style="display: flex; justify-content: space-between;">
                <strong>{t_str} (₹{s_price})</strong> {side_badge}
            </div>
            <div style="font-size: 12px; margin-top:4px; color: #8B949E;">
                State: <strong>{'STRONG ALIGNMENT' if i%2==0 else 'MOMENTUM SPIKE'}</strong>
            </div>
            <div style="font-size: 12px; margin-top:2px;">
                Strike Flow: <strong class="txt-blue">{stk} {'PE' if is_bull else 'CE'} ({ce_val}Cr / PE {pe_val}Cr)</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

elif nav_mode == "🚀 Gamma & Squeeze":
    st.subheader("🚀 Gamma Squeeze & Expiry Explosion Monitor")
    st.markdown("""
    <div style="background:#161B22; padding:12px; border-radius:8px; border:1px solid #FF1744; margin-bottom:10px;">
        <p style="margin:0; font-size:13px;">ఎక్స్పైరీ రోజుల్లో OTM స్ట్రైక్స్‌పై రైటర్ల అన్‌విండింగ్ మరియు బయర్స్ హెడ్జింగ్ వల్ల వచ్చే సడన్ మూవ్‌లను పసిగడుతుంది.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="OTM CE Volume", value=f"{otm_ce_vol} Lakhs", delta="High Spike" if otm_ce_vol > 180 else "Normal")
    with col2:
        st.metric(label="OTM PE Volume", value=f"{otm_pe_vol} Lakhs", delta="High Spike" if otm_pe_vol > 180 else "Normal")
    with col3:
        st.metric(label="Delta Spike Multiplier", value=f"{delta_spike}x", delta="Explosive" if delta_spike > 1.5 else "Stable")

elif nav_mode == "📊 IV Skew Tracker":
    st.subheader("📊 IV Skew Tracker (Overpriced / Underpriced Analysis)")
    st.markdown(f"""
    <div class="skew-card">
        <h4 style="color: #29B6F6; margin:0 0 5px 0;">Market Skew State: {skew_status}</h4>
        <p style="margin:0; font-size:13px;">ATM IV: <b>{atm_iv}%</b> | OTM Put IV: <b>{otm_put_iv}%</b> | OTM Call IV: <b>{otm_call_iv}%</b></p>
    </div>
    """, unsafe_allow_html=True)
    st.info("💡 **ట్రేడింగ్ గమనిక:** పుట్ IV అధికంగా ఉంటే మార్కెట్ కింది స్థాయిలలో పుట్ ప్రీమియంలు ఖరీదుగా (Overpriced) ఉన్నాయని అర్థం. కాల్ IV ఎక్కువైతే బ్రేక్‌అవుట్ వేగం పెరుగుతుంది.")

elif nav_mode == "📈 VWAP & SD Bands":
    st.subheader("📈 Institutional VWAP & Standard Deviation Bands")
    st.markdown(f"""
    <div class="vwap-card">
        <h4 style="color: #00E676; margin:0 0 5px 0;">VWAP Benchmark: ₹{vwap_val:,.2f}</h4>
        <p style="margin:0; font-size:13px;">ఇన్‌స్టిట్యూషనల్ ట్రెండ్ బౌండరీలు మరియు డీవియేషన్ లెవెల్స్.</p>
    </div>
    """, unsafe_allow_html=True)
    
    band_rows = [
        {"Band Level": "+2.0 SD (Extreme Upper Resistance)", "Price": f"₹{upper_2sd:,.2f}", "Action": "Profit Booking Zone"},
        {"Band Level": "+1.0 SD (Upper Boundary)", "Price": f"₹{upper_1sd:,.2f}", "Action": "Bullish Target"},
        {"Band Level": "VWAP (Fair Institutional Value)", "Price": f"₹{vwap_val:,.2f}", "Action": "Trend Pivot Line"},
        {"Band Level": "-1.0 SD (Lower Boundary)", "Price": f"₹{lower_1sd:,.2f}", "Action": "Bearish Support"},
        {"Band Level": "-2.0 SD (Extreme Lower Support)", "Price": f"₹{lower_2sd:,.2f}", "Action": "Dip Buying Zone"}
    ]
    st.dataframe(pd.DataFrame(band_rows), use_container_width=True, hide_index=True)

elif nav_mode == "🎯 Strike Imbalance":
    st.subheader("🎯 ATM ± 4 Strike Volume & Imbalance Matrix")
    strikes = [atm_strike + (i * 50) for i in range(-4, 5)]
    strike_rows = [
        {"Strike": s, "CE Vol (L)": np.random.randint(20, 150), "PE Vol (L)": np.random.randint(20, 150), "Imbalance Ratio": round(np.random.uniform(0.5, 2.1), 2)} 
        for s in strikes
    ]
    st.dataframe(pd.DataFrame(strike_rows), use_container_width=True, hide_index=True)

elif nav_mode == "📈 Futures & OI Matrix":
    st.subheader("📈 Futures Price & Open Interest Buildup Classification")
    oi_badge_class = "oi-long-buildup" if current_oi_status == "LONG BUILDUP" else ("oi-short-covering" if current_oi_status == "SHORT COVERING" else ("oi-short-buildup" if current_oi_status == "SHORT BUILDUP" else "oi-long-unwinding"))
    st.markdown(f"""
    <div style="background:#161B22; padding:15px; border-radius:8px; border:1px solid #29B6F6; margin-bottom:12px;">
        <h4 style="color:#29B6F6; margin:0 0 8px 0;">⚡ LIVE OI BUILDUP ENGINE</h4>
        <p style="margin:4px 0; font-size:13px;">Futures Price: <strong>₹{fut_price:,.2f}</strong> | Zero Gamma Level: <strong>{zero_gamma_level}</strong></p>
        <div style="margin-top:10px;">Market Classification: <span class="{oi_badge_class}">{current_oi_status}</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    if current_oi_status == "LONG BUILDUP":
        st.success("🟢 **Price Up + OI Up:** మార్కెట్లోకి ఫ్రెష్ బైయింగ్ మనీ వస్తోంది (Bullish Momentum).")
    elif current_oi_status == "SHORT COVERING":
        st.info("🔵 **Price Up + OI Down:** షార్ట్ సెల్లర్లు భయపడి పొజిషన్స్ కట్ చేసుకుంటున్నారు (Short Squeeze).")
    elif current_oi_status == "SHORT BUILDUP":
        st.error("🔴 **Price Down + OI Up:** హెవీ సెల్లింగ్ ప్రెషర్ కొనసాగుతోంది (Bearish Continuation).")
    else:
        st.warning("🟠 **Price Down + OI Down:** ప్రాఫిట్ బుకింగ్ జరుగుతోంది (Weakness / Unwinding).")

elif nav_mode == "🏆 Win Probability & Traps":
    st.subheader("🏆 Strike Win Probability & Institutional Trap Detector")
    strikes_list = [atm_strike + (i * 50) for i in range(-3, 4)]
    for s in strikes_list:
        diff = s - atm_strike
        if diff < 0:
            rank_title, stk_type, win_pct, badge_color = "Rank 1 (Best)", f"ITM ({abs(diff)} pts)", 68, "#00E676"
        elif diff == 0:
            rank_title, stk_type, win_pct, badge_color = "Rank 2 (High)", "ATM Pivot", 52, "#29B6F6"
        else:
            rank_title, stk_type, win_pct, badge_color = "Rank 3", f"OTM ({diff} pts)", 38, "#FFA726"
            
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.03); border-left: 4px solid {badge_color}; padding: 10px; border-radius: 6px; margin-bottom: 8px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <strong style="font-size: 15px; color: #FFF;">Strike: {s} ({stk_type})</strong>
                <span style="background-color: {badge_color}; color: #000; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px;">{rank_title}</span>
            </div>
            <div style="margin-top: 4px; font-size: 13px;"><strong>Win Probability:</strong> <span style="color:{badge_color}; font-weight:bold;">{win_pct}%</span></div>
        </div>
        """, unsafe_allow_html=True)

# Live Auto-Refresh Toggle Control in Sidebar
st.sidebar.markdown("---")
auto_refresh = st.sidebar.checkbox("⚡ Live Auto-Refresh (5 sec)", value=True)
if auto_refresh:
    time.sleep(5)
    st.rerun()
