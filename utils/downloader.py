# =========================================
# utils/downloader.py
# =========================================

import os
import asyncio
import yt_dlp

from config import (
    DOWNLOAD_DIR,
    MAX_DURATION
)

# =========================================
# DOWNLOADER CLASS
# =========================================

class Downloader:

    def __init__(self):

        self.download_dir = DOWNLOAD_DIR

    # =====================================
    # GET STREAM URL
    # =====================================

    async def get_stream(
        self,
        url: str
    ):

        loop = asyncio.get_running_loop()

        ydl_opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "nocheckcertificate": True,
            "ignoreerrors": False,
            "no_warnings": True,
            "geo_bypass": True
        }

        def extract():

            with yt_dlp.YoutubeDL(
                ydl_opts
            ) as ydl:

                info = ydl.extract_info(
                    url,
                    download=False
                )

                return info["url"]

        return await loop.run_in_executor(
            None,
            extract
        )

    # =====================================
    # GET INFO
    # =====================================

    async def get_info(
        self,
        url: str
    ):

        loop = asyncio.get_running_loop()

        ydl_opts = {
            "quiet": True,
            "nocheckcertificate": True,
            "ignoreerrors": False,
            "no_warnings": True,
            "geo_bypass": True
        }

        def extract():

            with yt_dlp.YoutubeDL(
                ydl_opts
            ) as ydl:

                info = ydl.extract_info(
                    url,
                    download=False
                )

                return info

        return await loop.run_in_executor(
            None,
            extract
        )

    # =====================================
    # DOWNLOAD AUDIO
    # =====================================

    async def download_audio(
        self,
        url: str,
        quality: str = "320"
    ):

        loop = asyncio.get_running_loop()

        ydl_opts = {

            "format": "bestaudio/best",

            "outtmpl":
                f"{self.download_dir}/%(title)s.%(ext)s",

            "quiet": True,

            "nocheckcertificate": True,

            "ignoreerrors": False,

            "no_warnings": True,

            "geo_bypass": True,

            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": quality
                }
            ]
        }

        def download():

            with yt_dlp.YoutubeDL(
                ydl_opts
            ) as ydl:

                info = ydl.extract_info(
                    url,
                    download=True
                )

                file_path = (
                    f"{self.download_dir}/"
                    f"{info['title']}.mp3"
                )

                return info, file_path

        return await loop.run_in_executor(
            None,
            download
        )

    # =====================================
    # DOWNLOAD VIDEO
    # =====================================

    async def download_video(
        self,
        url: str,
        quality: str = "720"
    ):

        loop = asyncio.get_running_loop()

        ydl_opts = {

            "format":
                f"bestvideo[height<={quality}]"
                f"+bestaudio/best",

            "merge_output_format": "mp4",

            "outtmpl":
                f"{self.download_dir}/%(title)s.%(ext)s",

            "quiet": True,

            "nocheckcertificate": True,

            "ignoreerrors": False,

            "no_warnings": True,

            "geo_bypass": True
        }

        def download():

            with yt_dlp.YoutubeDL(
                ydl_opts
            ) as ydl:

                info = ydl.extract_info(
                    url,
                    download=True
                )

                file_path = (
                    f"{self.download_dir}/"
                    f"{info['title']}.mp4"
                )

                return info, file_path

        return await loop.run_in_executor(
            None,
            download
        )

    # =====================================
    # CLEAN FILE
    # =====================================

    async def cleanup(
        self,
        file_path: str
    ):

        try:

            if os.path.exists(file_path):

                os.remove(file_path)

                return True

        except:
            return False

    # =====================================
    # CHECK DURATION
    # =====================================

    async def check_duration(
        self,
        url: str
    ):

        info = await self.get_info(url)

        duration = info.get(
            "duration",
            0
        )

        if duration > MAX_DURATION:
            return False

        return True


# =========================================
# INSTANCE
# =========================================

downloader = Downloader()

print("✅ Downloader Loaded")
