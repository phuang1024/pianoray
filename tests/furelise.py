from pianoray import *


class FurElise(DefaultScene):
    def setup(self):
        self.video.resolution = (960, 540)
        self.video.fps = 30

        self.midi.file = "examples/furelise/midi.mid"

        self.audio.file = "examples/furelise/audio.mp3"
        self.audio.start = 20.74

        self.blocks.speed = 0.5
        self.blocks.color.animate(Keyframe(200, (200, 200, 255), Interp.LINEAR))
        self.blocks.color.animate(Keyframe(300, (255, 200, 200), Interp.LINEAR))

        self.keyboard.file = "examples/furelise/video.mp4"
        self.keyboard.start = 4.75
        self.keyboard.crop = ((252,480), (1793,487), (1789,676), (257,666))
        self.keyboard.dim_mult = 0.6
        self.keyboard.dim_add = -8
