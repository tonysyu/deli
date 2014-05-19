import numpy as np
from traits.api import CArray, HasStrictTraits, Instance, Str

from ..abstract_overlay import AbstractOverlay
from ..artist.flag_label_artist import FlagLabelArtist
from ..plots.base_point_plot import BasePointPlot
from ..utils.text import switch_delimiters
from .base_tool import BaseTool


def format_floats(array, significant_digits=3):
    """ Return string version of floats in array. """
    max_digit = np.max(np.abs(array))
    if max_digit != 0:
        max_digit = np.log10(max_digit)
    max_digit -= (significant_digits - 1)
    if max_digit < 0:
        precision = np.ceil(-max_digit)
    text = np.array2string(np.asarray(array), separator=',',
                           precision=precision)
    return switch_delimiters(text, '[]', '()')


def choose_black_or_white(contrasting_color, threshold=0.4):
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

    def reset(self):
        self._text = ''
        self._origin = np.empty((0, 2))

    def update_point(self, data_point, screen_point):
        self._text = self.data_point_to_string(data_point)
        self._origin = screen_point
        self.component.request_redraw()

    def data_point_to_string(self, point):
        return format_floats(point)

    def draw(self, component, gc, view_bounds=None):
        self._draw_overlay(gc, view_bounds)

    def _draw_overlay(self, gc, view_bounds=None):
        if len(self._text) == 0:
            return

        with gc:
            gc.translate_ctm(*self._origin)
            self.label.draw(gc, self._text)


class DataCursorTool(BaseTool):

    component = Instance(BasePointPlot)

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
        screen_point = data_to_screen(data_point)
        if self.component.is_in(*screen_point):
            self.overlay.update_point(data_point, screen_point)
        else:
            self.overlay.reset()
        self.component.request_redraw()

    def on_mouse_leave(self, event):
        self.overlay.reset()
        self.component.request_redraw()
