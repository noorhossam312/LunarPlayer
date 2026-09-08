import json

from rich.console import Console

console = Console()

class StatisticsReader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read_stats(self):
        with open(self.file_path, "r") as f:
            stats = json.load(f)
            stats = stats["song_plays"]
            stats_songs = stats["songs"] # { "Song": 9, "Song 2": 9 }
            stats_total = stats["total"] # 18
            result = ["Songs".center(console.width)]
            for song_name, plays in stats_songs.items():
                result.append(f"{song_name}: {plays} plays".center(console.width))
            result.append(f"{stats_total} lifetime plays.".center(console.width))
            return "\n".join(result)
