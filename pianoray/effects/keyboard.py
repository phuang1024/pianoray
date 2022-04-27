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
import numpy as np

from .effect import Effect


class VideoRead:
    """
    Read frames of a video.
    The class internally accommodates for FPS.
    """
    # Video fps is in_fps, client fps is out_fps
    in_fps: int
    out_fps: int

    def __init__(self, path: str, fps: int, offset: int = 0):
        """
        Initialize.

        :param path: Path of video.
        :param fps: The FPS the client is rendering at.
            i.e. settings.video.fps
        :param offset: Timestamp, in seconds, of the frame that will
            be considered frame 0.
        """
        self._video = cv2.VideoCapture(path)

        self.in_fps = self._video.get(cv2.CAP_PROP_FPS)
        self.out_fps = fps

        # _frame stores frame number with first note = 0
        # _real_frame stores frame number with first frame of video=0
        self._frame = int(-1 * offset * self.in_fps)
        self._real_frame = 0
        self._last = None

    def _get_frame(self, frame: int) -> int:
        """
        Return frame of input video corresponding to
        client's frame.
        """
        f = frame * self.in_fps / self.out_fps
        return round(f)

    def _read_next(self, inc: bool = True):
        """
        Read next frame, store in self._last, and
        increment self._frame.

        :param inc: Whether to increment.
        """
        ret, img = self._video.read()
        self._real_frame += 1
        if inc:
            self._frame += 1
        if ret:
            self._last = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    def read(self, frame: int) -> np.ndarray:
        """
        Read frame. Pass the frame the client needs.
        Currently can only read monotonically.
        """
        f = self._get_frame(frame)
        if f < self._frame:
            raise ValueError("VideoRead can only read monotonically.")

        while self._frame < f:
            self._read_next()

        return self._last


class Keyboard(Effect):
    """
    Piano keyboard rendering.
    """

    def __init__(self, settings, cache, libs) -> None:
        assert settings.keyboard.file is not None

        super().__init__(settings, cache, libs)
        self.video = VideoRead(settings.keyboard.file,
            settings.video.fps, settings.keyboard.start)

        self.compute_crop(settings)

    @staticmethod
    def extend_vec(v1, v2, length):
        """
        Let u be the unit vector in the direction from v1 to v2.
        Let v be u * length.
        Returns v + v2
        """
        diff = v2 - v1
        u = diff / np.linalg.norm(diff)
        v = u * length
        return v + v2

    def compute_crop(self, settings):
        crop = np.array(settings.keyboard.crop)
        src_width = np.linalg.norm(crop[1]-crop[0])
        dst_width = settings.video.resolution[0]
        scale = src_width / dst_width

        below_len = settings.keyboard.below_length * scale
        src_points = np.array(
            (
                crop[0],
                crop[1],
                self.extend_vec(crop[1], crop[2], below_len),
                self.extend_vec(crop[0], crop[3], below_len),
            ),
            dtype=np.float32)

        dst_width = settings.video.resolution[0]
        dst_height = np.linalg.norm(src_points[3]-src_points[0]) / scale
        dst_kbd_height = np.linalg.norm(crop[3]-crop[0]) / scale
        dst_width, dst_height, dst_kbd_height = \
            map(int, (dst_width, dst_height, dst_kbd_height))
        dst_points = np.array(
            ((0,0), (dst_width,0), (dst_width,dst_height), (0,dst_height)),
            dtype=np.float32)

        mask = np.empty((dst_height, dst_width, 3), dtype=np.float32)
        for y in range(dst_height):
            fac = 1 if y < dst_kbd_height else \
                np.interp(y, (dst_kbd_height, dst_height), (1, 0))
            mask[y, :] = fac

        self.persp = cv2.getPerspectiveTransform(src_points, dst_points)
        self.dst_shape = (dst_width, dst_height)
        self.mask = mask

    def render(self, settings, img: np.ndarray, frame: int):
        """
        Render the keyboard.
        """
        dst = self.dst_shape

        kbd = self.video.read(frame)
        kbd = cv2.warpPerspective(kbd, self.persp, dst).astype(np.float64)
        kbd *= self.mask

        kbd *= settings.keyboard.dim_mult
        kbd += settings.keyboard.dim_add
        kbd[kbd<0] = 0
        kbd[kbd>255] = 255
        kbd = kbd.astype(np.uint8)

        half = int(settings.video.resolution[1] / 2)
        img[half:half+dst[1], 0:dst[0], ...] = kbd
