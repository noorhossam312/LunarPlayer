import os

import questionary

import downloader
import player
import searcher
import stat_reader


def main_menu(calling_from_player=False):
    p = player.Player()
    while True:
        abilities = ["Search and play a song", "View stats"]
        choice = questionary.select(
            "Welcome to LunarPlayer! What do you want to do?",
            choices=abilities,
        ).ask().lower()[0]
        if choice == "s":
            link, title = searcher.Searcher.search_and_ask(input("Search term\n> "))
            if os.path.exists(downloader.sanitize_filename(title)):
                p.play(downloader.sanitize_filename(title), title)
            else:
                filename = downloader.Downloader.download(link, title)
                p.play(filename, title)
        elif choice == "v":
            sr = stat_reader.StatisticsReader("stats.json")
            print(sr.read_stats())

if __name__ == '__main__':
    main_menu()
