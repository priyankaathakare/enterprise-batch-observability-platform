import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="ABSA 10 Countries Monitor", layout="wide")

API_URL = "https://enterprise-batch-observability-platform.onrender.com"

st.title("🌍 ABSA Group - Batch Observability (10 Countries)")
st.markdown("**South Africa | Botswana | Ghana | Kenya | Mauritius | Mozambique | Seychelles | Tanzania | Uganda | Zambia**")

try:
    metrics = requests.get(f"{API_URL}/api/v1/metrics", timeout=10).json()
    countries_data = requests.get(f"{API_URL}/api/v1/countries", timeout=10).json()
    st.success("🟢 LIVE DATA - Connected to API")
except:
    st.warning("🟡 Demo Data - API offline, showing local data")
    # fallback will be handled by API itself
    metrics = {"total_jobs": 830, "success": 705, "failed": 83, "sla_breaches": 42, "total_cost_impact_usd": 1250000}
    countries_data = []

# Top metrics
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Jobs", metrics.get("total_jobs", 0))
col2.metric("Success", metrics.get("success", 0))
col3.metric("Failed", metrics.get("failed", 0), delta_color="inverse")
col4.metric("SLA Breaches", metrics.get("sla_breaches", 0), delta_color="inverse")
col5.metric("Cost Impact", f"${metrics.get('total_cost_impact_usd',0):,}")

st.divider()

# Country filter
if countries_data:
    df_countries = pd.DataFrame(countries_data)
    st.subheader("📊 Country-wise Performance")
    st.bar_chart(df_countries.set_index("country")[["failed", "sla_breaches"]])

    st.dataframe(df_countries, use_container_width=True)

    # Country dropdown
    selected = st.selectbox("Select Country for Details", df_countries['country'].tolist())
    if selected:
        try:
            detail = requests.get(f"{API_URL}/api/v1/country/{selected}", timeout=10).json()
            st.write(f"### Jobs in {selected}")
            st.dataframe(pd.DataFrame(detail).head(20))
        except:
            pass

st.divider()
st.caption("ABSA Group Enterprise Monitoring | Built for 10 African Nations | Senior Project")