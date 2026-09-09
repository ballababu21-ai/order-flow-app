import streamlit as st
from dhanhq import dhanhq

st.set_page_config(
    page_title="Dhan Deep Debug", page_icon="🐞", layout="centered"
)

st.title("🐞 Dhan API Direct Debugger")

CLIENT_ID = "1103805642"
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ1c2VyUmVnaW9uIjoiRjEiLCJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzg5MDE3MzM0LCJpYXQiOjE3ODg5MzA5MzQsInRva2VuQ29uc3VtZXJUeXBlIjoiU0VMRiIsIndlYmhvb2tVcmwiOiIiLCJkaGFuQ2xpZW50SWQiOiIxMTAzODA1NjQyIn0.juKfpEMK3-LHb25CJseLW3t6sGnT1VCtpKeo4sVpqevqEW6XV2FsVQrcKisK4AyTBcBwYGwygVX7ADK60---Cg"

try:
  st.write("1. Initializing dhanhq client...")
  # టోకెన్ మరియు క్లైంట్ ఐడీ పాస్ చేసే విధానం
  dhan = dhanhq(client_id=CLIENT_ID, access_token=ACCESS_TOKEN)
  st.success("Client object created successfully!")

  st.write("2. Fetching test LTP data...")
  response = dhan.get_ltp_data(
      security_list=[{"exchange_segment": "IDX_I", "security_id": "13"}]
  )
  st.write("3. API Response received:")
  st.json(response)

except Exception as e:
  st.error("❌ Exception Caught during API Call:")
  st.exception(e)
