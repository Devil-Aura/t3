import os

# API Credentials
API_ID = int(os.environ.get("API_ID", "22768311"))
API_HASH = os.environ.get("API_HASH", "702d8884f48b42e865425391432b3794")
BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "") # Add your token here when ready

# Owner & Admins
OWNER_ID = int(os.environ.get("OWNER_ID", "6040503076"))
ADMINS = [int(x) for x in os.environ.get("ADMINS", str(OWNER_ID)).split()]

# Database
DB_URI = os.environ.get("DATABASE_URL", "")
DB_NAME = "CrunchyrollVault"

# System
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))
PORT = int(os.environ.get("PORT", "8789"))

# Defaults
DEFAULT_REVOKE_TIME = 1800 # 30 Minutes in seconds
DEFAULT_DELETE_TIME = 1800 # 30 Minutes
START_DELETE_TIME = 900 # 15 Minutes
HELP_DELETE_TIME = 120 # 2 Minutes
ABOUT_DELETE_TIME = 60 # 1 Minute

# Links
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "0")) # Optional default
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "0")) # For backups/logs
