# =========================================
# plugins/start.py
# =========================================

from pyrogram import filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from config import (
    BOT_NAME,
    SUPPORT_GROUP,
    UPDATES_CHANNEL
)

# =========================================
# REGISTER
# =========================================

def register(app):

    # =====================================
    # START COMMAND
    # =====================================

    @app.on_message(
        filters.command(
            ["start"],
            prefixes=["/", ".", "!"]
        )
    )
    async def start_command(
        client,
        message: Message
    ):

        user = message.from_user

        text = f"""
╔══════════════════════════════╗
║ 🎵 Welcome To {BOT_NAME} 🎵 ║
╚══════════════════════════════╝

👋 Hello {user.mention}

🔥 Advanced Telegram VC Music Bot

━━━━━━━━━━━━━━━━━━━

🎧 Fast Voice Chat Streaming
⚡ Ultra Smooth Music
📋 Queue System
🔊 Volume Control
⏸ Pause / Resume
⏭ Skip Feature
🎶 YouTube Support
🚀 High Quality Audio

━━━━━━━━━━━━━━━━━━━

📌 Available Commands:

/play - Play Music
/pause - Pause Music
/resume - Resume Music
/skip - Skip Song
/stop - Stop Music
/queue - Show Queue
/ping - Check Speed
/stats - Bot Stats

━━━━━━━━━━━━━━━━━━━

💖 Powered By Ultra Music
"""

        buttons = InlineKeyboardMarkup(

            [

                [

                    InlineKeyboardButton(
                        "➕ Add Me",
                        url=(
                            "https://t.me/"
                            f"{client.me.username}"
                            "?startgroup=true"
                        )
                    )

                ],

                [

                    InlineKeyboardButton(
                        "📢 Updates",
                        url=f"https://t.me/{UPDATES_CHANNEL.replace('@', '')}"
                    ),

                    InlineKeyboardButton(
                        "💬 Support",
                        url=f"https://t.me/{SUPPORT_GROUP.replace('@', '')}"
                    )

                ],

                [

                    InlineKeyboardButton(
                        "📚 Commands",
                        callback_data="commands"
                    )

                ]

            ]
        )

        await message.reply_photo(
            photo="https://graph.org/file/8d7c0bdb6b7d7e4c6d9f2.jpg",
            caption=text,
            reply_markup=buttons
        )

    # =====================================
    # HELP COMMAND
    # =====================================

    @app.on_message(
        filters.command(
            ["help"],
            prefixes=["/", ".", "!"]
        )
    )
    async def help_command(
        client,
        message: Message
    ):

        text = """
🎵 Music Commands

/play song name
/pause
/resume
/skip
/stop
/queue
/volume 1-200

━━━━━━━━━━━━━━━━━━━

⚙ Admin Commands

/ping
/stats
/broadcast
/eval
/sh

━━━━━━━━━━━━━━━━━━━

🔥 Enjoy High Quality Music
"""

        await message.reply(
            text
        )

    print("✅ Start Plugin Loaded")
