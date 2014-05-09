import numpy as np
from traits.api import CArray, Instance, Str

from ..abstract_overlay import AbstractOverlay
from ..artist.label_artist import LabelArtist
from ..renderer.base_point_renderer import BasePointRenderer
from .base_tool import BaseTool


class DataCursorTool(BaseTool, AbstractOverlay):

    component = Instance(BasePointRenderer)

    label = Instance(LabelArtist, {'x_origin': 'left', 'x_offset': 20})

    _origin = CArray
    _label = Str

    visible=True

    def data_point_to_string(self, point):
        return str(point)

    def on_mouse_move(self, event):
        x_data = self.component.x_src.get_data()
        y_data = self.component.y_src.get_data()
        screen_to_data = self.component.screen_to_data.transform
        data_to_screen = self.component.data_to_screen.transform

        x_cursor, y_cursor = screen_to_data((event.x, event.y))
        i = np.argmin(np.abs(x_data - x_cursor))
        self._label = self.data_point_to_string((x_data[i], y_data[i]))
        self._origin = data_to_screen((x_data[i], y_data[i]))
        self.component.request_redraw()

    def overlay(self, component, gc, view_bounds=None, mode="normal"):
        self._draw_overlay(gc, view_bounds, mode)

    def _draw_overlay(self, gc, view_bounds=None, mode="normal"):
        if len(self._label) == 0:
            return

        with gc:
            gc.translate_ctm(*self._origin)
            self.label.draw(gc, self._label)
