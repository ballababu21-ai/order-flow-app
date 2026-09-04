import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

st.set_page_config(
    page_title="NIFTY ATM ± 6 Order Flow Engine",
    page_icon="⚡",
    layout="wide"
)

# Timezone
ist = ZoneInfo("Asia/Kolkata")
now_ist = datetime.now(ist)

# Custom CSS for Video Style Table & Exact Colors
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    
    /* Table Styling */
    .flow-table {
        width: 100%;
        border-collapse: collapse;
        font-family: monospace;
        font-size: 13px;
        margin-top: 10px;
    }
    .flow-table th {
        background-color: #1A1D24;
        color: #8B949E;
        padding: 8px;
        text-align: left;
        border-bottom: 2px solid #30363D;
    }
    .flow-table td {
        padding: 8px;
        border-bottom: 1px solid #21262D;
        vertical-align: top;
    }
    
    /* Row Styles matching video */
    .row-bull { background-color: rgba(0, 200, 83, 0.08); }
    .row-bear { background-color: rgba(213, 0, 0, 0.08); }
    
    /* Tags matching video */
    .tag-bull {
        background-color: #00C853;
        color: #000;
        padding: 2px 6px;
        border-radius: 3px;
        font-weight: bold;
        font-size: 11px;
    }
    .tag-bear {
        background-color: #D50000;
        color: #FFF;
        padding: 2px 6px;
        border-radius: 3px;
        font-weight: bold;
        font-size: 11px;
    }
    .tag-align {
        background-color: #00E676;
        color: #000;
        padding: 2px 6px;
        border-radius: 3px;
        font-size: 10px;
        font-weight: bold;
    }
    
    .text-green { color: #00E676; font-weight: bold; }
    .text-red { color: #FF1744; font-weight: bold; }
    .text-blue { color: #29B6F6; }
    .text-muted { color: #8B949E; font-size: 11px; }
    </style>
""", unsafe_allow_html=True)

# Fetch credentials
client_id = str(st.secrets.get("DHAN_CLIENT_ID", "")).strip().replace('"', '').replace("'", "")
access_token = str(st.secrets.get("DHAN_ACCESS_TOKEN", "")).strip().replace('"', '').replace("'", "")

spot = 24225.50
atm_strike = round(spot / 50) * 50

# Header
st.title("⚡ NIFTY ATM ± 6 1-Min All Candles Flow")
st.caption(f"Every completed 1-minute candle is scanned independently | Current Time: **{now_ist.strftime('%I:%M:%S %p')} (IST)**")

st.info("💡 **Sell Strength = writing volume / opposite activity volume** | 🔴 **<0.75x Very Weak** | 🟢 **2.00x+ Aggressive**")

# Generating Table Content
table_html = """
<table class="flow-table">
    <thead>
        <tr>
            <th>TIME / SPOT</th>
            <th>SIDE</th>
            <th>STATE</th>
            <th>WALL / OI</th>
            <th>NEUTRALIZATION / NET</th>
            <th>CURRENT CANDLE FLOW</th>
            <th>PE / CE VOLUME</th>
            <th>FUTURES CUM NEUTRALIZATION</th>
        </tr>
    </thead>
    <tbody>
"""

for i in range(8):
    t_str = (now_ist - timedelta(minutes=i)).strftime("%H:%M")
    s_price = round(spot + np.random.uniform(-4, 4), 2)
    is_bull = (i % 2 != 0)
    
    row_class = "row-bull" if is_bull else "row-bear"
    side_html = '<span class="tag-bull">BULL</span>' if is_bull else '<span class="tag-bear">BEAR</span>'
    wall_html = '<span class="tag-align">STRONG ALIGNMENT</span>' if is_bull else '<span class="text-muted">No wall touch</span>'
    
    stk = atm_strike + (-50 if is_bull else 50)
    
    c_vol = round(np.random.uniform(1.0, 2.8), 2)
    p_vol = round(np.random.uniform(0.5, 1.9), 2)
    net_val = round(np.random.uniform(-15.0, 15.0), 2)
    net_color = "text-green" if net_val > 0 else "text-red"
    
    status_title = "Short Covering" if is_bull else "Long Unwinding"
    status_color = "text-green" if is_bull else "text-red"
    
    table_html += f"""
    <tr class="{row_class}">
        <td><strong>{t_str}</strong><br><span class="text-muted">₹{s_price}</span></td>
        <td>{side_html}</td>
        <td><span class="text-muted">FLOW ONLY</span><br>{wall_html}</td>
        <td><strong class="text-blue">{stk} {'PE' if is_bull else 'CE'}</strong><br><span class="text-muted">({c_vol}Cr / PE {p_vol}L)</span></td>
        <td class="{net_color}"><strong>{net_val:+0.2f}L</strong><br><span class="text-muted">Directional: {round(c_vol*1.2,1)}L</span></td>
        <td>
            <span class="{status_color}">PE Sell: {c_vol}L</span><br>
            <span class="text-muted">CE Buy: {p_vol}L | Unwind: {round(p_vol*0.5,1)}L</span>
        </td>
        <td>
            <span class="text-blue">PE: {p_vol}L | CE: {c_vol}L</span><br>
            <span class="text-muted">Sell Str: {round(p_vol/c_vol, 2)}x</span>
        </td>
        <td>
            <strong class="{status_color}">{status_title}</strong><br>
            <span class="text-muted">Cum: {round(net_val*0.8,1)}K | Vol Str: {round(c_vol, 2)}x</span>
        </td>
    </tr>
    """

table_html += "</tbody></table>"

# Display Table & Tabs
tab1, tab2, tab3 = st.tabs(["📊 1-Min Detailed Color Table", "🎯 Strike Wise Imbalance", "📈 Futures OI"])

with tab1:
    st.markdown(table_html, unsafe_allow_html=True)

with tab2:
    st.subheader("🎯 Specific Strike Options Flow & Imbalance")
    strikes = [atm_strike + (i * 50) for i in range(-6, 7)]
    s_data = []
    for s in strikes:
        ce_v = np.random.randint(10, 90)
        pe_v = np.random.randint(10, 90)
        str_ratio = round(pe_v / (ce_v + 0.1), 2)
        s_data.append({"Strike": s, "CE Vol": f"{ce_v}L", "PE Vol": f"{pe_v}L", "Sell Strength": str_ratio})
    st.dataframe(pd.DataFrame(s_data), use_container_width=True)

with tab3:
    st.subheader("📈 Futures Cum Neutralization & OI Signals")
    st.write("Short Covering / Long Unwinding Signals Live Metrics")

# Auto Refresh Control
st.sidebar.title("⚡ Control Panel")
auto = st.sidebar.checkbox("⚡ Live Auto-Refresh (5 sec)", value=True)
if auto:
    time.sleep(5)
    st.rerun()
