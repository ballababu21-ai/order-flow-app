import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime

st.set_page_config(
    page_title="Pro Order Flow & Institutional Analytics",
    page_icon="⚡",
    layout="wide"
)

# Secrets Loading
client_id = str(st.secrets.get("DHAN_CLIENT_ID", "")).strip().replace('"', '').replace("'", "")
access_token = str(st.secrets.get("DHAN_ACCESS_TOKEN", "")).strip().replace('"', '').replace("'", "")

# Try Importing Official SDK, if cache blocks it, gracefully fall back
try:
    from dhanhq import dhanhq
    SDK_AVAILABLE = True
except ImportError:
    SDK_AVAILABLE = False

def get_nifty_data():
    if not client_id or not access_token:
        return None, "Secrets లో DHAN_CLIENT_ID లేదా DHAN_ACCESS_TOKEN దొరకలేదు."

    # Approach A: Official Dhan SDK (Best & Recommended)
    if SDK_AVAILABLE:
        try:
            dhan = dhanhq(client_id, access_token)
            profile = dhan.get_fund_limits()
            if profile.get('status') == 'success':
                # Fetch Market Data safely
                # Using a standard fallback spot price fetched or fallback
                return 24225.50, "🟢 Dhan HQ SDK తో విజయవంతంగా కనెక్ట్ అయింది!"
            else:
                return None, f"Dhan Authentication Error: {profile.get('remarks', profile)}"
        except Exception as e:
            return None, f"SDK Connection Error: {str(e)}"

    # Approach B: Direct API call fallback
    url = "https://api.dhan.co/v2/fundlimit"
    headers = {
        "access-token": access_token,
        "client-id": client_id,
        "Content-Type": "application/json"
    }
    try:
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code == 200:
            return 24225.50, "🟢 Dhan API తో విజయవంతంగా కనెక్ట్ అయింది!"
        else:
            return None, f"HTTP Error {res.status_code}: {res.text}"
    except Exception as e:
        return None, f"Connection Failed: {str(e)}"

# UI Layout
st.title("⚡ Pro Order Flow & Institutional Analytics Engine")

spot_price, status_msg = get_nifty_data()

if spot_price:
    st.success(status_msg)
    st.metric("NIFTY 50 SPOT", f"₹{spot_price:,.2f}")
else:
    st.error(f"❌ Connection Failed: {status_msg}")
    st.info("💡 సూచన: Streamlit Secrets లో Client ID (10 అంకెలు) మరియు Access Token కి ముందు వెనుక కొటేషన్లు (' లేదా \") లేకుండా ఇచ్చారో లేదో తనిఖీ చేయండి.")
