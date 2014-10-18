from __future__ import absolute_import

import numpy as np
from kiva.basecore2d import GraphicsState as BaseGraphicsState

from vispy import gloo
from vispy.util.transforms import ortho

from .lines import LineElement
from .markers import MarkerElement
from .rect import RectElement
from .text import TextElement


identity_transform = np.eye(4, dtype=np.float32)


class GraphicsState(BaseGraphicsState):

    def __init__(self, *args, **kwargs):
        super(GraphicsState, self).__init__(*args, **kwargs)
        self.rect_clip = None


class GraphicsContext(object):

    def __init__(self, size):
        gloo.set_viewport(0, 0, *size)

        self._size = size
        self._state = GraphicsState()
        self._state.ctm = (0, 0)
        self._state_stack = [self._state]

        self._line_renderer = LineElement()
        self._marker_renderer = MarkerElement()
        self._rect_renderer = RectElement()
        self._text_renderer = TextElement()

        self._text_pos = (0, 0)

    def render(self, event):
        pass

    def clear(self, *args):
        gloo.clear()

    def __enter__(self):
        # Set new state to copy of present state (which can be modified.
        self._state_stack.append(self._state)
        self._state = self._state.copy()

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
        """ Set relative text position.

        The absolute position depends on the current transform matrix as well.
        """
        self._text_pos = (x, y)

    def get_full_text_extent(self, text):
        return 1, 1, 0, 0

    def show_text(self, text):
        self._update_renderer(self._text_renderer, self._state)
        self._text_renderer.update(self._state, text)
        self._text_renderer.draw()

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

        self._update_renderer(self._line_renderer, self._state)
        self._line_renderer.update(self._state, points, segments=True)
        self._line_renderer.draw()

    def begin_path(self):
        self._points = []

    def stroke_path(self):
        if len(self._points) == 0:
            return

        self._update_renderer(self._line_renderer, self._state)
        self._line_renderer.update(self._state, self._points)
        self._line_renderer.draw()
        self._points = []

    def fill_path(self):
        pass

    def draw_marker_at_points(self, points, size=5, marker='disc'):
        # XXX: TODO: pass marker shape to the element.
        kwargs = {'size': size, 'marker': 'disc'}
        self._update_renderer(self._marker_renderer, self._state)
        self._marker_renderer.update(self._state, points, **kwargs)
        self._marker_renderer.draw()

    def draw_rect(self, rect):
        self._update_renderer(self._rect_renderer, self._state)
        self._rect_renderer.update(self._state, rect)
        self._rect_renderer.draw()

    def clip_to_rect(self, *rect):
        x0, y0 = self._state.ctm
        x, y, width, height = rect
        self._state.rect_clip = (x0+x, y0+y, width, height)

    def _update_renderer(self, renderer, state):
        width, height = self._size

        # Translate model in world coordinates
        model = identity_transform.copy()
        model[3, :2] = state.ctm

        renderer['u_projection'] = ortho(0, width, 0, height, -1, 1)
        renderer["u_view"] = identity_transform
        renderer["u_model"] = model
        renderer["u_antialias"] = 1
        renderer["u_size"] = 1
