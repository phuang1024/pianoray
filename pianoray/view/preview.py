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

import cv2
import pygame

from .timeline import Timeline
from .utils import *
from .video import Video

pygame.init()


class Preview:
    """
    Preview current frame.
    """

    def __init__(self, video: Video, timeline: Timeline):
        self.video = video
        self.timeline = timeline

    def draw(self, surface: pygame.Surface, events, rect):
        """
        Draw info on surface.

        :param rect: ``(x, y, w, h)`` coordinates to draw.
        """
        x, y, w, h = rect

        if self.timeline.frame > self.video.extracted:
            return

        img = self.video.get(self.timeline.frame)
        img = cv2.resize(img, (w, h)).swapaxes(0, 1)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = pygame.surfarray.make_surface(img)
        surface.blit(img, (x, y))
