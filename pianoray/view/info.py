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
