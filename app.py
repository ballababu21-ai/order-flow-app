import base64
import hashlib
import hmac
import struct
import time
import requests
import streamlit as st

st.set_page_config(page_title="Live Market Tracker", layout="centered")


# --- TOTP GENERATOR ---
def get_totp(secret):
  secret = secret.strip().replace(" ", "").upper()
  key = base64.b32decode(secret + "=" * ((8 - len(secret) % 8) % 8))
  counter = struct.pack(">Q", int(time.time()) // 30)
  digest = hmac.new(key, counter, hashlib.sha1).digest()
  offset = digest[19] & 0x0F
  code = (
      struct.unpack(">I", digest[offset : offset + 4])[0] & 0x7FFFFFFF
  ) % 1000000
  return f"{code:06d}"


# --- FYERS DIRECT API LOGIN ---
@st.cache_resource(ttl=86400)
def get_access_token():
  try:
    app_id = st.secrets["APP_ID"].strip()
    secret_key = st.secrets["SECRET_KEY"].strip()
    fyers_id = st.secrets["FYERS_ID"].strip()
    pin = st.secrets["PIN"].strip()
    totp_key = st.secrets["TOTP_KEY"].strip()
    redirect_uri = "https://127.0.0.1"

    headers = {"Content-Type": "application/json"}

    # 1. Send OTP
    r1 = requests.post(
        "https://api-t1.fyers.in/api/v3/send-login-otp",
        json={"fy_id": fyers_id, "app_id": "2"},
        headers=headers,
    ).json()
    req_key = r1.get("request_key")
    if not req_key:
      return None

    # 2. Verify TOTP
    r2 = requests.post(
        "https://api-t1.fyers.in/api/v3/verify-otp",
        json={"request_key": req_key, "otp": get_totp(totp_key)},
        headers=headers,
    ).json()
    req_key2 = r2.get("request_key")
    if not req_key2:
      return None

    # 3. Verify PIN
    r3 = requests.post(
        "https://api-t1.fyers.in/api/v3/verify-pin",
        json={
            "request_key": req_key2,
            "identity_type": "pin",
            "identifier": pin,
        },
        headers=headers,
    ).json()
    token_val = r3.get("data", {}).get("access_token")
    if not token_val:
      return None

    # 4. Get Auth Code
    r4 = requests.post(
        "https://api-t1.fyers.in/api/v3/token",
        headers={"Authorization": f"Bearer {token_val}"},
        json={
            "client_id": app_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "state": "sample",
        },
    ).json()
    auth_code = r4.get("auth_code")
    if not auth_code:
      return None

    # 5. Generate Access Token
    app_id_hash = hashlib.sha256(
        f"{app_id}:{secret_key}".encode()
    ).hexdigest()
    r5 = requests.post(
        "https://api-t1.fyers.in/api/v3/validate-authcode",
        json={
            "grant_type": "authorization_code",
            "appIdHash": app_id_hash,
            "code": auth_code,
        },
        headers=headers,
    ).json()

    return r5.get("access_token")

  except Exception:
    return None


# --- UI ---
st.title("📊 Live Market Tracker")

if st.button("🔄 Refresh Data"):
  st.rerun()

token = get_access_token()

if token:
  app_id = st.secrets["APP_ID"].strip()
  headers = {"Authorization": f"{app_id}:{token}"}
  symbols = "NSE:NIFTY50-INDEX,BSE:SENSEX-INDEX"

  res = requests.get(
      f"https://api-t1.fyers.in/data/quotes?symbols={symbols}",
      headers=headers,
  ).json()

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
    st.error("డేటా రాలేదు. టోకెన్ లేదా సింబల్స్ చెక్ చేయండి.")
else:
  st.error(
      "అథెంటికేషన్ ఫెయిల్ అయింది. Streamlit Secrets లో వివరాలు సరిచూసుకోండి."
  )
