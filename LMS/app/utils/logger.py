# utils/logger.py
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "LMS.log"

logger = logging.getLogger("LMS")
logger.setLevel(logging.INFO)

# Console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(ch_formatter)

# Rotating file handler (5 MB per file, keep 3 backups)
fh = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3)
fh.setLevel(logging.INFO)
fh.setFormatter(ch_formatter)

# Avoid duplicate handlers on reload
if not logger.handlers:
    logger.addHandler(ch)
    logger.addHandler(fh)
