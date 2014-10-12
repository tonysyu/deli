from __future__ import absolute_import

import numpy as np
from kiva.basecore2d import GraphicsState

from vispy import gloo
from vispy.util.transforms import ortho

from .lines import LineElement
from .markers import MarkerElement
from .rect import RectElement


identity_transform = np.eye(4, dtype=np.float32)


class GraphicsContext(object):

    def __init__(self, size):
        gloo.set_viewport(0, 0, *size)

        self._size = size
        self._gl_elements = []
        self._state = GraphicsState()
        self._state.ctm = (0, 0)
        self._state_stack = [self._state]

    def render(self, event):
        for element in self._gl_elements:
            element.draw()
        self._gl_elements = []

    def clear(self, *args):
        pass

    def __enter__(self):
        # Set new state to copy of present state (which can be modified.
        self._state = self._state.copy()
        self._state_stack.append(self._state)

    def __exit__(self, type, value, traceback):
        self._state = self._state_stack.pop()

    def translate_ctm(self, dx, dy):
        # XXX: This is just a hack to fake offsets
        x, y = self._state.ctm
        self._state.ctm = (x+dx, y+dy)

    def rotate_ctm(self, radian_angle):
        pass

    def set_font(self, font):
        pass

    def set_text_position(self, x, y):
        pass

    def get_full_text_extent(self, text):
        return 1, 1, 0, 0

    def show_text(self, text):
        pass

    def set_antialias(self, antialias):
        self._state.antialias = antialias

    def set_alpha(self, alpha):
        self._state.line_color = alpha

    def set_stroke_color(self, color):
        self._state.line_color = color

    def set_fill_color(self, color):
        self._state.fill_color = color

    def set_line_width(self, width):
        self._state.line_width = width

    def set_line_dash(self, dash):
        self._state.line_dash = dash

    def lines(self, points):
        self._points.append(points)

    def line_set(self, starts, ends):
        points = np.zeros((len(starts) * 2, 2), dtype=starts.dtype)
        points[::2] = starts
        points[1::2] = ends
        self._add_element(LineElement(points, self._state, segments=True))

    def begin_path(self):
        self._points = []

    def stroke_path(self):
        if len(self._points) == 0:
            return
        self._add_element(LineElement(self._points, self._state))
        self._points = []

    def fill_path(self):
        pass

    def draw_marker_at_points(self, points, size=5, marker='disc'):
        # XXX: Pass marker shape to the element.
        self._add_element(MarkerElement(points, self._state,
                                        size=size, marker='disc'))

    def draw_rect(self, rect):
        self._add_element(RectElement(rect, self._state))

    def clip_to_rect(self, *rect):
        pass

    def _add_element(self, element):
        x, y = self._state.ctm
        width, height = self._size

        # Translate model in world coordinates
        model = identity_transform.copy()
        model[3, :2] = (x, y)

        element['u_projection'] = ortho(0, width, 0, height, -1, 1)
        element["u_view"] = identity_transform
        element["u_model"] = model
        element["u_antialias"] = 1
        element["u_size"] = 1
        self._gl_elements.append(element)
