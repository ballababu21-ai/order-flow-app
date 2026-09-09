import streamlit as st
from dhanhq import dhanhq

st.set_page_config(
    page_title="Dhan Fix Test", page_icon="⚡", layout="centered"
)

st.title("⚡ Dhan Single Argument Fix")

ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ1c2VyUmVnaW9uIjoiRjEiLCJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzg5MDE3MzM0LCJpYXQiOjE3ODg5MzA5MzQsInRva2VuQ29uc3VtZXJUeXBlIjoiU0VMRiIsIndlYmhvb2tVcmwiOiIiLCJkaGFuQ2xpZW50SWQiOiIxMTAzODA1NjQyIn0.juKfpEMK3-LHb25CJseLW3t6sGnT1VCtpKeo4sVpqevqEW6XV2FsVQrcKisK4AyTBcBwYGwygVX7ADK60---Cg"

try:
  # కేవలం టోకెన్ మాత్రమే పాస్ చేయాలి
  dhan = dhanhq(ACCESS_TOKEN)
  st.success("🟢 Dhan Client Initialized Successfully!")

  # LTP డేటా టెస్ట్
  response = dhan.get_ltp_data(
      security_list=[{"exchange_segment": "IDX_I", "security_id": "13"}]
  )
  st.write("API Response:", response)

except Exception as e:
  st.error(f"❌ Error: {str(e)}")
