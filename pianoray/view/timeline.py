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

import numpy as np
import pygame

from .utils import *
from .video import Video

pygame.init()


class Timeline:
    """
    Frame browser area.
    """

    def __init__(self, video: Video):
        self.video = video

        self.frame = 0

    def draw(self, surface: pygame.Surface, events, rect):
        """
        Draw timeline on surface.

        :param rect: ``(x, y, w, h)`` coordinates to draw.
        """
        x, y, w, h = rect

        # Handle events
        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()
            if x <= mx < x+w and y <= my < y+h:
                fac = (mx-x) / w
                self.frame = int(fac * self.video.num_frames)

        pygame.draw.rect(surface, DARK_GRAY, rect)

        # Draw cached
        x2 = Timeline.fac_to_pix(x, w, self.video.extracted/self.video.num_frames)
        pygame.draw.rect(surface, GRAY, (x, y, x2-x, 5))

        # Draw marker
        marker = Timeline.fac_to_pix(x, w, self.frame/self.video.num_frames)
        pygame.draw.line(surface, BLUE, (marker, y), (marker, y+h))

    @staticmethod
    def fac_to_pix(x, w, fac):
        return np.interp(fac, (0, 1), (x, x+w))
