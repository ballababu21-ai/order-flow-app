import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Order Flow Mobile", layout="centered")

st.markdown("""
    <style>
    .metric-card {
        background-color: #1e222d;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 10px;
        color: white;
    }
    .bullish { border-left: 5px solid #26a69a; }
    .bearish { border-left: 5px solid #ef5350; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Order Flow Mobile")

def fetch_data():
    return [
        {"Time": "11:05", "Strike": "24200 PE", "State": "BULL", "Signal": "FLOW ONLY", "Wall": "No wall touch"},
        {"Time": "11:05", "Strike": "24250 CE", "State": "BEAR", "Signal": "STRONG ALIGNMENT", "Wall": "No wall touch"},
        {"Time": "11:05", "Strike": "24300 CE", "State": "BEAR", "Signal": "STRONG ALIGNMENT", "Wall": "Wall Touch @ 24300"}
    ]

data = fetch_data()

for row in data:
    card_class = "bullish" if row["State"] == "BULL" else "bearish"
    color = "#26a69a" if row["State"] == "BULL" else "#ef5350"
    
    st.markdown(f"""
    <div class="metric-card {card_class}">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <b style="font-size: 16px;">{row['Time']} | {row['Strike']}</b>
            <span style="background-color:{color}; padding:2px 8px; border-radius:4px; font-weight:bold;">{row['State']}</span>
        </div>
        <div style="margin-top:8px; font-size:14px;">
            <b>Signal:</b> {row['Signal']}<br>
            <b>Status:</b> {row['Wall']}
        </div>
    </div>
    """, unsafe_allow_html=True)
