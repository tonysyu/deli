import numpy as np
from traits.api import CArray, Instance, Str

from ..abstract_overlay import AbstractOverlay
from ..artist.label_artist import LabelArtist
from ..renderer.base_point_renderer import BasePointRenderer
from .base_tool import BaseTool


DEFAULT_LABEL_STYLE = {'x_origin': 'left', 'x_offset': 20}


def draw_box(gc, rect, edge_color, fill_color):
    with gc:
        gc.set_stroke_color(edge_color)
        gc.set_fill_color(fill_color)
        gc.draw_rect([int(a) for a in rect])
        gc.fill_path()


class DataCursorOverlay(AbstractOverlay):

    label = Instance(LabelArtist, DEFAULT_LABEL_STYLE)

    _origin = CArray

    _text = Str

    def update_point(self, data_point, screen_point):
        self._text = self.data_point_to_string(data_point)

        data_to_screen = self.component.data_to_screen.transform
        self._origin = data_to_screen(data_point)
        self.component.request_redraw()

    def data_point_to_string(self, point):
        return str(point)

    def overlay(self, component, gc, view_bounds=None, mode="normal"):
        self._draw_overlay(gc, view_bounds, mode)

    def _draw_overlay(self, gc, view_bounds=None, mode="normal"):
        if len(self._text) == 0:
            return

        with gc:
            gc.translate_ctm(*self._origin)
            width, height = self.label.get_size(gc, self._text)

            x_bbox_offset = (self.label._x_offset_factor * width
                             + self.label.x_offset)
            y_bbox_offset = (self.label._y_offset_factor * height
                             + self.label.y_offset)

            rect = (x_bbox_offset, y_bbox_offset, width, height)
            draw_box(gc, rect, (0, 0, 0, 1), (1, 1, 0, 1))
            self.label.draw(gc, self._text)


class DataCursorTool(BaseTool):

    component = Instance(BasePointRenderer)

    overlay = Instance(AbstractOverlay)

    visible=True

    def _overlay_default(self):
        return DataCursorOverlay(component=self.component)

    def on_mouse_move(self, event):
        x_data = self.component.x_src.get_data()
        y_data = self.component.y_src.get_data()

        screen_to_data = self.component.screen_to_data.transform
        x_cursor, y_cursor = screen_to_data((event.x, event.y))
        i = np.argmin(np.abs(x_data - x_cursor))

        self._update_overlay((x_data[i], y_data[i]))

    def _update_overlay(self, data_point):
        data_to_screen = self.component.data_to_screen.transform
        self.overlay.update_point(data_point, data_to_screen(data_point))
        self.component.request_redraw()
