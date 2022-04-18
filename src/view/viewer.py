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

import time

import pygame

from .. import logger
from .video import Video

pygame.init()


def view_video(path: str) -> None:
    video = Video(path)
    logger.info(f"Extracting frames to {video.tmpdir}")
    logger.warn("This feature is not complete yet.")

    resized = False  # Redraw if resized
    display = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    pygame.display.set_caption("PianoRay Viewer")

    run = True
    while run:
        time.sleep(1/30)
        pygame.display.update()
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.VIDEORESIZE:
                resized = True

        display.fill((0, 0, 0))

    pygame.quit()
    video.run = False
