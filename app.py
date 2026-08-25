import base64
import hashlib
import hmac
import struct
import time
from fyers_apiv3 import fyersModel
import requests
import streamlit as st

st.set_page_config(page_title="Live Market Tracker", layout="centered")


# --- PURE PYTHON TOTP GENERATOR ---
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


# --- FYERS AUTHENTICATION ---
@st.cache_resource(ttl=86400)
def get_fyers_instance():
  try:
    app_id = st.secrets["APP_ID"].strip()
    secret_key = st.secrets["SECRET_KEY"].strip()
    fyers_id = st.secrets["FYERS_ID"].strip()
    pin = st.secrets["PIN"].strip()
    totp_key = st.secrets["TOTP_KEY"].strip()
    redirect_uri = "https://127.0.0.1"

    totp_code = get_totp_code(totp_key)

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        ),
        "Content-Type": "application/json",
    }

    # Step 1: Send OTP
    r1 = requests.post(
        "https://api.fyers.in/api/v3/send-login-otp",
        json={"fy_id": fyers_id, "app_id": "2"},
        headers=headers,
    ).json()

    # Step 2: Verify OTP
    r2 = requests.post(
        "https://api.fyers.in/api/v3/verify-otp",
        json={"request_key": r1.get("request_key"), "otp": totp_code},
        headers=headers,
    ).json()

    # Step 3: Verify PIN
    r3 = requests.post(
        "https://api.fyers.in/api/v3/verify-pin",
        json={
            "request_key": r2.get("request_key"),
            "identity_type": "pin",
            "identifier": pin,
        },
        headers=headers,
    ).json()

    token_val = r3.get("data", {}).get("access_token")

    # Step 4: Generate Auth Code
    auth_headers = headers.copy()
    auth_headers["Authorization"] = f"Bearer {token_val}"

    r4 = requests.post(
        "https://api.fyers.in/api/v3/token",
        headers=auth_headers,
        json={
            "client_id": app_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "state": "sample",
        },
    ).json()

    auth_code = r4.get("auth_code")

    # Step 5: Fyers Model Session
    session = fyersModel.SessionModel(
        client_id=app_id,
        secret_key=secret_key,
        redirect_uri=redirect_uri,
        response_type="code",
        grant_type="authorization_code",
    )
    session.set_token(auth_code)
    response = session.generate_token()
    access_token = response.get("access_token")

    return fyersModel.FyersModel(
        client_id=app_id, is_async=False, token=access_token, log_path=""
    )
  except Exception as e:
    st.error(f"Fyers Auth Error: {e}")
    return None


# --- UI & LIVE DATA ---
st.title("📊 Live Market Tracker")

if st.button("🔄 Refresh Data"):
  st.rerun()

fyers = get_fyers_instance()

if fyers:
  data = {"symbols": "NSE:NIFTY50-INDEX,BSE:SENSEX-INDEX"}
  res = fyers.quotes(data=data)

  if res.get("s") == "ok":
    quotes = {item["n"]: item["v"] for item in res.get("d", [])}

    nifty = quotes.get("NSE:NIFTY50-INDEX", {})
    sensex = quotes.get("BSE:SENSEX-INDEX", {})

    st.subheader("NIFTY 50")
    st.metric(
        label="LTP",
        value=nifty.get("lp", 0),
        delta=round(nifty.get("ch", 0), 2),
    )

    st.subheader("SENSEX")
    st.metric(
        label="LTP",
        value=sensex.get("lp", 0),
        delta=round(sensex.get("ch", 0), 2),
    )
  else:
    st.warning("డేటా పొందడంలో ఇబ్బంది వచ్చింది. Secrets సరిచూసుకోండి.")
