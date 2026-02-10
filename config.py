import os
from os import environ

# Credentials
API_ID = int(environ.get("API_ID", "0")) # Your API ID
API_HASH = environ.get("API_HASH", "0") # Your API HASH
BOT_TOKEN = environ.get("BOT_TOKEN", "") # Your Bot Token
OWNER_ID = int(environ.get("OWNER_ID", "6040503076"))

# Database
DATABASE_URL = environ.get("DATABASE_URL", "") # Your MongoDB URL
DATABASE_NAME = environ.get("DATABASE_NAME", "LinkShareBot")

# Channel Logs (Optional)
LOG_CHANNEL = int(environ.get("LOG_CHANNEL", "0")) 

# Default Admins
ADMINS = [OWNER_ID]
