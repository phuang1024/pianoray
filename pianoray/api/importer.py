import os
import sys
from pathlib import Path

from .scene import Scene


def import_scene(file: str, name: str) -> Scene:
    """
    Import a scene object class from a Python file.
    """
    path = Path(file)
    sys.path.insert(0, str(path.absolute().parent))

    mod = __import__(path.with_suffix("").name)
    cls = getattr(mod, name)

    sys.path.pop(0)
    return cls
