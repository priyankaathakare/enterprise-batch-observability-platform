import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="ABSA 10 Countries Monitor", layout="wide")

API_URL = "https://enterprise-batch-observability-platform.onrender.com"

st.title("🌍 ABSA Group - Batch Observability (10 Countries)")
st.markdown("**South Africa | Botswana | Ghana | Kenya | Mauritius | Mozambique | Seychelles | Tanzania | Uganda | Zambia**")

try:
    metrics = requests.get(f"{API_URL}/api/v1/metrics", timeout=15).json()
    countries_data = requests.get(f"{API_URL}/api/v1/countries", timeout=15).json()
    st.success("🟢 LIVE DATA - Connected to API")
except Exception as e:
    st.warning(f"🟡 Demo Data - API offline: {e}")
    metrics = {"total_jobs": 830, "success": 705, "failed": 83, "sla_breaches": 42, "total_cost_impact_usd": 1250000}
    countries_data = []

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Jobs", metrics.get("total_jobs", 0))
col2.metric("Success", metrics.get("success", 0))
col3.metric("Failed", metrics.get("failed", 0))
col4.metric("SLA Breaches", metrics.get("sla_breaches", 0))
col5.metric("Cost Impact", f"${metrics.get('total_cost_impact_usd',0):,}")

st.divider()

if countries_data and isinstance(countries_data, list):
    try:
        df_countries = pd.DataFrame(countries_data)
        if not df_countries.empty:
            st.subheader("📊 Country-wise Performance")
            if "country" in df_countries.columns:
                chart_df = df_countries.set_index("country")[["failed", "sla_breaches"]]
                st.bar_chart(chart_df)
            st.dataframe(df_countries, use_container_width=True)
    except Exception as ex:
        st.error(f"Chart error: {ex}")
        st.json(countries_data)
else:
    st.info("Waiting for country data from API...")

st.caption("ABSA Group Enterprise Monitoring | 10 African Nations")