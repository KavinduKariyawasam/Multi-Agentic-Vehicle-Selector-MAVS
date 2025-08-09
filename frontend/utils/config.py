import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_TIMEOUT_SECONDS = int(os.getenv("API_TIMEOUT_SECONDS", "300"))  # was 60
