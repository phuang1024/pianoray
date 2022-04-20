#
#  PianoRay
#  Piano performance visualizer.
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

import shutil
import time

import pygame

from .. import logger
from .info import Info
from .preview import Preview
from .timeline import Timeline
from .utils import *
from .video import Video

pygame.init()


def view_video(path: str) -> None:
    logger.warn("Viewer is not complete yet.")

    video = Video(path)
    timeline = Timeline(video)
    info = Info(video, timeline)
    preview = Preview(video, timeline)

    logger.info(f"Extracting frames to {video.tmpdir}")

    resized = False  # Redraw if resized
    display = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    pygame.display.set_caption("PianoRay Viewer")

    try:
        run = True
        while run:
            time.sleep(1/15)
            resized = False

            pygame.display.update()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    run = False

                elif event.type == pygame.VIDEORESIZE:
                    resized = True

                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RIGHT, pygame.K_l):
                        timeline.next_frame()
                    elif event.key in (pygame.K_LEFT, pygame.K_h):
                        timeline.prev_frame()

            width, height = display.get_size()
            v_split = int(height * 0.9)
            h_split = int(width * 0.8)

            display.fill(BLACK)
            timeline.draw(display, events, (0, v_split, width, height-v_split))
            info.draw(display, events, (h_split, 0, width-h_split, v_split))
            preview.draw(display, events, (0, 0, h_split, v_split))
            pygame.draw.line(display, WHITE, (0, v_split), (width, v_split))
            pygame.draw.line(display, WHITE, (h_split, 0), (h_split, v_split))

    finally:
        video.run = False
        time.sleep(0.05)  # Wait for thread to stop

        pygame.quit()
        shutil.rmtree(video.tmpdir)
