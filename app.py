import streamlit as st
from dhanhq import dhanhq

st.set_page_config(
    page_title="Dhan Exact Error Debugger", page_icon="🔍", layout="wide"
)

st.title("🔍 Dhan Exact Exception Debugger")

CLIENT_ID = "1103805642"
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ1c2VyUmVnaW9uIjoiRjEiLCJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzg5MDE3MzM0LCJpYXQiOjE3ODg5MzA5MzQsInRva2VuQ29uc3VtZXJUeXBlIjoiU0VMRiIsIndlYmhvb2tVcmwiOiIiLCJkaGFuQ2xpZW50SWQiOiIxMTAzODA1NjQyIn0.juKfpEMK3-LHb25CJseLW3t6sGnT1VCtpKeo4sVpqevqEW6XV2FsVQrcKisK4AyTBcBwYGwygVX7ADK60---Cg"

st.write("Trying to initialize `dhanhq` client...")

try:
  # ఇక్కడ వచ్చే అసలు ఎర్రర్‌ను క్యాచ్ చేసి స్క్రీన్ పై ప్రింట్ చేస్తుంది
  dhan = dhanhq(CLIENT_ID, ACCESS_TOKEN)
  st.success("🟢 Success! Client created.")

  # ఇప్పుడు LTP డేటా టెస్ట్ చేద్దాం
  res = dhan.get_ltp_data(
      security_list=[{"exchange_segment": "IDX_I", "security_id": "13"}]
  )
  st.write("API Response:", res)

except Exception as e:
  st.error(f"❌ Python Exception Caught:")
  st.exception(e)  # ఇది పూర్తి ఎర్రర్ ట్రేస్‌బ్యాక్‌ను చూపిస్తుంది
