"""Imports"""
import sys
import os
import time
import threading
import ffmpeg
import yt_dlp
import pygame
import readchar
import questionary
from rich.console import Console
from youtube_search import YoutubeSearch

console = Console()

"""Checks"""
if getattr(sys, 'frozen', False):  # This check is to check if the user is running the program through the source or the binary which will be compiled soon.
    binary = True
else:
    binary = False

if sys.platform == "darwin":
    console.input(
        f"[red]{'!!!FATAL ERROR!!!'.center(console.width)}[/red]\n"
        f"{'This program does not have support for MacOS. The program will terminate.'.center(console.width)}\n"
        f"{'Press Enter to terminate.'.center(console.width)}"
    )
    sys.exit(1)

platform = sys.platform

if platform == "linux":
    ffmpeg_path = "tools/linux/ffmpeg/bin/ffmpeg" if not binary else "../../../tools/linux/ffmpeg/bin/ffmpeg"
    deno_path = "tools/linux/deno/deno" if not binary else "../../../tools/linux/deno/deno"

if platform == "win32":
    ffmpeg_path = "tools/win32/ffmpeg/bin/ffmpeg.exe" if not binary else "../../../tools/win32/ffmpeg/bin/ffmpeg.exe"
    deno_path = "tools/win32/deno/deno.exe" if not binary else "../../../tools/win32/deno/deno.exe"

"""Version info"""
mode = "binary" if binary else "source"
print(f"LunarPlayer 0.1-alpha.1 {platform} ({mode})")

"""Functions"""
def song_ask(titles):
    choice = questionary.select(
        "Loaded 10 most relevant results, pick the one you want to play.",
        choices=titles,
    ).ask()

    def input_ask():
        making_sure = input(f"You chose {choice}. Is this correct? (y/n)\n"
                            f"> ").lower()
        if making_sure == "y":
            pass
            # download song
            # play song
        elif making_sure == "n":
            song_ask(titles)
        else:
            print("Wrong input.")
            input_ask()

    input_ask()
    return choice


def play_song(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    paused = False

    def listen_for_actions():
        nonlocal paused
        while True:
            key = readchar.readkey()
            if key == readchar.key.SPACE:
                if paused:
                    pygame.mixer.music.unpause()
                    print("Resumed")
                else:
                    pygame.mixer.music.pause()
                    print("Paused")
                paused = not paused
            elif key == readchar.key.ESC:
                print("Stopping music...")
                pygame.mixer.music.stop()
                pygame.mixer.quit()
                print("Music stopped.")
                print("Program killed.")
                os._exit(0)

    threading.Thread(target=listen_for_actions, daemon=True).start()

    while pygame.mixer.music.get_busy() or paused:
        time.sleep(0.1)

"""Search prompt"""
song = input("Song name: ")
results = YoutubeSearch(song, max_results=10).to_dict()
titles = []
for result in results:
    titles.append(result["title"])

choice = song_ask(titles)

for result in results:
    if result["title"] == choice:
        link = f"https://www.youtube.com{result['url_suffix']}"

"""Downloading"""
filename = f"songs/{choice}.ogg"

if os.path.exists(filename):
    play_song(filename)
else:
    print("Fetching audio stream...")
    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "noplaylist": True,
        "js_runtimes": {
            "deno": {
                "path": deno_path
            }
        }
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=False)
        stream = info["url"]

    print("Converting audio stream to ogg using ffmpeg...")
    ffmpeg.input(stream).output(filename, format="ogg", acodec="libvorbis", audio_bitrate="320k", loglevel="error").run(cmd=rf"{ffmpeg_path}")

    print("Downloaded, playing...")

    """Playing audio"""
    play_song(filename)