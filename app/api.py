from fastapi import FastAPI
import pandas as pd
import os

app = FastAPI(
    title="ABSA Batch Observability - 10 Countries",
    description="Enterprise Batch Monitoring for ABSA Group - 10 African Countries",
    version="3.0.0"
)

# Load data
DATA_FILE = "absa_batch_data_10_countries.csv"
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    # Fallback demo data for 10 countries
    import random
    from datetime import datetime, timedelta
    countries = ["South Africa", "Botswana", "Ghana", "Kenya", "Mauritius", "Mozambique", "Seychelles", "Tanzania", "Uganda", "Zambia"]
    data = []
    for c in countries:
        for i in range(80):
            status = random.choices(["SUCCESS", "FAILED", "RUNNING"], weights=[85,10,5])[0]
            data.append({
                "job_id": f"{c[:2].upper()}-{1000+i}", "job_name": random.choice(["RTGS","NEFT","CASA","Loan","ATM"]),
                "country": c, "status": status,
                "sla_status": "BREACH" if status=="FAILED" and random.random()>0.5 else "OK",
                "duration_mins": random.randint(5,240),
                "cost_impact_usd": random.randint(1000,50000) if status=="FAILED" else 0,
                "timestamp": datetime.now().isoformat()
            })
    df = pd.DataFrame(data)

@app.get("/")
def root():
    return {"message": "ABSA Group - 10 Countries Batch Observability LIVE", "countries": 10, "total_jobs": len(df)}

@app.get("/health")
def health():
    return {"status": "healthy", "countries": 10}

@app.get("/api/v1/metrics")
def metrics():
    return {
        "total_jobs": len(df),
        "success": len(df[df['status']=="SUCCESS"]),
        "failed": len(df[df['status']=="FAILED"]),
        "running": len(df[df['status']=="RUNNING"]),
        "sla_breaches": len(df[df['sla_status']=="BREACH"]),
        "total_cost_impact_usd": int(df['cost_impact_usd'].sum()),
        "countries": 10
    }

@app.get("/api/v1/countries")
def countries_list():
    result = []
    for country in df['country'].unique():
        cdf = df[df['country']==country]
        result.append({
            "country": country,
            "total_jobs": len(cdf),
            "failed": len(cdf[cdf['status']=="FAILED"]),
            "sla_breaches": len(cdf[cdf['sla_status']=="BREACH"]),
            "cost_impact_usd": int(cdf['cost_impact_usd'].sum())
        })
    return result

@app.get("/api/v1/failed-jobs")
def failed_jobs():
    return df[df['status']=="FAILED"].head(100).to_dict(orient="records")

@app.get("/api/v1/sla-breaches")
def sla_breaches():
    return df[df['sla_status']=="BREACH"].head(100).to_dict(orient="records")

@app.get("/api/v1/country/{country_name}")
def country_detail(country_name: str):
    cdf = df[df['country']==country_name]
    return cdf.to_dict(orient="records")