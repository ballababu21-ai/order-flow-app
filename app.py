import streamlit as st
import pandas as pd
from dhanhq import dhanhq
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Options Order Flow", layout="wide")

# 5 సెకన్లకు ఒకసారి ఆటో-రిఫ్రెష్
st_autorefresh(interval=5000, key="data_refresh")

# Secrets నుండి API Keys రీడ్ చేయడం
CLIENT_ID = st.secrets["DHAN_CLIENT_ID"]
ACCESS_TOKEN = st.secrets["DHAN_ACCESS_TOKEN"]

# Dhan Client Initialization
dhan = dhanhq(CLIENT_ID, ACCESS_TOKEN)

st.title("⚡ Options Flow & Neutralization Dashboard")

# Dhan API Connection Test
try:
    # Get Fund Limits / Connection Status
    fund_limits = dhan.get_fund_limits()
    if fund_limits.get('status') == 'success':
        st.success("✅ Dhan API Connected Successfully!")
    else:
        st.error("⚠️ Dhan API Connection Error: Token లేదా Client ID తప్పుగా ఉంది.")
except Exception as e:
    st.error(f"API Connection Exception: {e}")

# Sample Layout
st.markdown("### Real-time Market Signals")
col1, col2 = st.columns(2)
col1.metric("API Status", "Active", "Live Feed On")
col2.metric("Index", "NIFTY 50", "Monitoring")
