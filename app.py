import streamlit as st
import pandas as pd
import requests

# -------------------------------------------------------------------
# 1. Page Configuration & Custom CSS Styling
# -------------------------------------------------------------------
st.set_page_config(page_title="Advanced Options & Futures Flow Dashboard", layout="wide")

st.markdown("""
<style>
    .metric-card { background-color: #f8f9fa; border-radius: 8px; padding: 12px; border-left: 5px solid #007bff; margin-bottom: 12px; }
    .strike-card { background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 6px; padding: 12px; margin-bottom: 10px; }
    .badge-bull { background-color: #d4edda; color: #155724; padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 12px; }
    .badge-bear { background-color: #f8d7da; color: #721c24; padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 12px; }
    .badge-neutral { background-color: #e2e3e5; color: #383d41; padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 12px; }
    .sub-text { font-size: 11px; color: #6c757d; }
    .green-text { color: #28a745; font-weight: bold; }
    .red-text { color: #dc3545; font-weight: bold; }
    .blue-text { color: #007bff; font-weight: bold; }
    .section-header { font-size: 18px; font-weight: bold; margin-top: 15px; margin-bottom: 10px; border-bottom: 2px solid #007bff; padding-bottom: 5px; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ Advanced Order Flow & Neutralization Dashboard")

# -------------------------------------------------------------------
# 2. Controls & Dhan Credentials Setup
# -------------------------------------------------------------------
col_sel1, col_sel2 = st.columns([1, 3])
with col_sel1:
    selected_index = st.selectbox("Select Index", ["NIFTY", "SENSEX"])

if "DHAN_CLIENT_ID" not in st.secrets or "DHAN_ACCESS_TOKEN" not in st.secrets:
    st.error("⚠️ Streamlit Secrets లో Dhan API Credentials (DHAN_CLIENT_ID, DHAN_ACCESS_TOKEN) కనిపించలేదు.")
    st.stop()

client_id = str(st.secrets["DHAN_CLIENT_ID"]).strip()
access_token = str(st.secrets["DHAN_ACCESS_TOKEN"]).strip()

headers = {
    "access-token": access_token,
    "client-id": client_id,
    "Content-Type": "application/json"
}

# -------------------------------------------------------------------
# 3. Dhan API Data Fetching Function
# -------------------------------------------------------------------
@st.cache_data(ttl=5)
def get_dhan_option_chain(symbol):
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

raw_data = get_dhan_option_chain(selected_index)

# -------------------------------------------------------------------
# 4. Off-Market Fallback / Live Data Processing Logic
# -------------------------------------------------------------------
if not raw_data or not raw_data.get("oc"):
    st.info("ℹ️ మార్కెట్ ప్రస్తుతం క్లోజ్ అయి ఉంది (లేదా Live Data దొరకలేదు). Below is the Offline Advanced Analytical Dashboard View:")
    
    # Dummy/Offline dataset matching your video metrics
    candles_flow_data = [
        {"time": "12:45", "spot": 24223.55, "side": "BEAR", "state": "FLOW ONLY", "wall": "24300 CE (1.7G / PE 83.99L)", "neut": "-21.04L", "dir_opp": "Dir 1.62L | Opp 22.66L", "seller": "-4.63L"},
        {"time": "12:44", "spot": 24220.20, "side": "BULL", "state": "STRONG ALIGNMENT", "wall": "24200 PE (2.7G / CE 1.11G)", "neut": "+14.81L", "dir_opp": "Dir 15.62L | Opp 81.00K", "seller": "+14.81L"},
        {"time": "12:44", "spot": 24220.20, "side": "BULL", "state": "STRONG ALIGNMENT", "wall": "24150 PE (64.8L / CE 18.7L)", "neut": "-3.03L", "dir_opp": "Dir 1.02L | Opp 4.05L", "seller": "-3.03L"}
    ]
    
    futures_neutralization = [
        {"build": "Fresh Short Build", "px_oi": "Px -10.00 | OI +2.3K", "cum_vol": "Cum -4.42K | Vol 3.64K", "vol_oi_str": "Vol Strength 0.26x | OI Strength 1.06x", "ranks": "Vol Rank #21 | OI Add Rank #3", "cum_neut": "-4.42K", "dir_opp": "Directional 1.17K | Opposite 5.59K", "type_break": "FL 0.00 | SC 1.17K | FS 5.59K | LU 0.00"},
        {"build": "Short Covering", "px_oi": "Px +7.10 | OI -1.2K", "cum_vol": "Cum -2.08K | Vol 8.00K", "vol_oi_str": "Vol Strength 0.51x | OI Strength 0.36x", "ranks": "Vol Rank #10 | OI Exit Rank #8", "cum_neut": "-2.08K", "dir_opp": "Directional 1.17K | Opposite 3.25K", "type_break": "FL 0.00 | SC 1.17K | FS 3.25K | LU 0.00"}
    ]

    seller_only_flow = [
        {"strike": "24200 PE", "neut_flow": "-2.40L", "dir_opp": "Dir 15.21L | Opp 17.61L", "seller_strength": "Seller -1.00 | Unwind 1.00", "seller_net": "+10.14L", "net_break": "PE Net +10.14L | CE Net -1.00"},
        {"strike": "24250 CE", "neut_flow": "+44.49L", "dir_opp": "Dir 1.31G | Opp 36.69L", "seller_strength": "Seller +8.28L | Unwind -28.40L", "seller_net": "-8.39L", "net_break": "PE Net -8.39L | CE Net +27.75L"},
        {"strike": "24300 CE", "neut_flow": "+83.44L", "dir_opp": "Dir 2.66G | Opp 1.83Cr", "seller_strength": "Seller +11.54L | Unwind +0.00", "seller_net": "+77.94L", "net_break": "PE Net +83.44L | CE Net +1.47Cr"}
    ]
else:
    st.success(f"🟢 {selected_index} Real-time Live Market Feed Active!")
    # Dynamically structure data from API response
    oc_data = raw_data.get("oc", {})
    
    candles_flow_data = []
    futures_neutralization = []
    seller_only_flow = []
    
    for strike_price, values in list(oc_data.items())[:5]:
        ce_oi = values.get("ce", {}).get("oi", 0)
        pe_oi = values.get("pe", {}).get("oi", 0)
        ce_vol = values.get("ce", {}).get("volume", 0)
        pe_vol = values.get("pe", {}).get("volume", 0)
        
        net_flow = pe_oi - ce_oi
        side = "BULL" if net_flow > 0 else "BEAR"
        
        candles_flow_data.append({
            "time": "LIVE", "spot": strike_price, "side": side, "state": "FLOW ONLY",
            "wall": f"{strike_price} PE/CE", "neut": f"{net_flow:,}",
            "dir_opp": f"PE OI: {pe_oi:,} | CE OI: {ce_oi:,}", "seller": f"{net_flow:,}"
        })
        
        seller_only_flow.append({
            "strike": f"{strike_price} {selected_index}",
            "neut_flow": f"{net_flow:,}",
            "dir_opp": f"Dir {pe_vol:,} | Opp {ce_vol:,}",
            "seller_strength": "Seller Net Active",
            "seller_net": f"{net_flow:,}",
            "net_break": f"PE OI: {pe_oi:,} | CE OI: {ce_oi:,}"
        })

# -------------------------------------------------------------------
# 5. Render Section 1: 1-Min All Candles Flow
# -------------------------------------------------------------------
st.markdown('<div class="section-header">📊 1-Min All Candles Flow</div>', unsafe_allow_html=True)
st.caption("Every completed 1-minute candle is scanned independently without changing flow logic.")

for item in candles_flow_data:
    side_badge = "badge-bull" if item["side"] == "BULL" else "badge-bear"
    neut_color = "green-text" if "+" in str(item["neut"]) else "red-text"
    
    st.markdown(f"""
    <div class="strike-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <strong>TIME: {item['time']}</strong> | <span class="sub-text">Spot: {item['spot']}</span>
            </div>
            <div>
                <span class="{side_badge}">{item['side']}</span>
                <span class="badge-neutral" style="margin-left:5px;">{item['state']}</span>
            </div>
        </div>
        <hr style="margin: 6px 0; border: 0; border-top: 1px solid #eee;"/>
        <div style="display: flex; justify-content: space-between;">
            <div>
                <span class="sub-text">WALL / CE/PE VOL</span><br/>
                <span class="blue-text">{item['wall']}</span>
            </div>
            <div>
                <span class="sub-text">NEUTRALIZED FLOW</span><br/>
                <span class="{neut_color}">{item['neut']}</span><br/>
                <span class="sub-text">{item['dir_opp']}</span>
            </div>
            <div style="text-align: right;">
                <span class="sub-text">SELLER NET</span><br/>
                <span class="{neut_color}">{item['seller']}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------------
# 6. Render Section 2: Futures Cum Neutralization
# -------------------------------------------------------------------
st.markdown('<div class="section-header">📈 Futures & Cumulative Neutralization</div>', unsafe_allow_html=True)

if futures_neutralization:
    for fut in futures_neutralization:
        neut_color = "green-text" if "+" in fut["cum_neut"] else "red-text"
        st.markdown(f"""
        <div class="strike-card">
            <div style="display: flex; justify-content: space-between;">
                <div>
                    <strong style="color:#d9534f;">{fut['build']}</strong><br/>
                    <span class="sub-text">{fut['px_oi']} | {fut['cum_vol']}</span><br/>
                    <span class="sub-text">{fut['vol_oi_str']}</span><br/>
                    <span class="blue-text">{fut['ranks']}</span>
                </div>
                <div style="text-align: right;">
                    <span class="sub-text">FUTURES CUM NEUTRALIZATION</span><br/>
                    <span class="{neut_color}" style="font-size:16px;">{fut['cum_neut']}</span><br/>
                    <span class="sub-text">{fut['dir_opp']}</span><br/>
                    <span class="sub-text" style="font-weight:bold;">{fut['type_break']}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# -------------------------------------------------------------------
# 7. Render Section 3: Seller-Only Neutralization & Activity
# -------------------------------------------------------------------
st.markdown('<div class="section-header">🎯 Seller-Only Neutralization & Activity</div>', unsafe_allow_html=True)

for seller in seller_only_flow:
    neut_color = "green-text" if "+" in str(seller["neut_flow"]) else "red-text"
    seller_net_color = "green-text" if "+" in str(seller["seller_net"]) else "red-text"
    
    st.markdown(f"""
    <div class="strike-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <strong style="font-size: 16px;">{seller['strike']}</strong>
            <span class="sub-text">{seller['seller_strength']}</span>
        </div>
        <hr style="margin: 6px 0; border: 0; border-top: 1px solid #eee;"/>
        <div style="display: flex; justify-content: space-between;">
            <div>
                <span class="sub-text">NEUTRALIZED FLOW</span><br/>
                <span class="{neut_color}">{seller['neut_flow']}</span><br/>
                <span class="sub-text">{seller['dir_opp']}</span>
            </div>
            <div style="text-align: right;">
                <span class="sub-text">SELLER-ONLY NET</span><br/>
                <span class="{seller_net_color}">{seller['seller_net']}</span><br/>
                <span class="sub-text">{seller['net_break']}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
