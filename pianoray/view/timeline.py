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

        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()
            if x <= mx < x+w and y <= my < y+h:
                fac = (mx-x) / w
                self.frame = int(fac * self.video.num_frames)

        pygame.draw.rect(surface, DARK_GRAY, rect)

        marker = self.frame / self.video.num_frames
        marker = marker*w + x
        left_x = int(marker)
        left_col = (BLUE * (marker-left_x)).astype(int)
        right_x = int(marker) + 1
        right_col = (BLUE * (right_x-marker)).astype(int)
        pygame.draw.line(surface, left_col, (left_x, y), (left_x, y+h))
        pygame.draw.line(surface, right_col, (right_x, y), (right_x, y+h))
