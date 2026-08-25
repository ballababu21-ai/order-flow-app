import streamlit as st
import pandas as pd

st.title("Nifty Options & Candles Flow")
st.write("Live data or analysis dashboard ikkada display avtundi.")

# Sample table (ee place lo mee real-time data integration pettukovachu)
data = {
    "TIME": ["12:45", "12:44", "12:44"],
    "SIDE": ["BEAR", "BULL", "BULL"],
    "STATE": ["FLOW ONLY", "STRONG ALIGNMENT", "STRONG ALIGNMENT"],
    "VALUE": [24223.55, 24220.20, 24220.20]
}
df = pd.DataFrame(data)
st.dataframe(df)
