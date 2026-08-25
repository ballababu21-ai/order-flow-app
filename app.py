import base64
import hashlib
import hmac
import struct
import time
from fyers_apiv3 import fyersModel
import requests
import streamlit as st

st.set_page_config(page_title="Live Market Tracker", layout="centered")


# --- PURE PYTHON TOTP (No external pyotp required) ---
def get_totp_code(secret):
  secret = secret.strip().replace(" ", "").upper()
  key = base64.b32decode(secret + "=" * ((8 - len(secret) % 8) % 8))
  counter = struct.pack(">Q", int(time.time()) // 30)
  digest = hmac.new(key, counter, hashlib.sha1).digest()
  offset = digest[19] & 0x0F
  code = (
      struct.unpack(">I", digest[offset : offset + 4])[0] & 0x7FFFFFFF
  ) % 1000000
  return f"{code:06d}"


# --- FYERS AUTO-LOGIN & TOKEN GENERATION ---
@st.cache_resource(ttl=86400)
def get_fyers_instance():
  try:
    app_id = st.secrets["APP_ID"]
    secret_key = st.secrets["SECRET_KEY"]
    fyers_id = st.secrets["FYERS_ID"]
    pin = st.secrets["PIN"]
    totp_key = st.secrets["TOTP_KEY"]
    redirect_uri = "https://127.0.0.1"

    totp_code = get_totp_code(totp_key)

    r1 = requests.post(
        "https://api-v3.fyers.in/identity/v2/send_login_otp",
        json={"fy_id": fyers_id, "app_id": "2"},
    ).json()

    r2 = requests.post(
        "https://api-v3.fyers.in/identity/v2/verify_otp",
        json={"request_key": r1.get("request_key"), "otp": totp_code},
    ).json()

    r3 = requests.post(
        "https://api-v3.fyers.in/identity/v2/verify_pin",
        json={
            "request_key": r2.get("request_key"),
            "identity_type": "pin",
            "identifier": pin,
        },
    ).json()
    token_val = r3.get("data", {}).get("access_token")

    headers = {"Authorization": f"Bearer {token_val}"}
    r4 = requests.post(
        "https://api-v3.fyers.in/identity/v2/token",
        headers=headers,
        json={
            "client_id": app_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "state": "sample",
        },
    ).json()

    session = fyersModel.SessionModel(
        client_id=app_id,
        secret_key=secret_key,
        redirect_uri=redirect_uri,
        response_type="code",
        grant_type="authorization_code",
    )
    session.set_token(r4.get("auth_code"))
    access_token = session.generate_token().get("access_token")

    return fyersModel.FyersModel(
        client_id=app_id, is_async=False, token=access_token, log_path=""
    )
  except Exception as e:
    st.error(f"Fyers Auth Error: {e}")
    return None


# --- UI & LIVE DATA TRACKER ---
st.title("📊 Live Market Tracker")

if st.button("🔄 Refresh Data"):
  st.rerun()

fyers = get_fyers_instance()

if fyers:
  data = {"symbols": "NSE:NIFTY50-INDEX,NSE:NIFTYBANK-INDEX"}
  res = fyers.quotes(data=data)

  if res.get("s") == "ok":
    quotes = {item["n"]: item["v"] for item in res.get("d", [])}

    nifty = quotes.get("NSE:NIFTY50-INDEX", {})
    banknifty = quotes.get("NSE:NIFTYBANK-INDEX", {})

    st.subheader("NIFTY 50")
    st.metric(
        label="LTP",
        value=nifty.get("lp", 0),
        delta=round(nifty.get("ch", 0), 2),
    )

    st.subheader("BANK NIFTY")
    st.metric(
        label="LTP",
        value=banknifty.get("lp", 0),
        delta=round(banknifty.get("ch", 0), 2),
    )
  else:
    st.warning("డేటా పొందడంలో ఇబ్బంది వచ్చింది. Secrets సరిచూసుకోండి.")
