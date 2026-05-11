# =========================================
# utils/youtube.py
# =========================================

import re
import asyncio

from youtube_search import YoutubeSearch

# =========================================
# YOUTUBE CLASS
# =========================================

class YouTube:

    # =====================================
    # CHECK VALID URL
    # =====================================

    @staticmethod
    def is_valid_url(
        text: str
    ):

        patterns = [

            r"(https?://)?(www\.)?"
            r"(youtube\.com|youtu\.be)/",

            r"(https?://)?(www\.)?"
            r"youtube\.com/watch\?v=",

            r"(https?://)?youtu\.be/",

            r"(https?://)?(www\.)?"
            r"youtube\.com/playlist\?list=",

            r"(https?://)?(www\.)?"
            r"youtube\.com/shorts/"
        ]

        return any(
            re.match(pattern, text)
            for pattern in patterns
        )

    # =====================================
    # CHECK PLAYLIST
    # =====================================

    @staticmethod
    def is_playlist(
        text: str
    ):

        return (
            "playlist" in text
            or "list=" in text
        )

    # =====================================
    # SEARCH VIDEO
    # =====================================

    @staticmethod
    async def search(
        query: str,
        limit: int = 10
    ):

        loop = asyncio.get_running_loop()

        def search_sync():

            results = YoutubeSearch(
                query,
                max_results=limit
            ).to_dict()

            return results

        results = await loop.run_in_executor(
            None,
            search_sync
        )

        formatted = []

        for result in results:

            duration = result.get(
                "duration",
                "0:00"
            )

            duration_seconds = 0

            # =============================
            # CONVERT DURATION
            # =============================

            if ":" in duration:

                parts = duration.split(":")

                try:

                    if len(parts) == 2:

                        duration_seconds = (
                            int(parts[0]) * 60
                            + int(parts[1])
                        )

                    elif len(parts) == 3:

                        duration_seconds = (
                            int(parts[0]) * 3600
                            + int(parts[1]) * 60
                            + int(parts[2])
                        )

                except:
                    duration_seconds = 0

            # =============================
            # FORMAT DATA
            # =============================

            formatted.append({

                "title":
                    result.get(
                        "title",
                        "Unknown"
                    ),

                "duration":
                    duration,

                "duration_seconds":
                    duration_seconds,

                "url":
                    f"https://youtube.com"
                    f"{result['url_suffix']}",

                "views":
                    result.get(
                        "views",
                        "N/A"
                    ),

                "channel":
                    result.get(
                        "channel",
                        "Unknown"
                    ),

                "thumbnails":
                    result.get(
                        "thumbnails",
                        []
                    ),

                "id":
                    result.get(
                        "id",
                        ""
                    )
            })

        return formatted

    # =====================================
    # SEARCH SINGLE
    # =====================================

    @staticmethod
    async def search_single(
        query: str
    ):

        results = await YouTube.search(
            query,
            limit=1
        )

        if results:
            return results[0]

        return None


# =========================================
# INSTANCE
# =========================================

youtube = YouTube()

print("✅ YouTube Search Loaded")
