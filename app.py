from datetime import datetime
from zoneinfo import ZoneInfo
import streamlit as st

try:
  from dhanhq import dhanhq

  DHAN_AVAILABLE = True
except ImportError:
  DHAN_AVAILABLE = False

st.set_page_config(
    page_title="NIFTY Institutional Quant Engine", page_icon="⚡", layout="wide"
)

ist = ZoneInfo("Asia/Kolkata")

st.title("⚡ NIFTY Institutional Quant Engine (Error Debugger)")

with st.sidebar:
  st.header("🔑 Dhan API Credentials")
  input_client_id = st.text_input("Client ID", value="1103805642")
  input_access_token = st.text_input("Access Token", type="password")

dhan = None
init_error = None

if DHAN_AVAILABLE and input_client_id and input_access_token:
  try:
    # డైరెక్ట్ ఇనిషియలైజేషన్ విత్ ఎర్రర్ ట్రాకింగ్
    dhan = dhanhq(str(input_client_id).strip(), str(input_access_token).strip())
  except Exception as e:
    init_error = str(e)
    dhan = None

if dhan:
  st.success("🟢 Dhan API Connected Successfully!")

  try:
    response = dhan.get_ltp_data(
        security_list=[{"exchange_segment": "IDX_I", "security_id": "13"}]
    )
    st.write("API Response:", response)
  except Exception as api_err:
    st.error(f"API Fetch Error: {str(api_err)}")

else:
  st.error("❌ Dhan క్లైంట్ ఇనిషియలైజ్ కాలేదు.")
  if init_error:
    st.error(f"అసలు ఎర్రర్ ఇదే: {init_error}")
  else:
    st.warning(
        "దయచేసి సైడ్‌బార్‌లో మీ **Access Token** పూర్తిగా సరిగ్గా ఎంటర్"
        " చేయండి."
    )
