# LunarPlayer
***
## What it is
LunarPlayer is a music player that is designed to be as lightweight as possible, by using as little modules/dependencies as possible.

***
## Credits and licenses
LunarPlayer uses the following third-party software and assets:
- [Moon](https://icons8.com/icon/anfmaDWxCFY8/crescent-moon) icon by [Icons8](https://icons8.com)

LunarPlayer itself is licensed under the MIT license. See [LICENSE](LICENSE) for the full MIT license.
***
## Get started with LunarPlayer
1. Install all required modules from [requirements.txt](requirements.txt). Run `pip install -r requirements.txt` for regular pip, or `uv pip install -r requirements.txt` while in a venv for UV.
2. Install FFmpeg through your package manager. The usual name for the package is "ffmpeg" or "ffmpeg-free", or install [FFmpeg for 32 bits](https://github.com/defisym/FFmpeg-Builds-Win32/releases) or [FFmpeg for 64 bit](https://github.com/BtbN/FFmpeg-Builds/releases) if you are on Windows, then add the bin/ folder to your PATH.
3. Install an mpv .dll/.so file, and make sure it is in your system's PATH. Or if you're using Linux, install mpv-libs or mpv-devel.
4. Done! You can now run [main.py](main.py).
***
## Controls
Space: Pause/Resume

Arrow Up: Increment volume by 5%

Arrow Down: Decrement volume by 5%

Page Up: Increment volume by 1%

Page Down: Decrement volume by 1%

L: Toggle looping

Q: Quit safely (Please do not use Ctrl+C, as it doesn't exit the program cleanly)

C: Exit to main menu
***
## What to expect
It's not exactly super stable, it still isn't that thoroughly tested, so please open an issue if you encounter an issue/bug.