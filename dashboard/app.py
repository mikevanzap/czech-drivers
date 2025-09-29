import streamlit as st
import requests
import os

# Use API URL from env (set in Azure App Service)
API_URL = os.getenv("API_URL", "http://localhost:7071/api/data")

st.set_page_config(page_title="Czech Drivers Points Dashboard", layout="wide")
st.title("🚦 Points for Foreign Drivers in Czechia")
st.caption("Data: Ministry of Transport CZ | Updated monthly")

try:
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()
    data = response.json()

    if not data:
        st.warning("No data available.")
    else:
        st.bar_chart(data, x="area", y="total_points")
        st.dataframe(data, use_container_width=True)

except Exception as e:
    st.error(f"Failed to load  {e}")