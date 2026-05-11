# =========================================
# plugins/play.py
# =========================================

import asyncio

from pyrogram import filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from pytgcalls.types.input_stream import (
    AudioPiped
)

from config import (
    DEFAULT_VOLUME,
    MAX_DURATION
)

from utils.youtube import youtube
from utils.downloader import downloader
from utils.database import db

# =========================================
# STORAGE
# =========================================

active_calls = {}
queues = {}

# =========================================
# PLAYER CLASS
# =========================================

class Player:

    def __init__(self, app, call_py):

        self.app = app
        self.call_py = call_py

    # =====================================
    # PLAY SONG
    # =====================================

    async def play_song(
        self,
        message: Message,
        query: str
    ):

        chat_id = message.chat.id

        status = await message.reply(
            "🔍 Searching Song..."
        )

        # ================================
        # SEARCH
        # ================================

        result = await youtube.search(
            query,
            limit=1
        )

        if not result:

            return await status.edit(
                "❌ No Results Found"
            )

        data = result[0]

        title = data["title"]

        url = (
            f"https://youtube.com"
            f"{data['url_suffix']}"
        )

        duration = data.get(
            "duration",
            "Unknown"
        )

        thumbnail = ""

        try:
            thumbnail = data["thumbnails"][0]
        except:
            pass

        # ================================
        # GET STREAM
        # ================================

        stream = await downloader.get_stream(
            url
        )

        song = {
            "title": title,
            "url": url,
            "duration": duration,
            "thumbnail": thumbnail,
            "stream": stream,
            "requested_by": message.from_user.id,
            "requested_name": message.from_user.first_name
        }

        # ================================
        # CREATE QUEUE
        # ================================

        if chat_id not in queues:
            queues[chat_id] = []

        queues[chat_id].append(song)

        # ================================
        # JOIN VC
        # ================================

        if chat_id not in active_calls:

            try:

                await self.call_py.join_group_call(
                    chat_id,
                    AudioPiped(stream)
                )

                active_calls[chat_id] = {
                    "volume": DEFAULT_VOLUME,
                    "current": song
                }

                await self.send_now_playing(
                    status,
                    song,
                    chat_id
                )

            except Exception as e:

                return await status.edit(
                    f"❌ VC Join Failed\n\n{e}"
                )

        else:

            position = len(queues[chat_id])

            await status.edit(
                f"✅ Added To Queue\n\n"
                f"🎵 {title}\n"
                f"📍 Position: {position}"
            )

    # =====================================
    # NOW PLAYING MESSAGE
    # =====================================

    async def send_now_playing(
        self,
        msg,
        song,
        chat_id
    ):

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⏸ Pause",
                        callback_data=f"pause_{chat_id}"
                    ),

                    InlineKeyboardButton(
                        "▶ Resume",
                        callback_data=f"resume_{chat_id}"
                    )
                ],

                [
                    InlineKeyboardButton(
                        "⏭ Skip",
                        callback_data=f"skip_{chat_id}"
                    ),

                    InlineKeyboardButton(
                        "⏹ Stop",
                        callback_data=f"stop_{chat_id}"
                    )
                ],

                [
                    InlineKeyboardButton(
                        "📋 Queue",
                        callback_data=f"queue_{chat_id}"
                    )
                ]
            ]
        )

        text = (
            f"🎵 **Now Playing**\n\n"

            f"🏷 Title: {song['title']}\n"

            f"⏱ Duration: {song['duration']}\n"

            f"👤 Requested By: "
            f"{song['requested_name']}\n\n"

            f"🔗 [YouTube Link]"
            f"({song['url']})"
        )

        await msg.edit(
            text,
            reply_markup=buttons,
            disable_web_page_preview=True
        )

    # =====================================
    # SKIP SONG
    # =====================================

    async def skip(self, chat_id):

        if chat_id not in queues:
            return

        if len(queues[chat_id]) <= 1:

            return await self.stop(chat_id)

        queues[chat_id].pop(0)

        next_song = queues[chat_id][0]

        await self.call_py.change_stream(
            chat_id,
            AudioPiped(
                next_song["stream"]
            )
        )

        active_calls[chat_id]["current"] = next_song

        await self.app.send_message(
            chat_id,
            f"⏭ Skipped\n\n"
            f"🎵 Now Playing:\n"
            f"{next_song['title']}"
        )

    # =====================================
    # STOP
    # =====================================

    async def stop(self, chat_id):

        try:

            await self.call_py.leave_group_call(
                chat_id
            )

        except:
            pass

        if chat_id in queues:
            queues[chat_id] = []

        if chat_id in active_calls:
            del active_calls[chat_id]

    # =====================================
    # PAUSE
    # =====================================

    async def pause(self, chat_id):

        try:

            await self.call_py.pause_stream(
                chat_id
            )

        except:
            pass

    # =====================================
    # RESUME
    # =====================================

    async def resume(self, chat_id):

        try:

            await self.call_py.resume_stream(
                chat_id
            )

        except:
            pass

    # =====================================
    # VOLUME
    # =====================================

    async def set_volume(
        self,
        chat_id,
        volume
    ):

        volume = max(
            1,
            min(volume, 200)
        )

        try:

            await self.call_py.change_volume_call(
                chat_id,
                volume
            )

            active_calls[chat_id][
                "volume"
            ] = volume

        except:
            pass

        return volume


# =========================================
# PLAYER INSTANCE
# =========================================

player = None

# =========================================
# REGISTER
# =========================================

def register(app, call_py):

    global player

    player = Player(
        app,
        call_py
    )

    # =====================================
    # PLAY COMMAND
    # =====================================

    @app.on_message(
        filters.command(
            ["play", "p"],
            prefixes=["/", ".", "!"]
        )
    )
    async def play_command(
        client,
        message: Message
    ):

        if len(message.command) < 2:

            return await message.reply(
                "Usage:\n/play song name"
            )

        query = message.text.split(
            None,
            1
        )[1]

        await player.play_song(
            message,
            query
        )

    # =====================================
    # SKIP
    # =====================================

    @app.on_message(
        filters.command(
            ["skip", "next"],
            prefixes=["/", ".", "!"]
        )
    )
    async def skip_command(
        client,
        message: Message
    ):

        await player.skip(
            message.chat.id
        )

        await message.reply(
            "⏭ Song Skipped"
        )

    # =====================================
    # STOP
    # =====================================

    @app.on_message(
        filters.command(
            ["stop", "end"],
            prefixes=["/", ".", "!"]
        )
    )
    async def stop_command(
        client,
        message: Message
    ):

        await player.stop(
            message.chat.id
        )

        await message.reply(
            "⏹ VC Ended"
        )

    # =====================================
    # PAUSE
    # =====================================

    @app.on_message(
        filters.command(
            ["pause"],
            prefixes=["/", ".", "!"]
        )
    )
    async def pause_command(
        client,
        message: Message
    ):

        await player.pause(
            message.chat.id
        )

        await message.reply(
            "⏸ Paused"
        )

    # =====================================
    # RESUME
    # =====================================

    @app.on_message(
        filters.command(
            ["resume"],
            prefixes=["/", ".", "!"]
        )
    )
    async def resume_command(
        client,
        message: Message
    ):

        await player.resume(
            message.chat.id
        )

        await message.reply(
            "▶ Resumed"
        )

    # =====================================
    # QUEUE
    # =====================================

    @app.on_message(
        filters.command(
            ["queue", "q"],
            prefixes=["/", ".", "!"]
        )
    )
    async def queue_command(
        client,
        message: Message
    ):

        chat_id = message.chat.id

        if (
            chat_id not in queues
            or not queues[chat_id]
        ):

            return await message.reply(
                "📋 Queue Empty"
            )

        text = "📋 Current Queue\n\n"

        for i, song in enumerate(
            queues[chat_id],
            start=1
        ):

            text += (
                f"{i}. "
                f"{song['title']}\n"
            )

        await message.reply(text)

    print("✅ Play Plugin Loaded")
