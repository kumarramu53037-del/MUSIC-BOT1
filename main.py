import asyncio
import logging

from pyrogram import Client
from pyrogram.idle import idle

from pytgcalls import PyTgCalls

from config import (
    API_ID,
    API_HASH,
    BOT_TOKEN,
    STRING_SESSION,
    BOT_NAME
)

# =========================================
# LOGGING
# =========================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

LOGGER = logging.getLogger(BOT_NAME)

# =========================================
# BOT CLIENT
# =========================================

app = Client(
    name="UltraMusicBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=200,
    sleep_threshold=15
)

# =========================================
# ASSISTANT CLIENT
# =========================================

assistant = Client(
    name="UltraAssistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION,
    workers=200,
    sleep_threshold=15
)

# =========================================
# PYTGCALLS
# =========================================

call_py = PyTgCalls(assistant)

# =========================================
# START FUNCTION
# =========================================

async def start():

    LOGGER.info("Starting Bot...")

    # Start Bot
    await app.start()

    LOGGER.info("Bot Started")

    # Start Assistant
    await assistant.start()

    LOGGER.info("Assistant Started")

    # Start PyTgCalls
    await call_py.start()

    LOGGER.info("PyTgCalls Started")

    # =====================================
    # IMPORT PLUGINS
    # =====================================

    from plugins.play import register as play_register
    from plugins.callbacks import register as cb_register
    from plugins.admin import register as admin_register

    # Register Plugins
    play_register(app, call_py)

    cb_register(app)

    admin_register(app)

    LOGGER.info("Plugins Loaded")

    # =====================================
    # BOT INFO
    # =====================================

    me = await app.get_me()

    LOGGER.info(
        f"Bot Running As @{me.username}"
    )

    print("===================================")
    print(f"{BOT_NAME} Started Successfully")
    print("===================================")

    await idle()

    # =====================================
    # STOP
    # =====================================

    LOGGER.info("Stopping Bot...")

    await call_py.stop()

    await assistant.stop()

    await app.stop()

    LOGGER.info("Bot Stopped")


# =========================================
# RUN
# =========================================

if __name__ == "__main__":

    asyncio.get_event_loop().run_until_complete(
        start()
    )
