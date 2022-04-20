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

import pygame

from .timeline import Timeline
from .utils import *
from .video import Video

pygame.init()


class Info:
    """
    Shows info as text to user.
    """

    def __init__(self, video: Video, timeline: Timeline):
        self.video = video
        self.timeline = timeline

    def draw(self, surface: pygame.Surface, events, rect):
        """
        Draw info on surface.

        :param rect: ``(x, y, w, h)`` coordinates to draw.
        """
        frame = self.timeline.frame
        fps = self.video.fps
        text = [
            f"Frame: {frame}",
            f"Cached frames: {self.video.extracted}",
            f"Timestamp: {frame/fps:.3f}s",
        ]

        x = rect[0] + 20
        for i, t in enumerate(text):
            y = rect[1] + 10 + 20*i
            surf = FONT_MED.render(t, True, WHITE)
            surface.blit(surf, (x, y))
