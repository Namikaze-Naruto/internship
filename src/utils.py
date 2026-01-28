import logging
import os
from . import config

def setup_logging() -> None:
    os.makedirs(config.LOG_DIR, exist_ok=True)
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler(os.path.join(config.LOG_DIR, "scraper.log"), encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
