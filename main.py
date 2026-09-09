import os

import questionary

import config_handler
import downloader
import player
import searcher
import stat_reader


def main_menu(calling_from_player=False):
    while True:
        abilities = ["Search and play a song", "View stats"]
        choice = questionary.select(
            "Welcome to LunarPlayer! What do you want to do?",
            choices=abilities,
        ).ask().lower()[0]
        if choice == "s":
            s = searcher.Searcher()
            link, title = s.search_and_ask(input("Search term\n> "))
            if os.path.exists(downloader.sanitize_filename(title)):
                p = player.Player()
                p.play(downloader.sanitize_filename(title), title)
            else:

                filename = downloader.Downloader.download(link, title, config)
                p = player.Player()
                p.play(filename, title)
        elif choice == "v":
            sr = stat_reader.StatisticsReader("stats.json")
            print(sr.read_stats())

if __name__ == '__main__':
    print("Reading config...")
    r = config_handler.Reader("yt-dlp-presets/config.json")
    config = r.read()
    config_type = r.find_config_type()
    if config_type == "cookiesfrombrowser" and config["cookiesfrombrowser"] == "":
        r.write_browser()
    r.specify_quickjs()
    print("Done.")
    main_menu()
