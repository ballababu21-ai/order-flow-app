import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Live Options Order Flow", layout="wide")

st.markdown("""
<style>
    .metric-card { background-color: #f8f9fa; border-radius: 8px; padding: 12px; border-left: 5px solid #007bff; margin-bottom: 10px; }
    .strike-row { background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 6px; padding: 10px; margin-bottom: 8px; }
    .badge-bull { background-color: #d4edda; color: #155724; padding: 3px 8px; border-radius: 12px; font-weight: bold; font-size: 12px; }
    .badge-bear { background-color: #f8d7da; color: #721c24; padding: 3px 8px; border-radius: 12px; font-weight: bold; font-size: 12px; }
    .sub-text { font-size: 11px; color: #6c757d; }
    .green-text { color: #28a745; font-weight: 600; }
    .red-text { color: #dc3545; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ Real-Time Options Flow & Neutralization")

selected_index = st.selectbox("Select Index", ["NIFTY", "SENSEX"])

if "DHAN_CLIENT_ID" not in st.secrets or "DHAN_ACCESS_TOKEN" not in st.secrets:
    st.error("⚠️ Streamlit Secrets లో Credentials కనపడలేదు.")
    st.stop()

client_id = str(st.secrets["DHAN_CLIENT_ID"]).strip()
access_token = str(st.secrets["DHAN_ACCESS_TOKEN"]).strip()

headers = {
    "access-token": access_token,
    "client-id": client_id,
    "Content-Type": "application/json"
}

@st.cache_data(ttl=5)
def get_live_option_chain(symbol):
    scrip_id = 13 if symbol == "NIFTY" else 51
    exch_seg = "IDX_I" if symbol == "NIFTY" else "BSE_IDX"
    
    url = "https://api.dhan.co/v2/optionchain"
    payload = {
        "UnderlyingScrip": scrip_id,
        "UnderlyingSeg": exch_seg
    }
    
    try:
        res = requests.post(url, json=payload, headers=headers, timeout=5)
        if res.status_code == 200:
            return res.json().get("data", {})
        else:
            return None
    except Exception:
        return None

raw_data = get_live_option_chain(selected_index)

# Fallback Data for Off-market Hours
if not raw_data or not raw_data.get("oc"):
    st.info("ℹ️ మార్కెట్ ప్రస్తుతం క్లోజ్ అయి ఉంది. (Showing Last Snap/Offline Test View)")
    strikes_list = [
        {
            "strike": "24200 PE" if selected_index == "NIFTY" else "81000 PE", 
            "ce_pe_vol": "PE Vol: 6,973,000 | CE Vol: 4,697,000",
            "neut_flow": "+173,000", "dir_opp": "PE OI: 545,000 | CE OI: 373,000",
            "signal": "BULL"
        },
        {
            "strike": "24150 PE" if selected_index == "NIFTY" else "80900 PE", 
            "ce_pe_vol": "PE Vol: 2,588,000 | CE Vol: 861,000",
            "neut_flow": "-72,670", "dir_opp": "PE OI: 94,640 | CE OI: 167,000",
            "signal": "BEAR"
        }
    ]
    overall_sentiment = "BULLISH (OFF-MARKET)"
    total_neut_flow = 100330
else:
    st.success(f"🟢 {selected_index} Live Data Stream Connected!")
    strikes_list = []
    total_neut_flow = 0
    oc_data = raw_data.get("oc", {})
    
    for strike_price, values in oc_data.items():
        ce_oi = values.get("ce", {}).get("oi", 0)
        pe_oi = values.get("pe", {}).get("oi", 0)
        ce_vol = values.get("ce", {}).get("volume", 0)
        pe_vol = values.get("pe", {}).get("volume", 0)
        
        net_flow = pe_oi - ce_oi
        total_neut_flow += net_flow
        signal = "BULL" if net_flow > 0 else "BEAR"
        
        strikes_list.append({
            "strike": f"{strike_price} {selected_index}",
            "ce_pe_vol": f"PE Vol: {pe_vol:,} | CE Vol: {ce_vol:,}",
            "neut_flow": f"{'+' if net_flow > 0 else ''}{net_flow:,}",
            "dir_opp": f"PE OI: {pe_oi:,} | CE OI: {ce_oi:,}",
            "signal": signal
        })
    overall_sentiment = "BULLISH" if total_neut_flow > 0 else "BEARISH"

# Render Sentiment Card
st.markdown(f"""
<div class="metric-card">
    <span class="sub-text">MARKET SENTIMENT SUMMARY</span>
    <h3 style="margin:0;">{overall_sentiment}</h3>
    <span class="badge-bull">NET OI FLOW: {total_neut_flow:,}</span>
</div>
""", unsafe_allow_html=True)

# Render Strike Rows
st.subheader(f"Strike Flow & Neutralization - {selected_index}")
for row in strikes_list[:10]:
    badge_cls = "badge-bull" if row["signal"] == "BULL" else "badge-bear"
    neut_color = "green-text" if "+" in str(row["neut_flow"]) else "red-text"
    
    st.markdown(f"""
    <div class="strike-row">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <strong style="font-size:16px;">{row['strike']}</strong><br/>
                <span class="sub-text">{row['ce_pe_vol']}</span>
            </div>
            <div>
                <span class="{badge_cls}">{row['signal']}</span>
            </div>
        </div>
        <hr style="margin: 6px 0; border: 0; border-top: 1px solid #eee;"/>
        <div style="display: flex; justify-content: space-between;">
            <div>
                <span class="sub-text">NEUTRALIZED FLOW (OI NET)</span><br/>
                <span class="{neut_color}">{row['neut_flow']}</span><br/>
                <span class="sub-text">{row['dir_opp']}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
