import sys
import os
import tarfile
import zipfile
import stat
from urllib.request import urlretrieve
from zipfile import ZipFile

if __name__ == "__main__":
    print("Checking platform...")
    platform = sys.platform
    if platform == "win32":
        ffmpeg_link = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-lgpl.zip"
        deno_link = "https://github.com/denoland/deno/releases/download/v2.9.5/deno-x86_64-pc-windows-msvc.zip"
    elif platform == "linux":
        ffmpeg_link = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-lgpl.tar.xz"
        deno_link = "https://github.com/denoland/deno/releases/download/v2.9.5/deno-x86_64-unknown-linux-gnu.zip"

    print("Fetching ffmpeg...")
    urlretrieve(ffmpeg_link, "ffmpeg.zip" if platform == "win32" else "ffmpeg.tar.xz")

    print("Fetching deno...")
    urlretrieve(deno_link, "deno.zip")

    print("Extracting ffmpeg...")
    if platform == "win32":
        with zipfile.ZipFile("ffmpeg.zip", "r") as archive:
            archive.extractall("ffmpeg/")

    elif platform == "linux":
        with tarfile.open("ffmpeg.tar.xz", "r") as archive:
            archive.extractall("ffmpeg/")

    print("Extracting deno...")
    with ZipFile("deno.zip", "r") as archive:
        archive.extractall("deno/")

    print("Cleaning up...")
    os.remove("ffmpeg.zip") if platform == "win32" else os.remove("ffmpeg.tar.xz")
    os.remove("deno.zip")
    if platform == "linux":
        deno_stat = os.stat("deno/deno")
        os.chmod(deno_stat, deno_stat.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)

    print("Done!")

def add_tool_files_to_path():
    if __name__ == "__main__":
        ffmpeg_bin = os.path.abspath(f"ffmpeg/ffmpeg-master-latest-{'win64' if platform == 'win32' else 'linux64'}-lgpl/bin/")
        deno_bin = os.path.abspath("deno/")
        os.environ["PATH"] = ffmpeg_bin + os.pathsep + deno_bin + os.pathsep + os.environ["PATH"]
    else:
        ffmpeg_bin = os.path.abspath("installer/ffmpeg/ffmpeg/bin/")
        deno_bin = os.path.abspath("installer/deno/")
        os.environ["PATH"] = ffmpeg_bin + os.pathsep + deno_bin + os.pathsep + os.environ["PATH"]


