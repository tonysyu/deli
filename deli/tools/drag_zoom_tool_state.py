import numpy as np

from traits.api import Either, Float

from ..utils.traits import Alias
from .base_tool import BaseToolState


class AxisDragZoom(BaseToolState):

    canvas = Alias('parent.graph.canvas')
    data_bbox = Alias('parent.graph.canvas.data_bbox')

    _z_prev = Either(None, Float)
    _z_start = Either(None, Float)
    _screen_to_data = Either(None, Float)

    def _get_z(self, event):
        raise NotImplementedError()

    @property
    def data_size(self):
        raise NotImplementedError()

    @property
    def screen_size(self):
        raise NotImplementedError()

    @property
    def z_center(self):
        raise NotImplementedError()

    def _update_data_limits(self, dz):
        raise NotImplementedError()

    def on_enter(self, event):
        self._z_start = self._z_prev = self._get_z(event)
        self._screen_to_data = self.data_size / self.screen_size

    def on_mouse_move(self, event):
        # Calculate data displacement
        z = self._get_z(event)

        dz = self._get_data_stretch(z)
        self._update_data_limits(dz)

        self._z_prev = z
        event.handled = True
        self.parent.graph.request_redraw()

    def on_left_up(self, event):
        self._screen_to_data = self._z_start = self._z_prev = None
        self.exit_state(event)

    def _get_data_stretch(self, z):
        sign = np.sign(self.z_center - self._z_start)
        return sign * (z - self._z_prev) * self._screen_to_data


class DragZoomX(AxisDragZoom):

    def _get_z(self, event):
        return event.x

    @property
    def data_size(self):
        return self.data_bbox.width

    @property
    def screen_size(self):
        return self.canvas.screen_bbox.width

    @property
    def z_center(self):
        return self.parent.graph.x + self.parent.graph.width / 2.0

    def _update_data_limits(self, dx):
        x0, x1 = self.data_bbox.x_limits
        self.data_bbox.x_limits = np.array([(x0 - dx, x1 + dx)])


class DragZoomY(AxisDragZoom):

    def _get_z(self, event):
        return event.y

    @property
    def data_size(self):
        return self.data_bbox.height

    @property
    def screen_size(self):
        return self.canvas.screen_bbox.height

    @property
    def z_center(self):
        return self.parent.graph.y + self.parent.graph.height / 2.0

    def _update_data_limits(self, dy):
        y0, y1 = self.data_bbox.y_limits
        self.data_bbox.y_limits = np.array([(y0 - dy, y1 + dy)])
