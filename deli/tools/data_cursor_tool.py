import numpy as np
from traits.api import CArray, HasStrictTraits, Instance, Str

from ..abstract_overlay import AbstractOverlay
from ..artist.flag_label_artist import FlagLabelArtist
from ..renderer.base_point_renderer import BasePointRenderer
from .base_tool import BaseTool


def choose_black_or_white(contrasting_color, threshold=0.33):
    """ Return black or white to maximize contrast with an input color.

    Parameters
    ----------
    contrasting_color : array, length 3 or 4
        The color which we want to contrast with.
    """
    gray = np.mean(contrasting_color[:3])
    return 'black' if gray > threshold else 'white'


class DataCursorOverlay(AbstractOverlay):

    label = Instance(HasStrictTraits)

    _origin = CArray

    _text = Str

    def _label_default(self):
        return FlagLabelArtist()

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
            self.label.draw(gc, self._text)


class DataCursorTool(BaseTool):

    component = Instance(BasePointRenderer)

    overlay = Instance(AbstractOverlay)

    visible=True

    def _overlay_default(self):
        return DataCursorOverlay(component=self.component)

    def _component_changed(self):
        flag_color_name = self.component.line.color
        flag_color = self.component.line.color_
        self.overlay.label.edge_color = flag_color_name
        self.overlay.label.fill_color = flag_color_name
        self.overlay.label.text_color = choose_black_or_white(flag_color)

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
