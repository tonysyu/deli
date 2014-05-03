from traits.api import Float

from .base_tool import BaseHandlerMethodTool
from .key_spec import KeySpec


def zoom_out_centered_bounds(bounds, size_scale, offset_scale=None):
    x, y, width, height = bounds
    if offset_scale is None:
        offset_scale = size_scale / 4.0
    return (x - offset_scale*width, y - offset_scale*height,
           size_scale*width, size_scale*height)


def zoom_in_centered_bounds(bounds, size_scale):
    size_scale = 1.0/size_scale
    offset_scale = -size_scale / 2.0
    return zoom_out_centered_bounds(bounds, size_scale, offset_scale)


class ZoomTool(BaseHandlerMethodTool):

    key_zoom_in = KeySpec(['+', '='], ignore='shift')
    key_zoom_out = KeySpec('-')

    zoom_factor = Float(2)

    def normal_key_pressed(self, event):
        bounds = self.component.data_bbox.bounds
        if self.key_zoom_in.match(event):
            new_bounds = zoom_in_centered_bounds(bounds, self.zoom_factor)
        elif self.key_zoom_out.match(event):
            new_bounds = zoom_out_centered_bounds(bounds, self.zoom_factor)
        else:
            return

        self.component.data_bbox.bounds = new_bounds
        self.component.request_redraw()
