import os

BASE_DIR = os.getcwd()

# Directories
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Report File
REPORT_FILE = os.path.join(LOG_DIR, "report.json")

# Logging
LOG_LEVEL = "INFO"
