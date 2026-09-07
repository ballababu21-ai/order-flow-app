from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import numpy as np
import pandas as pd
import streamlit as st

try:
  from dhanhq import dhanhq
  DHAN_AVAILABLE = True
except ImportError:
  DHAN_AVAILABLE = False

st.set_page_config(
    page_title="MCX Crude Oil Quant Engine (Dhan Live)",
    page_icon="🛢️",
    layout="wide",
)

ist = ZoneInfo("Asia/Kolkata")

# --- మీ ధన్ API క్రెడెన్షియల్స్ ఇక్కడ ఇవ్వండి ---
CLIENT_ID = "YOUR_DHAN_CLIENT_ID"
ACCESS_TOKEN = "YOUR_DHAN_ACCESS_TOKEN"

dhan = None
if DHAN_AVAILABLE:
  try:
    # సరియైన కీవర్డ్ ఆర్గ్యుమెంట్స్ తో ఇనిషియలైజేషన్
    dhan = dhanhq(client_id=CLIENT_ID, access_token=ACCESS_TOKEN)
  except Exception as e:
    st.error(f"Dhan Init Error: {e}")

# క్రూడాయిల్ లైవ్ డేటా ఫెచ్ చేసే ఫంక్షన్
def get_live_market_data():
  if not dhan:
    return 6000.00, 6010.00

  try:
    response = dhan.get_ltp_data(
        security_list=[{"exchange_segment": "MCX_COMM", "security_id": "481575"}]
    )
    
    st.info(f"📡 Crude Oil Raw Response: {response}")

    if response and isinstance(response, dict) and "data" in response:
      data = response["data"]
      spot_val = 0.0

      if isinstance(data, dict):
        for k, v in data.items():
          if isinstance(v, dict):
            val = float(v.get("last_price", v.get("lp", v.get("ltp", 0))))
            if val > 0:
              spot_val = val
              break
          elif isinstance(v, (int, float)) and v > 0:
            spot_val = float(v)
            break

      if spot_val > 0:
        return spot_val, spot_val + 10.0

  except Exception as e:
    st.error(f"API Exception Error: {e}")

  return 6000.00, 6010.00

# Custom Styling
st.markdown(
    """
<style>
.stApp { background-color: #0E1117 !important; color: #FFFFFF !important; }
.stTabs [data-baseweb="tab-list"] {
    display: flex; flex-wrap: nowrap; overflow-x: auto; gap: 4px;
    background-color: #161B22; padding: 6px; border-radius: 8px;
}
.stTabs [data-baseweb="tab"] {
    background-color: #21262D; color: #8B949E; border-radius: 4px;
    padding: 8px 12px; font-weight: 600; font-size: 13px; white-space: nowrap;
}
.stTabs [aria-selected="true"] { background-color: #238636 !important; color: #FFFFFF !important; }
</style>
""",
    unsafe_allow_html=True,
)

st.title("🛢️ MCX Crude Oil Quant Engine (Dhan Live)")

spot, fut_price = get_live_market_data()

st.caption(f"CRUDE SPOT: **₹{spot:,.2f}** | FUT: **₹{fut_price:,.2f}**")

@st.fragment(run_every=5)
def render_live_dashboard():
  s_val, f_val = get_live_market_data()
  st.success(f"🟢 MCX Live Feed Active | Current Price: ₹{s_val:,.2f}")

render_live_dashboard()

st.sidebar.title("⚡ Control Panel")
st.sidebar.info("🟢 MCX Crude Oil Live Mode Active")
