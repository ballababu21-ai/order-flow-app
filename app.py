import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime

st.set_page_config(
    page_title="Live NIFTY Order Flow & Imbalance",
    page_icon="⚡",
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .flow-card {
        background-color: #11141C;
        border-radius: 8px;
        padding: 12px;
        border: 1px solid #1E222D;
        margin-bottom: 8px;
    }
    .tag-bull { background-color: #00C853; color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; }
    .tag-bear { background-color: #D50000; color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; }
    .tag-align { background-color: #1E88E5; color: white; padding: 3px 8px; border-radius: 4px; font-size: 11px; }
    </style>
""", unsafe_allow_html=True)

# Fetch Credentials from Streamlit Secrets
client_id = str(st.secrets.get("DHAN_CLIENT_ID", "")).strip().replace('"', '').replace("'", "")
access_token = str(st.secrets.get("DHAN_ACCESS_TOKEN", "")).strip().replace('"', '').replace("'", "")

headers = {
    "access-token": access_token,
    "client-id": client_id,
    "Content-Type": "application/json"
}

def get_dhan_option_chain():
    """Fetch Real-Time Option Chain Data from Dhan API"""
    if not client_id or not access_token:
        return None, "Secrets లో DHAN_CLIENT_ID లేదా DHAN_ACCESS_TOKEN మిస్ అయింది."

    # NIFTY Index Security ID: 13 (NSE_IND)
    url = "https://api.dhan.co/v2/optionchain"
    payload = {
        "UnderlyingScrip": 13,
        "UnderlyingSeg": "NSE_IND"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=6)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return data.get("data", {}), "OK"
            else:
                return None, f"Dhan API Error: {data.get('remarks', 'Failed to load option chain')}"
        else:
            return None, f"HTTP Error {response.status_code}: {response.text}"
    except Exception as e:
        return None, f"API Exception: {str(e)}"

# App Header
st.title("⚡ NIFTY ATM ± 6 Real-Time Order Flow Engine")

# Fetch Live Data
oc_data, status = get_dhan_option_chain()

if oc_data:
    spot_price = oc_data.get("last_price", 0.0)
    if spot_price == 0.0:
        # Fallback if last_price key varies
        spot_price = oc_data.get("oc", {}).get("last_price", 24223.55)
    
    atm_strike = round(spot_price / 50) * 50

    st.success(f"🟢 Live Dhan Feed Connected | NIFTY Spot: ₹{spot_price:,.2f} | ATM: {atm_strike}")
    
    # Process Strikes Data
    chain_list = oc_data.get("oc", {})
    
    # Selected ATM ± 6 strikes list
    target_strikes = [atm_strike + (i * 50) for i in range(-6, 7)]
    
    strike_records = []
    total_ce_vol = 0
    total_pe_vol = 0
    
    for strike, data in chain_list.items():
        try:
            strike_val = float(strike)
        except ValueError:
            continue
            
        if strike_val in target_strikes:
            ce_info = data.get("ce", {})
            pe_info = data.get("pe", {})
            
            ce_vol = ce_info.get("volume", 0)
            pe_vol = pe_info.get("volume", 0)
            ce_oi = ce_info.get("oi", 0)
            pe_oi = pe_info.get("oi", 0)
            
            total_ce_vol += ce_vol
            total_pe_vol += pe_vol
            
            # Order Flow Imbalance Ratio (Sell Strength)
            sell_strength = round(pe_vol / (ce_vol + 1e-5), 2)
            
            if sell_strength > 1.3:
                imbalance = "🟢 Strong Put Writing (Bullish)"
            elif sell_strength < 0.7:
                imbalance = "🔴 Strong Call Writing (Bearish)"
            else:
                imbalance = "⚪ Neutral Flow"

            strike_records.append({
                "Strike Price": int(strike_val),
                "CE Volume": f"{ce_vol:,}",
                "CE OI": f"{ce_oi:,}",
                "PE Volume": f"{pe_vol:,}",
                "PE OI": f"{pe_oi:,}",
                "Sell Strength": sell_strength,
                "Order Flow Imbalance": imbalance
            })

    # Display Options
    st.markdown("---")
    tab1, tab2 = st.tabs(["🎯 Live Strike-Wise Imbalance (ATM ± 6)", "⏱️ 1-Min Live Flow Summary"])

    with tab1:
        st.subheader("🎯 Real-Time ATM ± 6 Strikes Flow")
        if strike_records:
            df_live = pd.DataFrame(strike_records)
            st.dataframe(df_live, use_container_width=True)
        else:
            st.warning("ధన్ నుండి ఆప్షన్ చైన్ ప్రాసెస్ కావడం లేదు. మార్కెట్ అవర్స్ లో మళ్లీ చూడండి.")

    with tab2:
        st.subheader("⏱️ Live Candle Flow Signal")
        
        # Real-time Flow Direction Determination
        overall_flow = "BULL" if total_pe_vol > total_ce_vol else "BEAR"
        pcr_vol = round(total_pe_vol / (total_ce_vol + 1e-5), 2)
        
        curr_time = datetime.now().strftime("%H:%M")
        
        side_html = f'<span class="tag-bull">BULL</span>' if overall_flow == "BULL" else f'<span class="tag-bear">BEAR</span>'
        align_html = '<span class="tag-align">STRONG ALIGNMENT</span>' if pcr_vol > 1.2 or pcr_vol < 0.8 else '<span>No wall touch</span>'

        st.markdown(f"""
            <div class="flow-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="font-size: 18px; color: #FFFFFF;">{curr_time}</strong> 
                        <span style="color: #8B949E; margin-left: 10px;">₹{spot_price:,.2f}</span>
                    </div>
                    <div>{side_html}</div>
                </div>
                <div style="margin-top: 8px; font-size: 14px;">
                    State: <strong>FLOW ONLY</strong> | {align_html}
                </div>
                <div style="margin-top: 6px; font-size: 13px; color: #00E676;">
                    Total ATM±6 Volume PCR: <strong>{pcr_vol}</strong> (Put Vol: {total_pe_vol:,} / Call Vol: {total_ce_vol:,})
                </div>
            </div>
        """, unsafe_allow_html=True)

else:
    st.error(f"❌ లైవ్ డేటా కనెక్షన్ విఫలమైంది: {status}")
    st.info("💡 ధన్ API టోకెన్ వాలిడిటీ సరిచూసుకోండి (లేదా మార్కెట్ సమయం నందు మళ్లీ ప్రయత్నించండి).")

# Sidebar Controls
st.sidebar.title("⚡ Settings")
auto_refresh = st.sidebar.checkbox("⚡ Live Auto-Refresh (3 sec)", value=True)
if auto_refresh:
    time.sleep(3)
    st.rerun()
