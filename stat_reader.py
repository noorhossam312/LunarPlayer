import json

from rich.console import Console

console = Console()

class StatisticsReader:
    """Manages stats.json.

    This class manages the stats.json file.

    Attributes:
        file_path: Path to stats.json file
    """
    def __init__(self, file_path: str):
        """Initialize the StatisticsReader object with a file path.

        Args:
            file_path: The file path to the stats.json.
        """
        self.file_path = file_path

    def read_stats(self) -> str:
        """Read stats.json and return a human-readable string.

        Returns:
            result: String representation of stats.json.
        """

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
