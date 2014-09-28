from traits.api import Float

from ..utils.traits import Alias
from .base_tool import BaseTool
from .key_spec import KeySpec


def zoom_out_centered_rect(rect, size_scale, offset_scale=None):
    x, y, width, height = rect
    if offset_scale is None:
        offset_scale = size_scale / 4.0
    return (x - offset_scale*width, y - offset_scale*height,
            size_scale*width, size_scale*height)


def zoom_in_centered_rect(rect, size_scale):
    size_scale = 1.0/size_scale
    offset_scale = -size_scale / 2.0
    return zoom_out_centered_rect(rect, size_scale, offset_scale)


class ZoomTool(BaseTool):

    graph = Alias('component')

    key_zoom_in = KeySpec(['+', '='], ignore='shift')
    key_zoom_out = KeySpec('-')

    zoom_factor = Float(2)

    def on_key_press(self, event):
        rect = self.graph.canvas.data_bbox.rect
        if self.key_zoom_in.match(event):
            new_rect = zoom_in_centered_rect(rect, self.zoom_factor)
        elif self.key_zoom_out.match(event):
            new_rect = zoom_out_centered_rect(rect, self.zoom_factor)
        else:
            return

        self.graph.canvas.data_bbox.rect = new_rect
        self.graph.request_redraw()
