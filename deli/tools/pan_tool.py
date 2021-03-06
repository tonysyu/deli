import numpy as np
from traits.api import CArray

from ..utils.traits import Alias
from .base_tool import BaseTool, BaseToolState


class PanTool(BaseTool):

    def _state_handlers_default(self):
        return {'dragging': DraggingState(self)}

    def on_left_down(self, event):
        self.state_change(event, new_state='dragging')


class DraggingState(BaseToolState):

    graph = Alias('component')
    canvas = Alias('graph.canvas')

    _last_position = CArray

    def on_enter(self, event):
        self._last_position = np.array((event.x, event.y))

    def on_mouse_move(self, event):
        x0, y0, width, height = self.canvas.data_bbox.rect

        position = np.array((event.x, event.y))
        points = np.array([self._last_position, position])
        points = self.canvas.screen_to_data.transform(points)

        dx, dy = np.diff(points, axis=0)[0]
        # Save position for next call.
        self._last_position = position

        self.canvas.data_bbox.rect = x0 - dx, y0 - dy, width, height
        self.component.request_redraw()

    def on_left_up(self, event):
        self._last_position = ()
        self.exit_state(event)
