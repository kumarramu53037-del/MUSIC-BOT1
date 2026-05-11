# =========================================
# plugins/admin.py
# =========================================

import io
import sys
import time
import traceback
import asyncio
import psutil

from pyrogram import filters
from pyrogram.types import Message

from config import (
    SUDO_USERS,
    BOT_NAME
)

from utils.database import db
from plugins.play import (
    active_calls,
    queues
)

# =========================================
# REGISTER
# =========================================

def register(app):

    START_TIME = time.time()

    # =====================================
    # PING COMMAND
    # =====================================

    @app.on_message(
        filters.command(
            ["ping"],
            prefixes=["/", ".", "!"]
        )
    )
    async def ping_command(
        client,
        message: Message
    ):

        start = time.time()

        msg = await message.reply(
            "🏓 Pinging..."
        )

        end = time.time()

        ping = round(
            (end - start) * 1000
        )

        text = (
            f"🏓 Pong!\n\n"
            f"⚡ Speed: {ping} ms"
        )

        await msg.edit(text)

    # =====================================
    # STATS COMMAND
    # =====================================

    @app.on_message(
        filters.command(
            ["stats"],
            prefixes=["/", ".", "!"]
        )
    )
    async def stats_command(
        client,
        message: Message
    ):

        stats = await db.get_stats()

        cpu = psutil.cpu_percent()

        ram = psutil.virtual_memory().percent

        uptime = time.time() - START_TIME

        uptime = int(uptime)

        hours = uptime // 3600
        minutes = (uptime % 3600) // 60
        seconds = uptime % 60

        text = (
            f"📊 **{BOT_NAME} Stats**\n\n"

            f"👥 Users: {stats['users']}\n"

            f"🏘 Groups: {stats['
