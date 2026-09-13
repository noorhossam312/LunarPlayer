import re
import os

import ffmpeg
from pytubefix import YouTube

import nice_errors


def sanitize_filename(_filename: str, return_raw_filename: bool=False) -> str:
    """Filters filename for illegal characters.

    Args:
        _filename: A string representing the original filename.

    Returns:
        The final sanitized filename.
    """
    filename = re.sub(r'[\\/:*?<>|"]', '_', _filename).strip(". ")
    filename = re.sub(r'[^\x00-\x7F]+', '', filename)
    reserved = {"CON", "PRN", "AUX", "NUL"} | {f"COM{i}" for i in range(1, 10)} | {f"LPT{i}" for i in range(1, 10)}
    if filename.upper() in reserved:
        nice_errors.print_error("warn", "Song name is illegal, please pick a custom filename.")
        filename = input(f"Current: {filename}\n> ")

    if return_raw_filename:
        return filename
    return f"songs/{filename}.ogg"

class Downloader:
    """A static downloader that downloads from YouTube.

    This class is a namespace. It should not be instantiated.
    """

    @staticmethod
    def download(link: str, song_name: str):
        """Downloads an audio stream from YouTube using FFmpeg and yt-dlp.
        Args:
            link: A string representing the URL of the audio stream.
            song_name: A string representing the song name.

        Returns:
              The filename of the audio file, or None if something failed.
        """
        raw_filename = sanitize_filename(song_name, True)
        filename = f"songs/{raw_filename}.ogg"

        try:
            yt = YouTube(link)
            stream = yt.streams.get_audio_only()
            stream.download(output_path="songs_temp", filename=raw_filename + ".tmp")

            print("Converting temp file to ogg using ffmpeg...")
            ffmpeg.input(f"songs_temp/{raw_filename}.tmp").output(
                filename,
                format="ogg",
                acodec="libvorbis",
                audio_bitrate="320k",
                loglevel="error"
            ).run()

            print("Download completed.")
            return filename
        except ffmpeg.Error as e:
            nice_errors.print_error("ferror", f"FFmpeg failed: {e}")
        except Exception as e:
            nice_errors.print_error("ferror", f"Unexpected error during download: {e}")
        finally:
            print("Deleting temp file...")
            os.remove(f"songs_temp/{raw_filename}.tmp")
