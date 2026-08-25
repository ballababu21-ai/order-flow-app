import base64
import hashlib
import hmac
import struct
import time
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


# --- FYERS AUTO AUTH & ACCESS TOKEN ---
@st.cache_resource(ttl=86400)
def get_fyers_access_token():
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
            " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        "Content-Type": "application/json",
    }

    # Step 1: Send OTP
    r1 = requests.post(
        "https://api-t1.fyers.in/identity/v2/send_login_otp",
        json={"fy_id": fyers_id, "app_id": "2"},
        headers=headers,
    )
    if r1.status_code != 200:
      st.error(
          f"Step 1 Failed [Status {r1.status_code}]: {r1.text[:200]}"
      )
      return None
    res1 = r1.json()

    # Step 2: Verify OTP
    r2 = requests.post(
        "https://api-t1.fyers.in/identity/v2/verify_otp",
        json={"request_key": res1.get("request_key"), "otp": totp_code},
        headers=headers,
    )
    if r2.status_code != 200:
      st.error(
          f"Step 2 Failed [Status {r2.status_code}]: {r2.text[:200]}"
      )
      return None
    res2 = r2.json()

    # Step 3: Verify PIN
    r3 = requests.post(
        "https://api-t1.fyers.in/identity/v2/verify_pin",
        json={
            "request_key": res2.get("request_key"),
            "identity_type": "pin",
            "identifier": pin,
        },
        headers=headers,
    )
    if r3.status_code != 200:
      st.error(
          f"Step 3 Failed [Status {r3.status_code}]: {r3.text[:200]}"
      )
      return None
    res3 = r3.json()
    token_val = res3.get("data", {}).get("access_token")

    # Step 4: Auth Code
    auth_headers = headers.copy()
    auth_headers["Authorization"] = f"Bearer {token_val}"

    r4 = requests.post(
        "https://api-t1.fyers.in/identity/v2/token",
        headers=auth_headers,
        json={
            "client_id": app_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "state": "sample",
        },
    )
    if r4.status_code != 200:
      st.error(
          f"Step 4 Failed [Status {r4.status_code}]: {r4.text[:200]}"
      )
      return None
    res4 = r4.json()
    auth_code = res4.get("auth_code")

    # Step 5: Final Access Token
    app_id_hash = hashlib.sha256(
        f"{app_id}:{secret_key}".encode()
    ).hexdigest()
    r5 = requests.post(
        "https://api-t1.fyers.in/api/v3/validate-authcode",
        headers=headers,
        json={
            "grant_type": "authorization_code",
            "appIdHash": app_id_hash,
            "code": auth_code,
        },
    )
    if r5.status_code != 200:
      st.error(
          f"Step 5 Failed [Status {r5.status_code}]: {r5.text[:200]}"
      )
      return None
    res5 = r5.json()

    return res5.get("access_token")

  except Exception as e:
    st.error(f"Fyers Auth Error: {e}")
    return None


# --- UI & LIVE DATA ---
st.title("📊 Live Market Tracker")

if st.button("🔄 Refresh Data"):
  st.rerun()

access_token = get_fyers_access_token()

if access_token:
  app_id = st.secrets["APP_ID"].strip()
  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
      ),
      "Authorization": f"{app_id}:{access_token}",
  }
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
    st.warning("డేటా ఫెచ్ కాలేదు. Secrets లోని వివరాలు తనిఖీ చేయండి.")
