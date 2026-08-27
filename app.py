import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Options Order Flow", layout="wide")

st.markdown("""
<style>
    .metric-card { background-color: #f8f9fa; border-radius: 8px; padding: 12px; border-left: 5px solid #28a745; margin-bottom: 10px; }
    .strike-row { background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 6px; padding: 10px; margin-bottom: 8px; }
    .badge-bull { background-color: #d4edda; color: #155724; padding: 3px 8px; border-radius: 12px; font-weight: bold; font-size: 12px; }
    .badge-bear { background-color: #f8d7da; color: #721c24; padding: 3px 8px; border-radius: 12px; font-weight: bold; font-size: 12px; }
    .sub-text { font-size: 11px; color: #6c757d; }
    .green-text { color: #28a745; font-weight: 600; }
    .red-text { color: #dc3545; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ Options Flow & Neutralization Dashboard")

# Dhan API Connection Check
if "DHAN_CLIENT_ID" in st.secrets and "DHAN_ACCESS_TOKEN" in st.secrets:
    client_id = str(st.secrets["DHAN_CLIENT_ID"]).strip()
    access_token = str(st.secrets["DHAN_ACCESS_TOKEN"]).strip()
    
    headers = {
        "access-token": access_token,
        "client-id": client_id,
        "Content-Type": "application/json"
    }
    try:
        res = requests.get("https://api.dhan.co/v2/fundlimits", headers=headers, timeout=5)
        if res.status_code == 200:
            st.success("🟢 Dhan API Connected Successfully!")
        else:
            st.warning(f"⚠️ Dhan API Verification (Status: {res.status_code}). Token అప్‌డేట్ చేయండి.")
    except Exception as e:
        st.error(f"Network Error: {e}")
else:
    st.error("⚠️ Streamlit Secrets లో Credentials యాడ్ చేయలేదు.")

# Dashboard Cards
st.markdown("""
<div class="metric-card">
    <span class="sub-text">MARKET SENTIMENT</span>
    <h3 style="margin:0;">STRONG ALIGNMENT</h3>
    <span class="badge-bull">OVERALL FLOW: BULLISH (+2.45L)</span>
</div>
""", unsafe_allow_html=True)

st.subheader("Real-time Strike Flow")

strikes = [
    {
        "strike": "24200 PE", "ce_pe_vol": "69.73L / CE 46.97L",
        "neut_flow": "+1.73L", "dir_opp": "Dir 5.45L | Opp 3.73L",
        "seller_net": "+4.74L", "net_detail": "PE Net +4.74L | CE Net +0.00",
        "signal": "BULL", "state": "FLOW ONLY"
    },
    {
        "strike": "24150 PE", "ce_pe_vol": "25.88L / CE 8.61L",
        "neut_flow": "-72.67K", "dir_opp": "Dir 94.64K | Opp 1.67L",
        "seller_net": "+94.64K", "net_detail": "PE Net +94.64K | CE Net +0.00",
        "signal": "BEAR", "state": "STRONG ALIGNMENT"
    }
]

for row in strikes:
    badge_cls = "badge-bull" if row["signal"] == "BULL" else "badge-bear"
    neut_color = "green-text" if "+" in row["neut_flow"] else "red-text"
    
    st.markdown(f"""
    <div class="strike-row">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <strong style="font-size:16px;">{row['strike']}</strong><br/>
                <span class="sub-text">{row['ce_pe_vol']}</span>
            </div>
            <div>
                <span class="{badge_cls}">{row['signal']}</span>
                <span class="sub-text" style="margin-left:5px;">{row['state']}</span>
            </div>
        </div>
        <hr style="margin: 6px 0; border: 0; border-top: 1px solid #eee;"/>
        <div style="display: flex; justify-content: space-between;">
            <div>
                <span class="sub-text">NEUTRALIZED FLOW</span><br/>
                <span class="{neut_color}">{row['neut_flow']}</span><br/>
                <span class="sub-text">{row['dir_opp']}</span>
            </div>
            <div style="text-align: right;">
                <span class="sub-text">SELLER NET</span><br/>
                <span class="{neut_color}">{row['seller_net']}</span><br/>
                <span class="sub-text">{row['net_detail']}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
