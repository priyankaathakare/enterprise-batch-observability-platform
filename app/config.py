import os
class Settings:
    APP_NAME = "Enterprise Batch Observability Platform"
    SQLITE_PATH = os.path.join(os.getcwd(), "batch_jobs.db")
    API_URL = os.getenv("API_URL", "http://localhost:8000")

settings = Settings()