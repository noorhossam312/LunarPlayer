import os
import pathlib
import struct
import sys


def add_tools_to_path():
    cwd = pathlib.Path.cwd()
    project_root = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
    if cwd != project_root:
        os.chdir(project_root)
    bitness = str(struct.calcsize("P") * 8)
    bitness = "x86" if bitness == 32 else "x86_64"
    quickjs_path = project_root / "quickjs" / ("windows" if sys.platform == "win32" else sys.platform) / bitness
    os.environ["PATH"] = str(quickjs_path) + os.pathsep + os.environ["PATH"]
