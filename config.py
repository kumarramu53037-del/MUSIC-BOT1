import os
from dotenv import load_dotenv

load_dotenv()

# =========================================
# TELEGRAM API
# =========================================

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
STRING_SESSION = os.getenv("STRING_SESSION", "")

# =========================================
# DATABASE
# =========================================

MONGO_DB_URL = os.getenv("MONGO_DB_URL", "")
MONGO_DB_NAME = os.getenv(
    "MONGO_DB_NAME",
    "ultra_music_bot"
)

# =========================================
# REDIS
# =========================================

REDIS_URL = os.getenv("REDIS_URL", "")

# =========================================
# SPOTIFY
# =========================================

SPOTIFY_CLIENT_ID = os.getenv(
    "SPOTIFY_CLIENT_ID",
    ""
)

SPOTIFY_CLIENT_SECRET = os.getenv(
    "SPOTIFY_CLIENT_SECRET",
    ""
)

# =========================================
# BOT SETTINGS
# =========================================

DEFAULT_VOLUME = int(
    os.getenv("DEFAULT_VOLUME", "100")
)

MAX_DURATION = int(
    os.getenv("MAX_DURATION", "3600")
)

BITRATE = int(
    os.getenv("BITRATE", "128")
)

AUTO_LEAVE_TIME = int(
    os.getenv("AUTO_LEAVE_TIME", "300")
)

LANGUAGE = os.getenv("LANGUAGE", "en")

# =========================================
# SUDO USERS
# =========================================

SUDO_USERS = [
    int(x)
    for x in os.getenv(
        "SUDO_USERS",
        ""
    ).split(",")
    if x
]

# =========================================
# BOT INFO
# =========================================

BOT_NAME = "Ultra Pro Music Bot"

BOT_USERNAME = "ultrapro_music_bot"

ASSISTANT_NAME = "Ultra Assistant"

SUPPORT_GROUP = "@YourSupportGroup"

UPDATES_CHANNEL = "@YourUpdatesChannel"

# =========================================
# DIRECTORIES
# =========================================

DOWNLOAD_DIR = "downloads"

THUMBNAIL_DIR = "thumbnails"

CACHE_DIR = "cache"

LOGS_DIR = "logs"

# =========================================
# AUTO CREATE FOLDERS
# =========================================

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

os.makedirs(THUMBNAIL_DIR, exist_ok=True)

os.makedirs(CACHE_DIR, exist_ok=True)

os.makedirs(LOGS_DIR, exist_ok=True)
