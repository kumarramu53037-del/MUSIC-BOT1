# =========================================
# utils/helpers.py
# =========================================

import asyncio

from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

# =========================================
# CONVERT SECONDS
# =========================================

def seconds_to_min(
    seconds: int
):

    seconds = int(seconds)

    hours = seconds // 3600

    minutes = (
        seconds % 3600
    ) // 60

    seconds = seconds % 60

    if hours > 0:

        return (
            f"{hours}:"
            f"{minutes:02d}:"
            f"{seconds:02d}"
        )

    return (
        f"{minutes:02d}:"
        f"{seconds:02d}"
    )

# =========================================
# GET DURATION TEXT
# =========================================

def get_duration_text(
    seconds: int
):

    try:

        return seconds_to_min(
            int(seconds)
        )

    except:

        return "Unknown"

# =========================================
# PLAY BUTTONS
# =========================================

def stream_markup(
    chat_id: int
):

    buttons = InlineKeyboardMarkup(

        [

            [
                InlineKeyboardButton(
                    "⏸ Pause",
                    callback_data=
                    f"pause_{chat_id}"
                ),

                InlineKeyboardButton(
                    "▶ Resume",
                    callback_data=
                    f"resume_{chat_id}"
                )
            ],

            [
                InlineKeyboardButton(
                    "⏭ Skip",
                    callback_data=
                    f"skip_{chat_id}"
                ),

                InlineKeyboardButton(
                    "⏹ Stop",
                    callback_data=
                    f"stop_{chat_id}"
                )
            ],

            [
                InlineKeyboardButton(
                    "📋 Queue",
                    callback_data=
                    f"queue_{chat_id}"
                )
            ],

            [
                InlineKeyboardButton(
                    "🔊 Vol +",
                    callback_data=
                    f"volup_{chat_id}"
                ),

                InlineKeyboardButton(
                    "🔉 Vol -",
                    callback_data=
                    f"voldown_{chat_id}"
                )
            ],

            [
                InlineKeyboardButton(
                    "❌ Close",
                    callback_data="close"
                )
            ]
        ]
    )

    return buttons

# =========================================
# QUEUE BUTTONS
# =========================================

def queue_markup():

    buttons = InlineKeyboardMarkup(

        [

            [
                InlineKeyboardButton(
                    "❌ Close",
                    callback_data="close"
                )
            ]
        ]
    )

    return buttons

# =========================================
# SETTINGS BUTTONS
# =========================================

def settings_markup(
    chat_id: int
):

    buttons = InlineKeyboardMarkup(

        [

            [
                InlineKeyboardButton(
                    "🔊 Volume +",
                    callback_data=
                    f"volup_{chat_id}"
                ),

                InlineKeyboardButton(
                    "🔉 Volume -",
                    callback_data=
                    f"voldown_{chat_id}"
                )
            ],

            [
                InlineKeyboardButton(
                    "⏸ Pause",
                    callback_data=
                    f"pause_{chat_id}"
                ),

                InlineKeyboardButton(
                    "▶ Resume",
                    callback_data=
                    f"resume_{chat_id}"
                )
            ],

            [
                InlineKeyboardButton(
                    "⏭ Skip",
                    callback_data=
                    f"skip_{chat_id}"
                ),

                InlineKeyboardButton(
                    "⏹ Stop",
                    callback_data=
                    f"stop_{chat_id}"
                )
            ],

            [
                InlineKeyboardButton(
                    "❌ Close",
                    callback_data="close"
                )
            ]
        ]
    )

    return buttons

# =========================================
# AUTO DELETE MESSAGE
# =========================================

async def delete_message_after(
    message,
    seconds: int = 10
):

    await asyncio.sleep(seconds)

    try:

        await message.delete()

    except:
        pass

# =========================================
# PROGRESS BAR
# =========================================

def progress_bar(
    current,
    total,
    length=10
):

    try:

        percent = current / total

    except:
        percent = 0

    filled = int(
        length * percent
    )

    empty = length - filled

    return (
        "█" * filled
        + "░" * empty
    )

# =========================================
# FORMAT FILE SIZE
# =========================================

def format_size(
    size
):

    power = 1024

    n = 0

    labels = [
        "",
        "KB",
        "MB",
        "GB",
        "TB"
    ]

    while size > power:

        size /= power

        n += 1

    return (
        f"{round(size, 2)} "
        f"{labels[n]}"
    )

print("✅ Helpers Loaded")
