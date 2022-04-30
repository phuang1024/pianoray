import numpy as np
import pygame

from ..utils import bounds
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
        total_frames = self.video.num_frames

        # Handle events
        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()
            if x <= mx < x+w and y <= my < y+h:
                fac = (mx-x) / w
                self.frame = int(fac * self.video.num_frames)

        pygame.draw.rect(surface, DARK_GRAY, rect)

        # Draw cached
        x2 = Timeline.fac_to_pix(x, w, self.video.extracted/total_frames)
        pygame.draw.rect(surface, GRAY, (x, y, x2-x, 5))

        # Draw marker
        marker = Timeline.fac_to_pix(x, w, self.frame/total_frames)
        pygame.draw.line(surface, BLUE, (marker, y), (marker, y+h))

    def next_frame(self):
        self.frame = bounds(self.frame+1, 0, self.video.num_frames)

    def prev_frame(self):
        self.frame = bounds(self.frame-1, 0, self.video.num_frames)

    @staticmethod
    def fac_to_pix(x, w, fac):
        return np.interp(fac, (0, 1), (x, x+w))
