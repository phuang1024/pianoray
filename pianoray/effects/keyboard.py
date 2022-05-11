from typing import Tuple

import cv2
import numpy as np

from ..utils import interp
from .effect import Effect


class VideoRead:
    """
    Read frames of a video.
    Maps video frames to client frames.
    """

    def __init__(self, path: str, fps: int, mapping: Tuple[int, int, int, int]):
        """
        Initialize.

        :param path: Path of video.
        :param fps: Client fps.
        :param mapping: Tuple of
            ``(client_start, client_end, src_start, src_end)`` frames.
        """
        self._video = cv2.VideoCapture(path)
        self.mapping = mapping

        # _real_frame stores frame number with first frame of video = 0
        self._real_frame = 0
        self._last = None  # Last read img

        self._read_next()

    def _get_frame(self, frame: int) -> int:
        """
        Return frame of input video corresponding to client's frame.
        """
        f = interp(frame, self.mapping[:2], self.mapping[2:])
        return round(f)

    def _read_next(self):
        """
        Read next frame, store in self._last, and
        increment self._frame.
        """
        ret, img = self._video.read()
        self._real_frame += 1
        if ret:
            self._last = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    def read(self, frame: int) -> np.ndarray:
        """
        Read frame. Pass the frame the client needs.
        Can only read monotonically.
        """
        f = self._get_frame(frame)
        while self._real_frame < f:
            self._read_next()

        return self._last


class Keyboard(Effect):
    """
    Piano keyboard rendering.
    """

    def __init__(self, props, cache, libs, notes) -> None:
        """
        :param notes: Parsed MIDI notes.
        """
        super().__init__(props, cache, libs)

        fps = props.video.fps
        duration = notes[-1].start - notes[0].start
        self.video = VideoRead(props.keyboard.file, fps,
            (0, duration, props.keyboard.start*fps, props.keyboard.end*fps))

        self.compute_crop(props)

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

    def compute_crop(self, props):
        crop = np.array(props.keyboard.crop)
        src_width = np.linalg.norm(crop[1]-crop[0])
        dst_width = props.video.resolution[0]
        scale = src_width / dst_width

        below_len = props.keyboard.below_length * scale
        src_points = np.array(
            (
                crop[0],
                crop[1],
                self.extend_vec(crop[1], crop[2], below_len),
                self.extend_vec(crop[0], crop[3], below_len),
            ),
            dtype=np.float32)

        dst_width = props.video.resolution[0]
        dst_height = np.linalg.norm(src_points[3]-src_points[0]) / scale
        dst_kbd_height = np.linalg.norm(crop[3]-crop[0]) / scale
        dst_width, dst_height, dst_kbd_height = \
            map(int, (dst_width, dst_height, dst_kbd_height))
        dst_points = np.array(
            ((0,0), (dst_width,0), (dst_width,dst_height), (0,dst_height)),
            dtype=np.float32)

        mask = np.empty((dst_height, dst_width, 3), dtype=np.float32)
        for y in range(dst_height):
            if y < dst_kbd_height:
                fac = 1
            else:
                fac = np.interp(y, (dst_kbd_height, dst_height), (0, 1))
                fac **= 2
                fac = np.interp(fac, (0, 1), (1, 0.4))

            mask[y, :] = fac

        self.persp = cv2.getPerspectiveTransform(src_points, dst_points)
        self.dst_shape = (dst_width, dst_height)
        self.mask = mask

    def render(self, props, img: np.ndarray, frame: int):
        """
        Render the keyboard.
        """
        dst = self.dst_shape

        kbd = self.video.read(frame)
        kbd = cv2.warpPerspective(kbd, self.persp, dst).astype(np.float64)
        kbd *= self.mask

        kbd *= props.keyboard.dim_mult
        kbd += props.keyboard.dim_add
        kbd[kbd<0] = 0
        kbd[kbd>255] = 255
        kbd = kbd.astype(np.uint8)

        half = int(props.video.resolution[1] / 2)
        img[half:half+dst[1], 0:dst[0], ...] = kbd

        # Octave lines
        if props.keyboard.octave_lines:
            self.libs["keyboard"].render_octave_lines(
                img, img.shape[1], img.shape[0])
