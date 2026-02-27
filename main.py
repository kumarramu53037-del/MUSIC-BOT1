import os
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio
import yt_dlp
import asyncio

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SESSION_STRING = os.getenv("SESSION_STRING")

# Bot Client
bot = Client(
    "musicbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Assistant Client
assistant = Client(
    "assistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

call = PyTgCalls(assistant)


@bot.on_message(filters.command("start"))
async def start(_, message: Message):
    await message.reply_text("🎧 VC Music Bot Online Hai!")


@bot.on_message(filters.command("play"))
async def play(_, message: Message):

    if len(message.command) < 2:
        return await message.reply_text("❌ Song name do!\nExample: /play kesariya")

    query = " ".join(message.command[1:])

    await message.reply_text("🔎 Searching...")

    ydl_opts = {
        "format": "bestaudio",
        "quiet": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)["entries"][0]
            url = info["url"]
            title = info["title"]

        await call.join_group_call(
            message.chat.id,
            AudioPiped(url, HighQualityAudio())
        )

        await message.reply_text(f"▶️ Playing: {title}")

    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")


@bot.on_message(filters.command("stop"))
async def stop(_, message: Message):
    try:
        await call.leave_group_call(message.chat.id)
        await message.reply_text("⏹ Stopped Playing.")
    except:
        await message.reply_text("❌ Kuch play hi nahi ho raha.")


async def main():
    await bot.start()
    await assistant.start()
    await call.start()
    print("Music Bot Started")
    await asyncio.Event().wait()


asyncio.run(main())
