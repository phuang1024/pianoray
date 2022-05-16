"""
Default scene, contains settings for PianoRay.
i.e. default "implementation" of Scene.
"""

from .modifiers import *
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
        animatable=False,
        default=(1920, 1080),
        shape=(2,),
    )

    fps: IntProp(
        name="FPS",
        desc="Frames per second of output video.",
        animatable=False,
        default=30,
        min=1,
    )

    vcodec: StrProp(
        name="Video Codec",
        desc="Codec for video, passed to FFmpeg.",
        animatable=False,
        default="libx265",
    )


class AudioProps(PropertyGroup):
    """
    Audio.
    """

    file: PathProp(
        name="Audio File",
        desc="Path to audio file.",
        animatable=False,
        default=None,
        isfile=True,
    )

    start: FloatProp(
        name="Start Time",
        desc="Timestamp, in seconds, you press the first note.",
        animatable=False,
        default=0,
    )


class CompositionProps(PropertyGroup):
    """
    Composition, i.e. structure of the video.
    """

    margin_start: FloatProp(
        name="Start Margin",
        desc="Pause, in seconds, before first note starts.",
        animatable=False,
        default=3,
        min=0,
    )

    margin_end: FloatProp(
        name="End Margin",
        desc="Pause, in seconds, after the last note ends.",
        animatable=False,
        default=3,
        min=0,
    )

    fade_in: FloatProp(
        name="Fade In",
        desc="Seconds of fade in.",
        animatable=False,
        default=1,
        min=0,
    )

    fade_out: FloatProp(
        name="Fade Out",
        desc="Seconds of fade out.",
        animatable=False,
        default=1,
        min=0,
    )

    fade_blur: FloatProp(
        name="Fade Blur",
        desc="Blur radius of fade in coords.",
        animatable=False,
        mods=[Coords()],
        default=1,
        coords=True,
    )


class PianoProps(PropertyGroup):
    """
    Piano parameters.
    """

    black_width_fac: FloatProp(
        name="Black Key Width Factor",
        desc="Black key width as factor of white key width.",
        animatable=False,
        default=0.6,
        min=0,
    )


class BlocksProps(PropertyGroup):
    """
    The blocks that fall down.
    """

    speed: FloatProp(
        name="Speed",
        desc="If ``X`` is the distance between the top of the screen and the"
             "top of the keyboard, the blocks travel ``speed * X`` per second.",
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
        mods=[Coords()],
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
        mods=[Coords()],
        default=0.4,
        coords=True,
    )


class MidiProps(PropertyGroup):
    file: PathProp(
        name="MIDI File",
        desc="Path to MIDI file.",
        animatable=False,
        default=None,
        isfile=True,
    )

    speed: FloatProp(
        name="Speed Multiplier",
        desc="MIDI notes speed multiplier.",
        animatable=False,
        default=1,
    )

    min_length: FloatProp(
        name="Minimum Duration",
        desc="Min duration of a note in seconds.",
        animatable=False,
        default=0.08,
        min=0,
    )


class KeyboardProps(PropertyGroup):
    file: PathProp(
        name="Video File",
        desc="Path to video recording of keyboard.",
        animatable=False,
        default=None,
        isfile=True,
    )

    start: FloatProp(
        name="Start",
        desc="Timestamp, in seconds, when the first note starts in the video.",
        animatable=False,
        default=None,
    )

    end: FloatProp(
        name="End",
        desc="Timestamp, in seconds, when the last note starts in the video.",
        animatable=False,
        default=None,
    )

    crop: ArrayProp(
        name="Crop",
        desc="Crop points of the keyboard. See docs for more info.",
        animatable=False,
        default=None,
        shape=(4, 2),
    )

    dim_mult: FloatProp(
        name="Multiplicative Dimming",
        desc="Multiplier to pixel brightness.",
        default=1,
        min=0,
    )

    dim_add: FloatProp(
        name="Additive Dimming",
        desc="Value added to pixel brightness (0 to 255).",
        default=0,
    )

    below_length: FloatProp(
        name="Length of Below Section",
        desc="Length in coords of section below keyboard.",
        mods=[Coords()],
        default=7,
        min=0,
    )

    octave_lines: BoolProp(
        name="Octave Lines",
        desc="Whether to render octave lines.",
        default=True,
    )


class GlareProps(PropertyGroup):
    radius: FloatProp(
        name="Radius",
        desc="Radius of glare in coords.",
        mods=[Coords()],
        default=3,
        min=0,
    )

    intensity: FloatProp(
        name="Intensity",
        desc="Intensity of glare.",
        default=0.9,
        min=0,
    )

    jitter: FloatProp(
        name="Jitter",
        desc="Range of random multiplier.",
        default=0.08,
        min=0,
    )

    streaks: IntProp(
        name="Streaks",
        desc="Number of streaks.",
        default=6,
        min=0,
        max=20,  # C implementation limitation.
    )


class ParticleProps(PropertyGroup):
    pps: FloatProp(
        name="Particles per Second",
        desc="Number of particles to emit per note per second.",
        default=40,
        min=0,
    )

    air_resist: FloatProp(
        name="Air Resistance",
        desc="Velocity multiplies by this every second.",
        default=0.6,
        min=0,
    )

    lifetime: FloatProp(
        name="Lifetime",
        desc="Particle lifetime in seconds.",
        default=3,
        min=0,
    )

    x_vel: FloatProp(
        name="X Velocity",
        desc="Initial X velocity range in coords/sec.",
        mods=[Coords(), SecToFrame()],
        default=1,
        min=0,
    )

    y_vel: FloatProp(
        name="Y Velocity",
        desc="Initial Y velocity range in coords/sec.",
        mods=[Coords(), SecToFrame()],
        default=4,
        min=0,
    )

    wind_strength: FloatProp(
        name="Wind Strength",
        desc="Strength multiplier of wind affecting particles.",
        default=1,
    )

    heat_strength: FloatProp(
        name="Heat Strength",
        desc="Strength multiplier of heat affecting particles.",
        default=1,
    )

    gravity: FloatProp(
        name="Gravity",
        desc="Strength multiplier of gravity affecting particles.",
        default=1,
    )


class DefaultScene(Scene):
    _pgroups = {
        "audio": AudioProps(),
        "blocks": BlocksProps(),
        "composition": CompositionProps(),
        "glare": GlareProps(),
        "keyboard": KeyboardProps(),
        "midi": MidiProps(),
        "ptcls": ParticleProps(),
        "piano": PianoProps(),
        "video": VideoProps(),
    }
