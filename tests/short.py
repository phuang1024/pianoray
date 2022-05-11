from pianoray import *


class Short(DefaultScene):
    def setup(self):
        self.video.resolution = (640, 360)
        self.video.fps = 24

        self.midi.file = "examples/short/midi.mid"

        self.audio.file = "examples/short/audio.mp3"
        self.audio.start = 2.4

        self.keyboard.file = "examples/furelise/video.mp4"
        self.keyboard.start = 4.75
        self.keyboard.end = 37.64
        self.keyboard.crop = ((252,480), (1793,487), (1789,676), (257,666))
