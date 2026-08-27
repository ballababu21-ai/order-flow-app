import streamlit as st
import pandas as pd

st.set_page_config(page_title="Options Order Flow", layout="wide")

# Autorefresh without needing extra packages
st.components.v1.html("""
    <script>
        setTimeout(function(){
            window.parent.postMessage({type: 'streamlit:render'}, '*');
        }, 5000);
    </script>
""", height=0)

# DhanHQ Safe Import (App crash avvakunda untundhi)
dhanhq_available = False
dhan = None

try:
    from dhanhq import dhanhq
    dhanhq_available = True
except Exception:
    dhanhq_available = False

# Dashboard CSS Styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 12px;
        border-left: 5px solid #28a745;
        margin-bottom: 10px;
    }
    .strike-row {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 6px;
        padding: 10px;
        margin-bottom: 8px;
    }
    .badge-bull { background-color: #d4edda; color: #155724; padding: 3px 8px; border-radius: 12px; font-weight: bold; font-size: 12px; }
    .badge-bear { background-color: #f8d7da; color: #721c24; padding: 3px 8px; border-radius: 12px; font-weight: bold; font-size: 12px; }
    .sub-text { font-size: 11px; color: #6c757d; }
    .green-text { color: #28a745; font-weight: 600; }
    .red-text { color: #dc3545; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ Options Flow & Neutralization Dashboard")

# API Connection logic
if dhanhq_available:
    try:
        CLIENT_ID = st.secrets["DHAN_CLIENT_ID"]
        ACCESS_TOKEN = st.secrets["DHAN_ACCESS_TOKEN"]
        dhan = dhanhq(CLIENT_ID, ACCESS_TOKEN)
        
        fund_limits = dhan.get_fund_limits()
        if fund_limits.get('status') == 'success':
            st.success("✅ Dhan API Connected Successfully!")
        else:
            st.warning("⚠️ Dhan Credentials check cheyandi.")
    except Exception as e:
        st.info("ℹ️ Secrets check cheyandi: Dhan Secrets missing.")
else:
    st.info("ℹ️ DhanHQ setup load avthondhi.")

# Top Summary Card
st.markdown("""
<div class="metric-card">
    <span class="sub-text">MARKET SENTIMENT</span>
    <h3 style="margin:0;">STRONG ALIGNMENT</h3>
    <span class="badge-bull">OVERALL FLOW: BULLISH (+2.45L)</span>
</div>
""", unsafe_allow_html=True)

st.subheader("Real-time Strike Flow")

strikes = [
    {
        "strike": "24200 PE", "ce_pe_vol": "69.73L / CE 46.97L",
        "neut_flow": "+1.73L", "dir_opp": "Dir 5.45L | Opp 3.73L",
        "seller_net": "+4.74L", "net_detail": "PE Net +4.74L | CE Net +0.00",
        "signal": "BULL", "state": "FLOW ONLY"
    },
    {
        "strike": "24150 PE", "ce_pe_vol": "25.88L / CE 8.61L",
        "neut_flow": "-72.67K", "dir_opp": "Dir 94.64K | Opp 1.67L",
        "seller_net": "+94.64K", "net_detail": "PE Net +94.64K | CE Net +0.00",
        "signal": "BEAR", "state": "STRONG ALIGNMENT"
    }
]

for row in strikes:
    badge_cls = "badge-bull" if row["signal"] == "BULL" else "badge-bear"
    neut_color = "green-text" if "+" in row["neut_flow"] else "red-text"
    
    st.markdown(f"""
    <div class="strike-row">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <strong style="font-size:16px;">{row['strike']}</strong><br/>
                <span class="sub-text">{row['ce_pe_vol']}</span>
            </div>
            <div>
                <span class="{badge_cls}">{row['signal']}</span>
                <span class="sub-text" style="margin-left:5px;">{row['state']}</span>
            </div>
        </div>
        <hr style="margin: 6px 0; border: 0; border-top: 1px solid #eee;"/>
        <div style="display: flex; justify-content: space-between;">
            <div>
                <span class="sub-text">NEUTRALIZED FLOW</span><br/>
                <span class="{neut_color}">{row['neut_flow']}</span><br/>
                <span class="sub-text">{row['dir_opp']}</span>
            </div>
            <div style="text-align: right;">
                <span class="sub-text">SELLER NET</span><br/>
                <span class="{neut_color}">{row['seller_net']}</span><br/>
                <span class="sub-text">{row['net_detail']}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
