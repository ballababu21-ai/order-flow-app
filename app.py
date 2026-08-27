import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Intraday Options Flow Tracker", layout="wide")

st.title("📊 Options Order Flow & Futures Neutralization Dashboard")

# Sidebar Filters
st.sidebar.header("Control Panel")
index_symbol = st.sidebar.selectbox("Select Index", ["NIFTY", "BANKNIFTY"])
expiry = st.sidebar.date_input("Select Expiry")

# Top Metrics Row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Overall Flow Signal", "BULLISH", "+2.45L")
col2.metric("PE Net Seller Flow", "+10.21L", "Strong PE Support")
col3.metric("CE Net Seller Flow", "-4.15L", "Weak CE Resistance")
col4.metric("Market Sentiment", "STRONG ALIGNMENT", delta_color="normal")

st.divider()

# Sample Data Structure matching your screenshot
data = [
    {
        "Time": "11:05",
        "Strike": "24200 PE",
        "CE / PE Vol": "69.73L / 46.97L",
        "Neutralized Flow": "+1.73L",
        "Seller Net": "+4.74L",
        "Signal": "BULL",
        "State": "FLOW ONLY",
        "Build-Up": "Fresh Short Build"
    },
    {
        "Time": "11:05",
        "Strike": "24150 PE",
        "CE / PE Vol": "25.88L / 8.61L",
        "Neutralized Flow": "-72.67K",
        "Seller Net": "+94.64K",
        "Signal": "BEAR",
        "State": "STRONG ALIGNMENT",
        "Build-Up": "Fresh Short Build"
    },
    {
        "Time": "11:05",
        "Strike": "24250 CE",
        "CE / PE Vol": "35.19L / 37.56L",
        "Neutralized Flow": "+31.14K",
        "Seller Net": "-1.11L",
        "Signal": "BEAR",
        "State": "STRONG ALIGNMENT",
        "Build-Up": "Short Covering"
    },
    {
        "Time": "11:05",
        "Strike": "24300 CE",
        "CE / PE Vol": "1.13Cr / 75.93L",
        "Neutralized Flow": "-26.52K",
        "Seller Net": "+6.63L",
        "Signal": "BEAR",
        "State": "STRONG ALIGNMENT",
        "Build-Up": "Fresh Long Build"
    }
]

df = pd.DataFrame(data)

# Styled Dataframe Display
st.subheader("⚡ Real-time Strike-wise Flow & Cumulative Neutralization")

def highlight_signal(val):
    if val == 'BULL':
        return 'background-color: #d4edda; color: green; font-weight: bold'
    elif val == 'BEAR':
        return 'background-color: #f8d7da; color: red; font-weight: bold'
    return ''

styled_df = df.style.map(highlight_signal, subset=['Signal'])
st.dataframe(styled_df, use_container_width=True)

# Futures & OI Build-up Details Section
st.subheader("🎯 Futures Cum Neutralization & OI Signals")
col_left, col_right = st.columns(2)

with col_left:
    st.info("**Fresh Short Build Detected**\n\nPx: -10.00 | OI: +2.3K\nVol Strength: 0.26x | OI Strength: 1.06x")

with col_right:
    st.success("**Short Covering Signal**\n\nPx: +7.10 | OI: -1.2K\nVol Strength: 0.51x | OI Strength: 0.36x")
