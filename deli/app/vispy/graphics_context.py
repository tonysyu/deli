from __future__ import absolute_import

import numpy as np
from kiva.basecore2d import GraphicsState as BaseGraphicsState

from vispy import gloo
from vispy.util.transforms import ortho

from .lines import LineElement
from .markers import MarkerElement
from .rect import RectElement


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

        self._draw_stack = []
        self._line_renderer = LineElement()
        self._marker_renderer = MarkerElement()
        self._rect_renderer = RectElement()

    def render(self, event):
        # Scissors, i.e. clipping, need to be turned off after drawing so
        # previous clip planes don't persist.
        for renderer, state, args, kwargs in self._draw_stack:
            self._update_renderer(renderer, state, *args, **kwargs)
            renderer.draw()
        self._draw_stack = []

    def clear(self, *args):
        pass

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

        state = self._state.copy()
        args = [points]
        kwargs = {'segments': True}
        self._draw_stack.append((self._line_renderer, state, args, kwargs))

    def begin_path(self):
        self._points = []

    def stroke_path(self):
        if len(self._points) == 0:
            return

        state = self._state.copy()
        args = [self._points[:]]
        self._draw_stack.append((self._line_renderer, state, args, {}))
        self._points = []

    def fill_path(self):
        pass

    def draw_marker_at_points(self, points, size=5, marker='disc'):

        state = self._state.copy()
        args = [points]
        # XXX: TODO: pass marker shape to the element.
        kwargs = {'size': size, 'marker': 'disc'}
        self._draw_stack.append((self._marker_renderer, state, args, kwargs))

    def draw_rect(self, rect):
        state = self._state.copy()
        args = [rect]
        self._draw_stack.append((self._rect_renderer, state, args, {}))

    def clip_to_rect(self, *rect):
        x0, y0 = self._state.ctm
        x, y, width, height = rect
        self._state.rect_clip = (x0+x, y0+y, width, height)

    def _update_renderer(self, renderer, state, *args, **kwargs):
        x, y = state.ctm
        width, height = self._size

        # Translate model in world coordinates
        model = identity_transform.copy()
        model[3, :2] = (x, y)

        renderer['u_projection'] = ortho(0, width, 0, height, -1, 1)
        renderer["u_view"] = identity_transform
        renderer["u_model"] = model
        renderer["u_antialias"] = 1
        renderer["u_size"] = 1
        renderer.update(state, *args, **kwargs)
