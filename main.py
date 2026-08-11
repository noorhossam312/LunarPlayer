"""Imports"""
import sys
import os
import time
import threading
import json
import ffmpeg
import yt_dlp
import pygame
import readchar
import questionary
from rich.console import Console
from youtube_search import YoutubeSearch
from installer import install_all

console = Console()

"""Checks"""
if getattr(sys, 'frozen', False):  # This check is to check if the user is running the program through the source or the binary.
    binary = True
else:
    binary = False

platform = sys.platform

if platform == "darwin":
    console.input(
        f"[red]{'!!!FATAL ERROR!!!'.center(console.width)}[/red]\n"
        f"{'This program does not have support for MacOS. The program will terminate.'.center(console.width)}\n"
        f"{'Press Enter to terminate.'.center(console.width)}"
    )
    sys.exit(1)



browser_exists = False

with open("yt-dlp-presets/cookiesfrombrowser.json", "r") as f:
    loaded_json = json.load(f)
    if "browser" in loaded_json:
        if loaded_json["cookiesfrombrowser"] != "":
            browser_exists = True

"""Important calls"""
install_all.add_tool_files_to_path()

"""Version info"""
mode = "binary" if binary else "source"
print(f"LunarPlayer 0.1-alpha.1 {platform} ({mode})")

"""Functions"""
def song_ask(titles):
    choice = questionary.select(
        "Loaded the 10 most relevant results, pick the result you want to play.",
        choices=titles,
    ).ask()

    def input_ask():
        making_sure = input(f"You chose {choice}. Is this correct? (y/n)\n"
                            f"> ").lower()
        if making_sure == "y":
            pass
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
        input(result['url_suffix'])

"""Downloading"""
filename = f"songs/{choice}.ogg"

if os.path.exists(filename):
    play_song(filename)
else:
    print("Fetching audio stream...")
    with open("yt-dlp-presets/cookiesfrombrowser.json", "r") as f:
        config = json.load(f)
        if "cookiesfrombrowser" in config and not browser_exists:
            console.print(
                f"[yellow]{'WARNING'.center(console.width)}[/yellow]"
                f"You are using the cookiesfrombrowser approach. This will let yt-dlp use your already authenticated cookies, which could lead to YouTube detecting automated activity, restricting or invalidating your session. Use this only when necessary.".center(console.width)
            )
            get_browser = questionary.select(
                "LunarPlayer has recognized cookiesfrombrowser in the JSON config file. Please pick the browser you are logged into YouTube with.",
                choices=["Brave",
                         "Chrome",
                         "Chromium",
                         "Edge",
                         "Firefox",
                         "Opera",
                         "Safari",
                         "Vivaldi",
                         "Whale",
                ],
            ).ask().lower()
            config["cookiesfrombrowser"] = (get_browser,)
            with open("yt-dlp-presets/cookiesfrombrowser.json", "w") as f:
                json.dump(config, f, indent=4)

    ydl_opts = config

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=False)
        stream = info["url"]

    print("Converting audio stream to ogg using ffmpeg...")
    ffmpeg.input(stream).output(filename, format="ogg", acodec="libvorbis", audio_bitrate="320k", loglevel="error").run()

    print("Downloaded, playing...")

    """Playing audio"""
    play_song(filename)