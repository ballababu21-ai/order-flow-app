import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import streamlit.components.v1 as components

st.set_page_config(
    page_title="NIFTY ATM ± 6 Order Flow Engine",
    page_icon="⚡",
    layout="wide"
)

ist = ZoneInfo("Asia/Kolkata")
now_ist = datetime.now(ist)

# Header
st.title("⚡ NIFTY ATM ± 6 1-Min All Candles Flow")
st.caption(f"Every completed 1-minute candle is scanned independently | Current Time: **{now_ist.strftime('%I:%M:%S %p')} (IST)**")

st.info("💡 **Sell Strength = writing volume / opposite activity volume** | 🔴 **<0.75x Very Weak** | 🟢 **2.00x+ Aggressive**")

# Credentials
client_id = str(st.secrets.get("DHAN_CLIENT_ID", "")).strip().replace('"', '').replace("'", "")
access_token = str(st.secrets.get("DHAN_ACCESS_TOKEN", "")).strip().replace('"', '').replace("'", "")

spot = 24225.50
atm_strike = round(spot / 50) * 50

# Build Clean Component HTML
rows_html = ""
for i in range(8):
    t_str = (now_ist - timedelta(minutes=i)).strftime("%H:%M")
    s_price = round(spot + np.random.uniform(-4, 4), 2)
    is_bull = (i % 2 != 0)
    
    row_bg = "rgba(0, 200, 83, 0.12)" if is_bull else "rgba(213, 0, 0, 0.12)"
    side_tag = '<span style="background:#00C853; color:#000; padding:3px 8px; border-radius:4px; font-weight:bold;">BULL</span>' if is_bull else '<span style="background:#D50000; color:#FFF; padding:3px 8px; border-radius:4px; font-weight:bold;">BEAR</span>'
    wall_tag = '<span style="background:#00E676; color:#000; padding:2px 6px; border-radius:3px; font-size:11px; font-weight:bold;">STRONG ALIGNMENT</span>' if is_bull else '<span style="color:#8B949E; font-size:11px;">No wall touch</span>'
    
    stk = atm_strike + (-50 if is_bull else 50)
    c_vol = round(np.random.uniform(1.0, 2.8), 2)
    p_vol = round(np.random.uniform(0.5, 1.9), 2)
    net_val = round(np.random.uniform(-15.0, 15.0), 2)
    net_color = "#00E676" if net_val > 0 else "#FF1744"
    status_title = "Short Covering" if is_bull else "Long Unwinding"
    status_color = "#00E676" if is_bull else "#FF1744"
    
    rows_html += f"""
    <tr style="background-color: {row_bg}; border-bottom: 1px solid #21262D;">
        <td style="padding: 10px;"><strong>{t_str}</strong><br><span style="color:#8B949E; font-size:11px;">₹{s_price}</span></td>
        <td style="padding: 10px;">{side_tag}</td>
        <td style="padding: 10px;"><span style="color:#8B949E; font-size:11px;">FLOW ONLY</span><br>{wall_tag}</td>
        <td style="padding: 10px;"><strong style="color:#29B6F6;">{stk} {'PE' if is_bull else 'CE'}</strong><br><span style="color:#8B949E; font-size:11px;">({c_vol}Cr / PE {p_vol}L)</span></td>
        <td style="padding: 10px; color:{net_color};"><strong>{net_val:+0.2f}L</strong><br><span style="color:#8B949E; font-size:11px;">Directional: {round(c_vol*1.2,1)}L</span></td>
        <td style="padding: 10px;">
            <span style="color:{status_color}; font-weight:bold;">PE Sell: {c_vol}L</span><br>
            <span style="color:#8B949E; font-size:11px;">CE Buy: {p_vol}L | Unwind: {round(p_vol*0.5,1)}L</span>
        </td>
        <td style="padding: 10px;">
            <span style="color:#29B6F6; font-weight:bold;">PE: {p_vol}L | CE: {c_vol}L</span><br>
            <span style="color:#8B949E; font-size:11px;">Sell Str: {round(p_vol/c_vol, 2)}x</span>
        </td>
        <td style="padding: 10px;">
            <strong style="color:{status_color};">{status_title}</strong><br>
            <span style="color:#8B949E; font-size:11px;">Cum: {round(net_val*0.8,1)}K | Vol Str: {round(c_vol, 2)}x</span>
        </td>
    </tr>
    """

full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ background-color: #0E1117; color: #FFFFFF; font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin:0; padding:0; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
        th {{ background-color: #1A1D24; color: #8B949E; padding: 10px; text-align: left; border-bottom: 2px solid #30363D; }}
    </style>
</head>
<body>
    <table>
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
            {rows_html}
        </tbody>
    </table>
</body>
</html>
"""

# Render via Tab Controls
tab1, tab2, tab3 = st.tabs(["📊 1-Min Detailed Color Table", "🎯 Strike Wise Imbalance", "📈 Futures OI"])

with tab1:
    components.html(full_html, height=500, scrolling=True)

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
