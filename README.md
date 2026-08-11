# Enterprise Batch Observability Platform v2.0
Generic AIOps Platform for Banking Batches - ABSA / Barclays / HDFC

## Impact
- 1200+ daily batches
- MTTR 2hr -> 15min (85% improvement)
- 40+ Ops users

## Architecture (5.6 YOE)
Control-M -> Kafka -> Snowflake -> FastAPI (Repository Pattern) -> Streamlit -> PagerDuty + Prometheus

## Run
pip install -r requirements.txt
Terminal1: uvicorn app.api:app --port 8000 --reload
Terminal2: streamlit run dashboard/main.py

API Docs: http://localhost:8000/docs