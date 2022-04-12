#
#  PianoRay
#  Video rendering pipeline with piano visualization.
#  Copyright  PianoRay Authors  2022
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import os
import numpy as np
from pianoray import BasePipeline

FPS = 30

MIDI_PATH = os.path.abspath("examples/furelise.mid")


class Pipeline(BasePipeline):
    def get_meta(self):
        length = self.kernels.midi({
            "midi": {
                "type": "length",
                "file": MIDI_PATH,
                "fps": FPS,
            }
        })["midi"]
        length = int(length)

        return {
            "start": -60,
            "end": length + 60,
            "res": (1920, 1080),
            "fps": FPS,
        }

    def render_frame(self, frame, meta):
        if frame == 0:
            # Testing stuff

            # MIDI kernel
            midi_input = {
                "midi": {
                    "type": "length",
                    "file": os.path.abspath("./examples/furelise.mid"),
                    "fps": 30,
                    #"types": ["note_on"],
                    #"attrs": ["type", "note", "velocity"],
                }
            }
            run = self.kernels.midi.run()
            run.send(midi_input)
            print(run.recv())
            run.send(midi_input)
            print(run.recv())

            #print(self.kernels.midi(midi_input))

            """
            # Async kernel
            run = self.kernels.pytest(None, True)
            run.wait()
            print(run.output)

            # The Java ...
            print(self.kernels.jtest(None))
            """

        res = meta["res"]

        img = np.zeros((res[1], res[0], 3), dtype=np.uint8)
        img[..., 0] = 255

        return img
