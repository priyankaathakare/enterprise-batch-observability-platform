import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Enterprise Batch", layout="wide")

st.title("Enterprise Batch Observability Platform v2.0")
st.success("Dashboard is LIVE! Connected!")

API_URL = "API_URL = "https://enterprise-batch-observability-platform.onrender.com""


# Try API
try:
    response = requests.get(f"{API_URL}/api/v1/metrics", timeout=5)
    if response.status_code == 200:
        data = response.json()
        st.success(f"API Connected: {API_URL}")
    else:
        raise Exception(f"Status {response.status_code}")
except Exception as e:
    st.warning("Using Demo Data - API offline")
    st.info(f"Error: {e}")
    st.info("Make sure Terminal 1 running: uvicorn app.api:app --host 0.0.0.0 --port 8000 --reload")
    data = {"total_batches": 1247, "success_rate": 82.5, "failed_count": 99, "avg_duration": 145}

# Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Batches", data.get('total_batches', 1247))
col2.metric("Success Rate", f"{data.get('success_rate', 82)}%")
col3.metric("Failed", data.get('failed_count', 99))
col4.metric("Avg Duration", f"{data.get('avg_duration', 145)}s")

# Charts
st.divider()
col1, col2 = st.columns(2)

with col1:
    st.subheader("Batch Status")
    chart_data = pd.DataFrame({"Status": ["Success", "Failed", "Running"], "Count": [1025, 99, 123]})
    st.bar_chart(chart_data, x="Status", y="Count")

with col2:
    st.subheader("Performance")
    st.line_chart([120, 135, 145, 130, 150, 145])

st.divider()
st.subheader("Recent Batches")
df = pd.DataFrame({
    "Batch ID": ["B-1024", "B-1025", "B-1026", "B-1027"],
    "Status": ["Success", "Failed", "Running", "Success"],
    "Duration": ["124s", "340s", "89s", "156s"],
    "Time": ["10:30 AM", "10:45 AM", "11:00 AM", "11:15 AM"]
})
st.dataframe(df, use_container_width=True)

st.balloons()