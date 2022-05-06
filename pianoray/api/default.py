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
        min=0,
    )

    fade_out: FloatProp(
        name="Fade Out",
        desc="Seconds of fade out.",
        default=1,
        animatable=False,
        min=0,
    )

    fade_blur: FloatProp(
        name="Fade Blur",
        desc="Blur radius of fade in coords.",
        default=1,
        animatable=False,
        coords=True,
    )


class PianoProps(Scene):
    """
    Piano parameters.
    """

    black_width_fac: FloatProp(
        name="Black Key Width Factor",
        desc="Black key width as factor of white key width.",
        default=0.6,
        animatable=False,
        min=0,
    )


class BlocksProps(Scene):
    """
    The blocks that fall down.
    """

    speed: FloatProp(
        name="Speed",
        desc="If ``X`` is the distance between the top of the screen and the"
             "top of the keyboard, the blocks travel ``speed * X`` per second."
        default=0.5,
    )

    color: RGBProp(
        name="Color",
        desc="Color of the blocks.",
        default=(150, 160, 240),
    )

    radius: FloatProp(
        name="Corner Radius",
        desc="Corner rounding radius in coords.",
        default=0.25,
        min=0,
    )

    glow_intensity: FloatProp(
        name="Glow Intensity",
        desc="Intensity of glow around blocks.",
        default=0.3,
        min=0,
    )

    glow_color: RGBProp(
        name="Glow Color",
        desc="Color of the glow.",
        default=(230, 230, 255),
    )

    glow_radius: FloatProp(
        name="Glow Radius",
        desc="Radius of glow around blocks in coords.",
        default=0.4,
        coords=True,
    )


class DefaultScene(Scene):
    _pgroups = {
        "video": VideoProps,
        "audio": AudioProps,
        "composition": CompositionProps,
    }
