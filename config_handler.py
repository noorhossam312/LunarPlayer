import json
import os
import pathlib
import struct
import sys

import questionary
from rich.console import Console

import nice_errors


class Reader:
    """A reader for the configuration file.

    This class manages the configuration file.

    Attributes:
        path: A string representing the file path to the configuration file.
        console: A Rich Console instance.
    """
    def __init__(self, file_path: str):
        """Initializes the Reader.

        Also initializes Rich.

        Args:
            file_path: A string representing the file path to the configuration file.
        """
        self.path = file_path
        self.console = Console()

    def find_config_type(self) -> str:
        """Finds the configuration file type.

        Returns:
            A string representing the configuration file type.
            Can return either "cookiesfrombrowser", "cookiefile", or "default".
        """
        with open(self.path, 'r') as f:
            file_json = json.load(f)
            config_types = ["cookiesfrombrowser", "cookiefile", "default"]
            if config_types[0] in file_json:
                return config_types[0]
            elif config_types[1] in file_json:
                return config_types[1]
            else:
                return config_types[2]

    def read(self) -> dict:
        """Reads the configuration file.

        Returns:
            A dictionary representing the configuration file.
        """
        with open(self.path, 'r') as f:
            return json.load(f)


    def write_browser(self) -> None:
        """Asks the user what browser they are logged onto YouTube with, to use the cookies for yt-dlp.

        This method asks the user what browser they use for YouTube
        using Questionary, and then writes it to the configuration file.
        """
        browser = questionary.select(
            "You are using \"cookiesfrombrowser\". Please pick the browser you are logged into YouTube with.",
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
        try:
            config = self.read()
            config["cookiesfrombrowser"] = (browser,)
            with open(self.path, 'w') as f:
                json.dump(config, f, indent=2)

        except FileNotFoundError as e:
            nice_errors.print_error("ferror", str(e))
        except json.decoder.JSONDecodeError as e:
            nice_errors.print_error("ferror", str(e))
        except Exception as e:
            nice_errors.print_error("ferror", str(e))

    def specify_quickjs(self) -> None:
        """Finds the QuickJS-ng executable path, and writes it on disk.

        This method checks the architecture, and operating system of the user's machine, and finds
        the path using those key points.
        """
        config = self.read()
        if not config["js_runtimes"]["quickjs"]:
            architecture = "x86" if struct.calcsize("P") * 8 == 32 else "x86_64"
            platform = "windows" if sys.platform == "win32" else "linux"
            quickjs_dir = (pathlib.Path("quickjs")
                           / platform
                           / architecture
                           / ("qjs.exe" if sys.platform == "win32" else "qjs"))
            quickjs_abspath = os.path.abspath(str(quickjs_dir))
            config["js_runtimes"]["quickjs"]["path"] = quickjs_abspath
            with open(self.path, 'w') as f:
                json.dump(config, f, indent=2)
