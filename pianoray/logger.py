"""
Logging utils.
"""

import sys
import termcolor
from datetime import datetime


def time():
    now = datetime.now()
    return now.strftime("%H:%M:%S")


def log(type: str, msg: str, color: str):
    s = f"[{time()}] {type}:"
    s += " " * (6-len(type))
    s += msg
    print(termcolor.colored(s, color), file=sys.stderr)

def info(msg: str) -> None:
    """
    Info log to stderr.
    Color: blue
    """
    log("INFO", msg, "cyan")

def warn(msg: str) -> None:
    """
    Warning log to stderr.
    Color: yellow
    """
    log("WARN", msg, "yellow")

def error(msg: str) -> None:
    """
    Error log to stderr.
    Color: red
    """
    log("ERROR", msg, "red")
