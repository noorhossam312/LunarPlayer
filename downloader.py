import re

import ffmpeg
import yt_dlp

import nice_errors


def sanitize_filename(_filename: str) -> str:
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
    return f"songs/{filename}.ogg"

class Downloader:
    """A static downloader that downloads from YouTube.

    This class is a namespace. It is fully static. It should not be instantiated.
    """

    @staticmethod
    def download(link: str, song_name: str, ydl_opts: dict):
        """Downloads an audio stream from YouTube using FFmpeg and yt-dlp.
        Args:
            link: A string representing the URL of the audio stream.
            song_name: A string representing the song name.
            ydl_opts: A dictionary representing the yt-dlp options.

        Returns:
              The filename of the audio file, or None if something failed.
        """
        filename = sanitize_filename(song_name)

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
            nice_errors.print_error("ferror", f"Failed to fetch audio stream: {e}")
        except ffmpeg.Error as e:
            nice_errors.print_error("ferror", f"FFmpeg failed: {e}")
        except Exception as e:
            nice_errors.print_error("ferror", f"Unexpected error during download: {e}")
