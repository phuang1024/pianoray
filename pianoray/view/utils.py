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

import numpy as np
import pygame

pygame.init()

TMP = "/tmp"

BLACK = np.array((0, 0, 0))
DARK_GRAY = np.array((50, 50, 50))
GRAY = np.array((120, 120, 120))
LIGHT_GRAY = np.array((170, 170, 170))
WHITE = np.array((255, 255, 255))
BLUE = np.array((130, 130, 255))

FONT_MED = pygame.font.SysFont("ubuntu", 18)
