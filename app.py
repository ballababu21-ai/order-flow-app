import streamlit as st

st.set_page_config(
    page_title="Dhan Debugger", page_icon="🔍", layout="centered"
)

st.title("🔍 Dhan API Secrets & Connection Debugger")

# 1. Check if dhanhq is installed
try:
  from dhanhq import dhanhq

  st.success("✅ `dhanhq` library is installed successfully.")
  DHAN_AVAILABLE = True
except ImportError:
  st.error(
      "❌ `dhanhq` library is NOT installed! Please run `pip install dhanhq`."
  )
  DHAN_AVAILABLE = False

# 2. Check Secrets
st.subheader("📋 Secrets Check:")
client_id_val = ""
access_token_val = ""

try:
  if "CLIENT_ID" in st.secrets:
    client_id_val = st.secrets["CLIENT_ID"]
    st.write(
        "Found `CLIENT_ID` directly in st.secrets (Length:"
        f" {len(str(client_id_val))})"
    )
  elif "dhan" in st.secrets and "CLIENT_ID" in st.secrets["dhan"]:
    client_id_val = st.secrets["dhan"]["CLIENT_ID"]
    st.write(
        "Found `CLIENT_ID` inside `[dhan]` section (Length:"
        f" {len(str(client_id_val))})"
    )
  else:
    st.error("❌ `CLIENT_ID` not found in st.secrets!")
except Exception as e:
  st.error(f"Error reading CLIENT_ID: {e}")

try:
  if "ACCESS_TOKEN" in st.secrets:
    access_token_val = st.secrets["ACCESS_TOKEN"]
    st.write(
        "Found `ACCESS_TOKEN` directly in st.secrets (Length:"
        f" {len(str(access_token_val))})"
    )
  elif "dhan" in st.secrets and "ACCESS_TOKEN" in st.secrets["dhan"]:
    access_token_val = st.secrets["dhan"]["ACCESS_TOKEN"]
    st.write(
        "Found `ACCESS_TOKEN` inside `[dhan]` section (Length:"
        f" {len(str(access_token_val))})"
    )
  else:
    st.error("❌ `ACCESS_TOKEN` not found in st.secrets!")
except Exception as e:
  st.error(f"Error reading ACCESS_TOKEN: {e}")

# 3. Test Dhan Initialization
if DHAN_AVAILABLE and client_id_val and access_token_val:
  st.subheader("🔌 Dhan Client Initialization Test:")
  try:
    dhan_client = dhanhq(str(client_id_val).strip(), str(access_token_val).strip())
    st.success("🟢 Dhan Client Initialized Successfully!")

    # Test LTP Fetch
    with st.spinner("Fetching Nifty LTP data from Dhan..."):
      res = dhan_client.get_ltp_data(
          security_list=[{"exchange_segment": "IDX_I", "security_id": "13"}]
      )
      st.write("API Response:")
      st.json(res)

  except Exception as e:
    st.error(f"❌ Dhan Client Initialization Failed with Error: {str(e)}")
else:
  st.warning(
      "⚠️ Cannot initialize Dhan client because credentials or library are"
      " missing."
  )
