# =========================================
# plugins/callbacks.py
# =========================================

from pyrogram import Client

from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from plugins.play import (
    player,
    queues,
    active_calls
)

# =========================================
# REGISTER
# =========================================

def register(app: Client):

    # =====================================
    # CALLBACK HANDLER
    # =====================================

    @app.on_callback_query()
    async def callback_handler(
        client: Client,
        query: CallbackQuery
    ):

        data = query.data

        # =================================
        # STOP
        # =================================

        if data.startswith("stop_"):

            chat_id = int(
                data.split("_")[1]
            )

            await player.stop(chat_id)

            await query.message.edit(
                "⏹ Music Stopped\n\n"
                "🚪 Left Voice Chat"
            )

            return await query.answer()

        # =================================
        # PAUSE
        # =================================

        elif data.startswith("pause_"):

            chat_id = int(
                data.split("_")[1]
            )

            await player.pause(chat_id)

            await query.answer(
                "⏸ Music Paused"
            )

        # =================================
        # RESUME
        # =================================

        elif data.startswith("resume_"):

            chat_id = int(
                data.split("_")[1]
            )

            await player.resume(chat_id)

            await query.answer(
                "▶ Music Resumed"
            )

        # =================================
        # SKIP
        # =================================

        elif data.startswith("skip_"):

            chat_id = int(
                data.split("_")[1]
            )

            await player.skip(chat_id)

            await query.answer(
                "⏭ Song Skipped"
            )

        # =================================
        # QUEUE
        # =================================

        elif data.startswith("queue_"):

            chat_id = int(
                data.split("_")[1]
            )

            if (
                chat_id not in queues
                or not queues[chat_id]
            ):

                return await query.answer(
                    "📋 Queue Empty",
                    show_alert=True
                )

            text = (
                "📋 Current Queue\n\n"
            )

            for i, song in enumerate(
                queues[chat_id],
                start=1
            ):

                text += (
                    f"{i}. "
                    f"{song['title']}\n"
                )

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

            await query.message.edit(
                text,
                reply_markup=buttons
            )

        # =================================
        # CLOSE
        # =================================

        elif data == "close":

            await query.message.delete()

            await query.answer()

        # =================================
        # VOLUME UP
        # =================================

        elif data.startswith("volup_"):

            chat_id = int(
                data.split("_")[1]
            )

            current = active_calls.get(
                chat_id,
                {}
            ).get("volume", 100)

            new_volume = min(
                current + 10,
                200
            )

            await player.set_volume(
                chat_id,
                new_volume
            )

            await query.answer(
                f"🔊 Volume: {new_volume}%"
            )

        # =================================
        # VOLUME DOWN
        # =================================

        elif data.startswith("voldown_"):

            chat_id = int(
                data.split("_")[1]
            )

            current = active_calls.get(
                chat_id,
                {}
            ).get("volume", 100)

            new_volume = max(
                current - 10,
                1
            )

            await player.set_volume(
                chat_id,
                new_volume
            )

            await query.answer(
                f"🔉 Volume: {new_volume}%"
            )

    print("✅ Callback Plugin Loaded")
