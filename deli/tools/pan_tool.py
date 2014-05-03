import numpy as np
from traits.api import CArray, Either, Enum

from .base_tool import BaseTool


class PanTool(BaseTool):

    _last_position = Either(None, CArray)

    event_state = Enum('normal', 'dragging')

    def normal_left_down(self, event):
        self.event_state = 'dragging'
        self._last_position = np.array((event.x, event.y))

    def dragging_mouse_move(self, event):
        x0, y0, width, height = self.component.data_bbox.bounds

        position = np.array((event.x, event.y))
        points = np.array([self._last_position, position])
        points = self.component.screen_to_data.transform(points)

        dx, dy = np.diff(points, axis=0)[0]
        # Save position for next call.
        self._last_position = position

        self.component.data_bbox.bounds = x0 - dx, y0 - dy, width, height
        self.component.request_redraw()

    def dragging_left_up(self, event):
        self.event_state = 'normal'
        self._last_position = None
