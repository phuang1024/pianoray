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
from .timeline import Timeline
from .video import Video

pygame.init()


def view_video(path: str) -> None:
    logger.warn("Viewer is not complete yet.")

    video = Video(path)
    timeline = Timeline(video)
    logger.info(f"Extracting frames to {video.tmpdir}")

    resized = False  # Redraw if resized
    display = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    pygame.display.set_caption("PianoRay Viewer")

    try:
        run = True
        while run:
            time.sleep(1/30)
            resized = False
    
            pygame.display.update()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.VIDEORESIZE:
                    resized = True
    
            width, height = display.get_size()
            v_split = int(height * 0.9)
            h_split = int(width * 0.8)
    
            timeline.draw(display, events, (0, v_split, width, height-v_split))

    finally:
        video.run = False
        time.sleep(0.05)  # Wait for thread to stop
    
        pygame.quit()
        shutil.rmtree(video.tmpdir)
