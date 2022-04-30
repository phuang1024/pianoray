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
