import numpy as np
from traits.api import CArray, Instance, Str

from ..abstract_overlay import AbstractOverlay
from ..artist.label_artist import LabelArtist
from ..renderer.base_point_renderer import BasePointRenderer
from .base_tool import BaseTool


DEFAULT_LABEL_STYLE = {'x_origin': 'left', 'x_offset': 20}


class DataCursorOverlay(AbstractOverlay):

    origin = CArray

    text = Str

    label = Instance(LabelArtist, DEFAULT_LABEL_STYLE)

    def overlay(self, component, gc, view_bounds=None, mode="normal"):
        self._draw_overlay(gc, view_bounds, mode)

    def _draw_overlay(self, gc, view_bounds=None, mode="normal"):
        if len(self.text) == 0:
            return

        with gc:
            gc.translate_ctm(*self.origin)
            self.label.draw(gc, self.text)


class DataCursorTool(BaseTool):

    component = Instance(BasePointRenderer)

    overlay = Instance(AbstractOverlay)

    visible=True

    def _overlay_default(self):
        return DataCursorOverlay(component=self.component)

    def data_point_to_string(self, point):
        return str(point)

    def on_mouse_move(self, event):
        x_data = self.component.x_src.get_data()
        y_data = self.component.y_src.get_data()

        screen_to_data = self.component.screen_to_data.transform
        x_cursor, y_cursor = screen_to_data((event.x, event.y))
        i = np.argmin(np.abs(x_data - x_cursor))

        self._update_overlay((x_data[i], y_data[i]))

    def _update_overlay(self, data_point):
        self.overlay.text = self.data_point_to_string(data_point)

        data_to_screen = self.component.data_to_screen.transform
        self.overlay.origin = data_to_screen(data_point)
        self.component.request_redraw()
