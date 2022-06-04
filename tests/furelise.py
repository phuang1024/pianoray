from pianoray import *


class FurElise(DefaultScene):
    def setup(self):
        self.video.resolution = (960, 540)
        self.video.fps = 30

        self.midi.file = "examples/furelise/midi.mid"

        self.audio.file = "examples/furelise/audio.mp3"
        self.audio.start = 20.74

        self.blocks.speed.animate(
            (100, 0.5, Interp.LINEAR),
            (150, 0.2, Interp.LINEAR),
            (200, 0.2, Interp.LINEAR),
            (250, 1, Interp.LINEAR),
            (300, 1, Interp.QUADRATIC),
            (350, 0.5, Interp.QUADRATIC),
        )
        self.blocks.color.animate(100, (0.6, 0.65, 0.9), Interp.LINEAR)
        self.blocks.color.animate((150, (0.9, 0.65, 0.6), Interp.CONSTANT))

        self.keyboard.file = "examples/furelise/video.mp4"
        self.keyboard.start = 4.75
        self.keyboard.end = 37.64
        self.keyboard.crop = ((252,480), (1793,487), (1789,676), (257,666))
        self.keyboard.dim_mult = 0.6
        self.keyboard.dim_add = -8

        """
        self.comp.shutter.animate(50, 1, Interp.LINEAR)
        self.comp.shutter.animate(100, 2, Interp.LINEAR)
        self.comp.shutter.animate(150, 0.5, Interp.LINEAR)
        """
