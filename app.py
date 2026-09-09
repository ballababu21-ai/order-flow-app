from datetime import datetime
from zoneinfo import ZoneInfo
import streamlit as st
from dhanhq import dhanhq

st.set_page_config(
    page_title="NIFTY Institutional Quant Engine", page_icon="⚡", layout="wide"
)

ist = ZoneInfo("Asia/Kolkata")

CLIENT_ID = "1103805642"
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ1c2VyUmVnaW9uIjoiRjEiLCJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzg5MDE3MzM0LCJpYXQiOjE3ODg5MzA5MzQsInRva2VuQ29uc3VtZXJUeXBlIjoiU0VMRiIsIndlYmhvb2tVcmwiOiIiLCJkaGFuQ2xpZW50SWQiOiIxMTAzODA1NjQyIn0.juKfpEMK3-LHb25CJseLW3t6sGnT1VCtpKeo4sVpqevqEW6XV2FsVQrcKisK4AyTBcBwYGwygVX7ADK60---Cg"

st.title("⚡ NIFTY Institutional Quant Engine (Direct Token)")

dhan = None
try:
  dhan = dhanhq(CLIENT_ID, ACCESS_TOKEN)
except Exception as e:
  dhan = None


def get_live_market_data():
  if not dhan:
    return None, None, "Dhan క్లైంట్ కనెక్ట్ కాలేదు."
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


if dhan:
  st.success(
      f"🟢 Dhan API Connected Successfully |"
      f" {datetime.now(ist).strftime('%I:%M:%S %p')} IST"
  )
else:
  st.error("❌ కనెక్షన్ ఫెయిల్ అయింది.")


@st.fragment(run_every=5)
def render_live_dashboard():
  current_spot, current_fut, err = get_live_market_data()
  if current_spot is None:
    st.error(f"లైవ్ డేటా ఎర్రర్: {err}")
    return

  st.markdown(
      f"### 🟢 Live Spot: ₹{current_spot:,.2f} | Futures:"
      f" ₹{current_fut:,.2f}"
  )
  st.success("మార్కెట్ లైవ్ డేటా విజయవంతంగా స్ట్రీమ్ అవుతోంది!")


if dhan:
  render_live_dashboard()
