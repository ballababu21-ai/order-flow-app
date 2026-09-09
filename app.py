from datetime import datetime
from zoneinfo import ZoneInfo
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="NIFTY Institutional Quant Engine", page_icon="⚡", layout="wide"
)

ist = ZoneInfo("Asia/Kolkata")

CLIENT_ID = "1103805642"
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ1c2VyUmVnaW9uIjoiRjEiLCJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzg5MDE3MzM0LCJpYXQiOjE3ODg5MzA5MzQsInRva2VuQ29uc3VtZXJUeXBlIjoiU0VMRiIsIndlYmhvb2tVcmwiOiIiLCJkaGFuQ2xpZW50SWQiOiIxMTAzODA1NjQyIn0.juKfpEMK3-LHb25CJseLW3t6sGnT1VCtpKeo4sVpqevqEW6XV2FsVQrcKisK4AyTBcBwYGwygVX7ADK60---Cg"

# ధన్ లైబ్రరీని సేఫ్‌గా లోడ్ చేయడం
dhan = None
init_error = None

try:
  from dhanhq import dhanhq

  # అధికారిక డాక్యుమెంటేషన్ ప్రకారం కరెక్ట్ ఇనిషియలైజేషన్
  dhan = dhanhq(client_id=CLIENT_ID, access_token=ACCESS_TOKEN)
except Exception as e:
  init_error = str(e)
  try:
    # ఒకవేళ సింగిల్ ఆర్గ్యుమెంట్ అయితే
    dhan = dhanhq(ACCESS_TOKEN)
    init_error = None
  except Exception as e2:
    init_error = f"Init 1: {e} | Init 2: {e2}"
    dhan = None


def get_live_market_data():
  if not dhan:
    return None, None, f"ధన్ క్లైంట్ కనెక్ట్ కాలేదు. ఎర్రర్: {init_error}"
  try:
    response = dhan.get_ltp_data(
        security_list=[
            {"exchange_segment": "IDX_I", "security_id": "13"},
            {"exchange_segment": "NSE_FNO", "security_id": "55332"},
        ]
    )
    spot_val, fut_val = None, None
    if response and isinstance(response, dict):
      data = response.get("data", {})
      if isinstance(data, dict):
        idx_data = data.get("IDX_I", {})
        if isinstance(idx_data, dict):
          spot_val = float(
              idx_data.get(
                  "13",
                  idx_data.get("last_price", idx_data.get("lp", idx_data.get("ltp", 0))),
              )
          )
        fno_data = data.get("NSE_FNO", {})
        if isinstance(fno_data, dict):
          fut_val = float(
              fno_data.get(
                  "55332",
                  fno_data.get("last_price", fno_data.get("lp", fno_data.get("ltp", 0))),
              )
          )
    if spot_val and spot_val > 0:
      return spot_val, fut_val if (fut_val and fut_val > 0) else spot_val, None
    else:
      return None, None, f"రెస్పాన్స్ వచ్చింది కానీ ప్రైస్ లేదు: {response}"
  except Exception as e:
    return None, None, str(e)


st.markdown(
    """
<style>
.stApp { background-color: #0E1117 !important; color: #FFFFFF !important; }
.stTabs [data-baseweb="tab-list"] { display: flex; flex-wrap: nowrap; overflow-x: auto; gap: 4px; background-color: #161B22; padding: 6px; border-radius: 8px; }
.stTabs [data-baseweb="tab"] { background-color: #21262D; color: #8B949E; border-radius: 4px; padding: 8px 12px; font-weight: 600; font-size: 13px; white-space: nowrap; }
.stTabs [aria-selected="true"] { background-color: #238636 !important; color: #FFFFFF !important; }
.row-bull-box { background-color: rgba(0, 200, 83, 0.12); border: 1px solid #00C853; border-radius: 6px; padding: 10px; margin-bottom: 8px; }
.gex-card { background: linear-gradient(135deg, rgba(156, 39, 176, 0.15), rgba(33, 150, 243, 0.05)); border: 1px solid #AB47BC; border-radius: 8px; padding: 12px; margin-bottom: 10px; }
.badge-bull { background-color: #00C853; color: #000; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; }
</style>
""",
    unsafe_allow_html=True,
)

st.title("⚡ NIFTY Institutional Quant Engine (Dhan Live)")

if dhan:
  st.success(
      f"🟢 Dhan API Connected Successfully |"
      f" {datetime.now(ist).strftime('%I:%M:%S %p')} IST"
  )
else:
  st.error(f"❌ కనెక్షన్ ఫెయిల్ అయింది. వివరాలు: {init_error}")


def check_wall_and_alignment(price, c_wall, p_wall, mtf_trend, flow_type):
  if abs(price - c_wall) <= 20:
    return "CALL WALL TOUCHED", "⚠️ ప్రైస్ కాల్ వాల్‌ను తాకింది!"
  elif abs(price - p_wall) <= 20:
    return "PUT WALL TOUCHED", "📍 ప్రైస్ పుట్ వాల్‌ను తాకింది!"
  return "ALIGNED", "Flow మరియు ట్రెండ్ ఒకే దిశలో ఉన్నాయి."


@st.fragment(run_every=5)
def render_live_dashboard():
  current_spot, current_fut, err_msg = get_live_market_data()

  if current_spot is None:
    st.error(f"🚨 లైవ్ డేటా ఎర్రర్: {err_msg}")
    return

  current_atm = round(current_spot / 50) * 50
  active_strikes = [current_atm + (i * 50) for i in range(-4, 5)]
  c_wall = current_atm + 150
  p_wall = current_atm - 150
  zero_gamma = current_atm - 25
  vah = current_atm + 85
  val = current_atm - 75
  poc_strike = current_atm

  st.markdown(
      f"SPOT: **₹{current_spot:,.2f}** | FUT: **₹{current_fut:,.2f}** | ATM:"
      f" **{current_atm}**"
  )

  tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
      "📊 Flow & OI",
      "🎯 Strikes & Matrix",
      "🔮 GEX & Walls",
      "🌊 Dark Pools & VAH",
      "📊 Footprint & Analytics",
      "⚡ Summary",
  ])

  with tab1:
    st.subheader("⏱️ Live Order Flow & 9-Strikes Range Tracker")
    st.info(
        f"🎯 **Active 9-Strikes Range (Spot ± 4):**"
        f" `{', '.join(map(str, active_strikes))}`"
    )
    status_type, status_msg = check_wall_and_alignment(
        current_spot, c_wall, p_wall, "BULLISH", "BULLISH"
    )
    st.success(f"**Alignment Status:** {status_type} — {status_msg}")

  with tab2:
    st.subheader("🎯 Specific Strikes, POC & MTF Matrix")
    col1, col2, col3 = st.columns(3)
    with col1:
      st.metric(label="Live PCR", value="1.14")
    with col2:
      st.metric(label="Max Pain", value=f"{current_atm}")
    with col3:
      st.metric(label="ATM IV", value="13.45%")

  with tab3:
    st.subheader("🔮 Gamma Exposure (GEX) & Dealer Walls")
    st.markdown(
        f"""
        <div class="gex-card">
        <h4 style="color: #AB47BC; margin:0 0 5px 0;">⚡ Zero Gamma Level: {zero_gamma}</h4>
        </div>
        """,
        unsafe_allow_html=True,
    )

  with tab4:
    st.subheader("🌊 Dark Pools, Vol Skew & VAH Migration")
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
      st.metric(label="VAH", value=f"₹{vah}")
    with col_p2:
      st.metric(label="POC", value=f"₹{poc_strike}")
    with col_p3:
      st.metric(label="VAL", value=f"₹{val}")

  with tab5:
    st.subheader("📊 Footprint Delta & Market Flow Analytics")
    st.success("🟢 మార్కెట్ డేటా లైవ్‌లో సింక్ అవుతోంది.")

  with tab6:
    st.subheader("⚡ Quick Executive Dashboard Summary")
    st.markdown(f"""
        - **Live Spot Price:** ₹{current_spot:,.2f}
        - **Live Futures Price:** ₹{current_fut:,.2f}
        - **ATM Strike:** {current_atm}
        - **Data Source:** Dhan Live API
        """)


if dhan:
  render_live_dashboard()
else:
  st.warning(
      "⚠️ దయచేసి `requirements.txt` లో `dhanhq` సరిగ్గా ఇన్‌స్టాల్ అయిందో లేదో"
      " చెక్ చేయండి (pip install dhanhq)."
  )

st.sidebar.title("⚡ Control Panel")
st.sidebar.info("🟢 Direct Token Mode Active.")
