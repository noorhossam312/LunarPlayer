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
    def __init__(self):
        self.stop = False
        self.player = mpv.MPV()

    def play(self, filename: str, song_name: str):
        self.player.play(filename)
        self.filename = filename
        self.write_stats_to_disk(song_name)
        threading.Thread(target=self.listen_for_actions, daemon=True).start()
        os.system("cls" if os.name == "nt" else "clear")
        with Live(console=console, refresh_per_second=10) as live:
            while not self.stop:
                player_pos = time.strftime("%H:%M:%S", time.gmtime(int(self.player.time_pos or 0.0)))
                song_dur = time.strftime("%H:%M:%S", time.gmtime(int(self.player.duration or 0.0)))
                live.update(f"{song_name}\n"
                f"{player_pos}/{song_dur}\n"
                f"{int(self.player.volume)}% volume"
                )
                time.sleep(0.1)

    def listen_for_actions(self):
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
                print("Looping toggled.")
            elif key == readchar.key.RIGHT:
                self.seek(10)
            elif key == readchar.key.LEFT:
                self.seek(-10)

    def toggle_pause(self, *args):
        self.player.pause = not self.player.pause

    def quit(self, *args):
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
