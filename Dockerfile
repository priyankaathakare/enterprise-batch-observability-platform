FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt
COPY..
EXPOSE 8000 10000
CMD uvicorn app.api:app --host 0.0.0.0 --port 8000 & streamlit run dashboard/main.py --server.port 10000 --server.address 0.0.0.0 --server.headless=true