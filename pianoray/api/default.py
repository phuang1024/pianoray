"""
Default scene, contains settings for PianoRay.
i.e. "implementation" of Scene.
"""

from .pgroup import PropertyGroup
from .props import *
from .scene import Scene


class VideoProps(PropertyGroup):
    """
    Output video parameters.
    """

    resolution: ArrayProp(
        name="Resolution",
        desc="Output video resolution.",
        default=(1920, 1080),
        animatable=False,
        shape=(2,),
    )

    fps: IntProp(
        name="FPS",
        desc="Frames per second of output video.",
        default=30,
        animatable=False,
        min=1,
    )

    vcodec: StrProp(
        name="Video Codec",
        desc="Codec for video, passed to FFmpeg.",
        default="libx265",
        animatable=False,
    )


class AudioProps(PropertyGroup):
    """
    Audio.
    """

    file: StrProp(
        name="Audio File",
        desc="Path to audio file.",
        default="",
        animatable=False,
    )

    start: FloatProp(
        name="Start Time",
        desc="Timestamp, in seconds, you press the first note.",
        default=0,
        animatable=False,
    )


class CompositionProps(PropertyGroup):
    """
    Composition, i.e. structure of the video.
    """

    margin_start: FloatProp(
        name="Start Margin",
        desc="Pause, in seconds, before first note starts.",
        default=3,
        animatable=False,
        min=0,
    )

    margin_end: FloatProp(
        name="End Margin",
        desc="Pause, in seconds, after the last note ends.",
        default=3,
        animatable=False,
        min=0,
    )

    fade_in: FloatProp(
        name="Fade In",
        desc="Seconds of fade in.",
        default=1,
        animatable=False,
        min=0
    )

    fade_out: FloatProp(
        name="Fade Out",
        desc="Seconds of fade out.",
        default=1,
        animatable=False,
        min=0
    )


class DefaultScene(Scene):
    _pgroups = {
        "video": VideoProps,
        "audio": AudioProps,
        "composition": CompositionProps,
    }
