import numpy as np
from traits.api import CArray, Either

from .base_tool import BaseTool, BaseToolState


class PanTool(BaseTool):

    def _state_handlers_default(self):
        return {'dragging': DraggingState(self)}

    def on_left_down(self, event):
        self.state_change(event, new_state='dragging')


class DraggingState(BaseToolState):

    _last_position = Either(None, CArray)

    def on_enter(self, event):
        self._last_position = np.array((event.x, event.y))

    def on_mouse_move(self, event):
        x0, y0, width, height = self.component.data_bbox.bounds

        position = np.array((event.x, event.y))
        points = np.array([self._last_position, position])
        points = self.component.screen_to_data.transform(points)

        dx, dy = np.diff(points, axis=0)[0]
        # Save position for next call.
        self._last_position = position

        self.component.data_bbox.bounds = x0 - dx, y0 - dy, width, height
        self.component.request_redraw()

    def on_left_up(self, event):
        self._last_position = None
        self.exit_state(event)
