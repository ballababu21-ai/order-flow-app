import base64
import hashlib
import hmac
import struct
import time
from fyers_apiv3 import fyersModel
import requests
import streamlit as st

st.set_page_config(page_title="Live Market Tracker", layout="centered")


# --- TOTP GENERATOR ---
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


# --- FYERS AUTO-LOGIN & ACCESS TOKEN ---
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
    headers = {"Content-Type": "application/json"}

    # 1. Send Login OTP
    url_send_otp = "https://api-t1.fyers.in/identity/v2/send_login_otp"
    r1 = requests.post(
        url_send_otp, json={"fy_id": fyers_id, "app_id": "2"}, headers=headers
    )
    res1 = r1.json()
    if res1.get("s") != "ok":
      st.error(f"Step 1 (Send OTP) Failed: {res1}")
      return None

    request_key = res1.get("request_key")

    # 2. Verify OTP (TOTP)
    url_verify_otp = "https://api-t1.fyers.in/identity/v2/verify_otp"
    r2 = requests.post(
        url_verify_otp,
        json={"request_key": request_key, "otp": totp_code},
        headers=headers,
    )
    res2 = r2.json()
    if res2.get("s") != "ok":
      st.error(f"Step 2 (Verify TOTP) Failed: {res2}")
      return None

    request_key_2 = res2.get("request_key")

    # 3. Verify PIN
    url_verify_pin = "https://api-t1.fyers.in/identity/v2/verify_pin"
    r3 = requests.post(
        url_verify_pin,
        json={
            "request_key": request_key_2,
            "identity_type": "pin",
            "identifier": pin,
        },
        headers=headers,
    )
    res3 = r3.json()
    if res3.get("s") != "ok":
      st.error(f"Step 3 (Verify PIN) Failed: {res3}")
      return None

    token_val = res3.get("data", {}).get("access_token")

    # 4. Auth Code Generation
    url_token = "https://api-t1.fyers.in/identity/v2/token"
    auth_headers = {
        "Authorization": f"Bearer {token_val}",
        "Content-Type": "application/json",
    }
    r4 = requests.post(
        url_token,
        headers=auth_headers,
        json={
            "client_id": app_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "state": "sample",
        },
    )
    res4 = r4.json()
    if res4.get("s") != "ok":
      st.error(f"Step 4 (Auth Code) Failed: {res4}")
      return None

    auth_code = res4.get("auth_code")

    # 5. Fyers Official SDK Session for Access Token
    session = fyersModel.SessionModel(
        client_id=app_id,
        secret_key=secret_key,
        redirect_uri=redirect_uri,
        response_type="code",
        grant_type="authorization_code",
    )
    session.set_token(auth_code)
    response = session.generate_token()

    if response.get("s") == "ok":
      access_token = response.get("access_token")
      return fyersModel.FyersModel(
          client_id=app_id, is_async=False, token=access_token, log_path=""
      )
    else:
      st.error(f"Step 5 (Final Token) Failed: {response}")
      return None

  except Exception as e:
    st.error(f"Auth Exception: {e}")
    return None


# --- UI & LIVE MARKET DATA ---
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
    st.warning(f"డేటా పొందడంలో ఇబ్బంది: {res}")
