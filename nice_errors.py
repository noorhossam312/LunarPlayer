import sys
from typing import Literal

from rich.align import Align
from rich.console import Console
from rich.panel import Panel

console = Console()

def print_error(severity: Literal["warn", "ferror"], error: str) -> None:
    """Prints a pretty error message.

    This function prints a pretty error message to the console, returning nothing.

    Args:
        severity: How severe the error is (ferror: fatal error, warn: warning)
        error: The error message to print.
    """
    if severity == "warn":
        panel = Panel(
            error,
            title="[yellow]WARNING[/yellow]",
            expand=False,
        )
        console.print(panel)
    elif severity == "ferror":
        panel = Panel(
            f"{error}\nPress Enter to exit...",
            title="[red]!!!FATAL ERROR!!![/red]",
            expand=False,
        )
        console.input(Align.center(panel))
        sys.exit()
