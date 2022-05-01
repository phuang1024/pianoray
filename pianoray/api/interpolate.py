from .keyframe import Keyframe


def interpolate(k1: Keyframe, k2: Keyframe, frame: int) -> Any:
    """
    Interpolate between two keyframes.
    """
