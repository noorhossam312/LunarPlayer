import re

import ffmpeg
import yt_dlp

import nice_errors
from add_tools_to_path import add_tools_to_path


class Downloader:
    def __init__(self, add_to_path=True):
        if add_to_path:
            add_tools_to_path()

    def download(self, link: str, song_name: str, ydl_opts: dict):
        filename = self.sanitize_filename(song_name)

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=False)
                stream = info["url"]

            print("Converting audio stream to ogg using ffmpeg...")
            ffmpeg.input(stream).output(filename, format="ogg", acodec="libvorbis", audio_bitrate="320k",
                                        loglevel="error").run()

            print("Download completed.")
            return filename
        except yt_dlp.utils.DownloadError as e:
            nice_errors.print_error("ferror", f"Failed to fetch stream: {e}")
        except ffmpeg.Error as e:
            nice_errors.print_error("ferror", f"FFmpeg conversion failed: {e}")
        except Exception as e:
            nice_errors.print_error("ferror", f"Unexpected error during download: {e}")

    @staticmethod
    def sanitize_filename(_filename):
        filename = re.sub(r'[\\/:*?<>|"]', '_', _filename).strip(". ")
        filename = re.sub(r'[^\x00-\x7F]+', '', filename)
        reserved = {"CON", "PRN", "AUX", "NUL"} | {f"COM{i}" for i in range(1, 10)} | {f"LPT{i}" for i in range(1, 10)}
        if filename.upper() in reserved:
            nice_errors.print_error("warn", "Song name is illegal, please pick a custom filename.")
            filename = input(f"Current: {filename}\n> ")
        return f"songs/{filename}.ogg"
