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

st.title("⚡ NIFTY Institutional Quant Engine (Direct Connect)")

# --- ఇన్‌పుట్ బాక్స్ ద్వారా క్రిడెన్షియల్స్ ఎంటర్ చేసే సింపుల్ మెథడ్ ---
with st.sidebar:
  st.header("🔑 Dhan API Credentials")
  st.info(
      "సీక్రెట్స్ టెన్షన్ వదిలేయండి. మీ Dhan వివరాలు ఇక్కడ డైరెక్ట్‌గా ఎంటర్"
      " చేయండి."
  )

  # మీరు కావాలంటే ఇక్కడ మీ వివరాలు బై-డిఫాల్ట్ కూడా సెట్ చేసుకోవచ్చు
  input_client_id = st.text_input("Client ID", type="default")
  input_access_token = st.text_input(
      "Access Token", type="password"
  )  # టోకెన్ కనిపించకుండా ఉంటుంది

# ధన్ క్లైంట్ ఇనిషియలైజేషన్
dhan = None
if DHAN_AVAILABLE and input_client_id and input_access_token:
  try:
    dhan = dhanhq(str(input_client_id).strip(), str(input_access_token).strip())
  except Exception as e:
    dhan = None


def get_live_market_data():
  if not dhan:
    return (
        None,
        None,
        "Dhan క్లైంట్ కనెక్ట్ కాలేదు. దయచేసి సైడ్‌బార్‌లో మీ Client ID మరియు"
        " Access Token ఎంటర్ చేయండి.",
    )
  try:
    response = dhan.get_ltp_data(
        security_list=[
            {"exchange_segment": "IDX_I", "security_id": "13"},  # Nifty Spot
            {
                "exchange_segment": "NSE_FNO",
                "security_id": "55332",
            },  # Nifty Future
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
      return (
          None,
          None,
          f"API రెస్పాన్స్ వచ్చింది కానీ ప్రైస్ లేదు. రెస్పాన్స్:"
          f" {response}",
      )
  except Exception as e:
    return None, None, f"API ఎర్రర్: {str(e)}"


if dhan:
  st.success(
      f"🟢 Dhan API Connected Successfully |"
      f" {datetime.now(ist).strftime('%I:%M:%S %p')} IST"
  )
else:
  st.warning(
      "⚠️ దయచేసి సైడ్‌బార్‌లో మీ ధన్ **Client ID** మరియు **Access Token**"
      " ఎంటర్ చేయండి."
  )


@st.fragment(run_every=5)
def render_live_dashboard():
  current_spot, current_fut, err = get_live_market_data()
  if current_spot is None:
    st.error(f"🚨 లైవ్ డేటా ఎర్రర్: {err}")
    return

  st.markdown(
      f"### 🟢 Live Spot Price: ₹{current_spot:,.2f} | Futures Price:"
      f" ₹{current_fut:,.2f}"
  )
  st.success(
      "మార్కెట్ లైవ్ డేటా సక్సెస్‌ఫుల్‌గా ఫెచ్ అవుతోంది! టెన్షన్ లేదు."
  )


if dhan:
  render_live_dashboard()
