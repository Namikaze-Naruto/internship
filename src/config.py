import os
from dotenv import load_dotenv

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data", "internships")
LOG_DIR = os.path.join(ROOT_DIR, "logs")

load_dotenv(os.path.join(ROOT_DIR, ".env"))

HOURS_LOOKBACK = int(os.getenv("HOURS_LOOKBACK", "24"))
API_PER_PAGE = int(os.getenv("API_PER_PAGE", "20"))
REQUEST_DELAY_SECONDS = float(os.getenv("REQUEST_DELAY_SECONDS", "2"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
API_BASE_URL = os.getenv("API_BASE_URL", "")
