import json
import os
import threading
import time

import mpv
import readchar
from rich.console import Console
from rich.live import Live

console = Console()

class Player:
    """Plays an audio file.

    It uses python-mpv to play the audio file, while adding some extra keybinds.
    """
    def __init__(self):
        self.stop = False
        self.player = mpv.MPV()

    def play(self, filepath: str, song_name: str) -> None:
        """Plays a song by its file path.

        This function writes stats.json, and plays a song.

        Args:
            filepath: The file path to the song.
            song_name: The name of the song. (Used for writing stats.json)
        """
        self.player.play(filepath)
        self.filename = filepath
        self.write_stats_to_disk(song_name)

        threading.Thread(target=self.listen_for_actions, daemon=True).start()

        os.system("cls" if os.name == "nt" else "clear")
        with Live(console=console, refresh_per_second=10) as live:
            while not self.stop and self.player.path:
                player_pos = time.strftime("%H:%M:%S", time.gmtime(int(self.player.time_pos or 0.0)))
                song_dur = time.strftime("%H:%M:%S", time.gmtime(int(self.player.duration or 0.0)))
                live.update(f"{song_name}\n"
                f"{player_pos}/{song_dur}\n"
                f"{int(self.player.volume)}% volume, Looping is {'on' if self.player.loop_file == 'inf' else 'off'}\n"
                f"{p}"
                )

        menu_or_quit = questionary.select(
            "Song is over. What to do?",
            choices=["Exit to main menu", "Quit"],
        )
        if menu_or_quit.lower()[0] == "q":
            self.quit()

    def listen_for_actions(self):
        """Listens for keybinds.

        This function listens for keybinds using readchar so that it can execute functions.
        """
        while True:
            key = readchar.readkey()
            if key == readchar.key.SPACE:
                self.toggle_pause()
            elif key == 'q':
                self.quit()
                return
            elif key == readchar.key.DOWN:
                self.vol_down_major()
            elif key == readchar.key.UP:
                self.vol_up_major()
            elif key == readchar.key.PAGE_DOWN:
                self.vol_down_minor()
            elif key == readchar.key.PAGE_UP:
                self.vol_up_minor()
            elif key == 'c':
                self.close()
                return
            elif key == 'l':
                self.toggle_loop()
            elif key == readchar.key.RIGHT:
                self.seek(10)
            elif key == readchar.key.LEFT:
                self.seek(-10)

    def toggle_pause(self):
        self.player.pause = not self.player.pause

    def quit(self):
        self.stop = True
        self.player.terminate()
        os._exit(0)

    def vol_down_major(self):
        self.player.volume = max(0, self.player.volume - 5)

    def vol_up_major(self):
        self.player.volume = min(100, self.player.volume + 5)

    def vol_down_minor(self):
        self.player.volume = max(0, self.player.volume - 1)

    def vol_up_minor(self):
        self.player.volume = min(100, self.player.volume + 1)

    def close(self):
        self.stop = True
        self.player.terminate()

    def toggle_loop(self):
        if self.player.loop_file == "inf":
            self.player.loop_file = "no"
        else:
            self.player.loop_file = "inf"

    def seek(self, amount_to_seek):
        self.player.seek(amount_to_seek, "relative")

    def write_stats_to_disk(self, song: str):
        song_stats = self.read_stats()
        if song in song_stats["song_plays"]["songs"]:
            song_stats["song_plays"]["songs"][song] += 1
        else:
            song_stats["song_plays"]["songs"][song] = 1
        song_stats["song_plays"]["total"] += 1
        with open('stats.json', 'w') as f:
            json.dump(song_stats, f, indent=2)

    @staticmethod
    def read_stats():
        with open('stats.json', 'r') as f:
            stats_json = json.load(f)
            return stats_json
