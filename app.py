st.markdown(f"""
        **Key Quant Levels:**
        - **Zero Gamma:** {zero_gamma}
        - **Call / Put Walls:** {call_wall} / {put_wall}
        - **POC Strike:** {poc_strike}
        """)
  st.success("🟢 Dhan API connection active. All 6 modules are fully operational.")

# Auto Refresh Control in Sidebar
st.sidebar.title("⚡ Control Panel")
auto = st.sidebar.checkbox("⚡ Live Auto-Refresh (5 sec)", value=True)
if auto:
  time.sleep(5)
  st.rerun()