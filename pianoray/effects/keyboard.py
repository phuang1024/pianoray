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

        # Compute perspective warp
        crop = np.array(settings.keyboard.crop)
        src_width = np.linalg.norm(crop[1]-crop[0])
        src_height = np.linalg.norm(crop[3]-crop[0])
        dst_width = settings.video.resolution[0]
        dst_height = dst_width * src_height / src_width

        width = settings.video.resolution[0]
        half = settings.video.resolution[1] / 2
        src_points = crop.astype(np.float32)
        dst_points = np.array(
            ((0,0), (width,0), (width,dst_height), (0,dst_height)),
            dtype=np.float32)

        self.persp = cv2.getPerspectiveTransform(src_points, dst_points)
        self.dst_shape = (int(dst_width), int(dst_height))

    def render(self, settings, img: np.ndarray, frame: int):
        """
        Render the keyboard.
        """
        dst = self.dst_shape

        kbd = self.video.read(frame)
        kbd = cv2.warpPerspective(kbd, self.persp, dst)

        half = int(settings.video.resolution[1] / 2)
        img[half:half+dst[1], 0:dst[0], ...] = kbd
