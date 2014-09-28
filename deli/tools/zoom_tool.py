from traits.api import Float

from ..utils.traits import Alias
from .base_tool import BaseTool
from .key_spec import KeySpec
from .drag_zoom_tool_state import DragZoomX, DragZoomY


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


def point_in_x_axis_area(graph, x, y):
    margin = graph.margin
    if y > margin:
        return False
    return margin < x < (graph.width - margin)


def point_in_y_axis_area(graph, x, y):
    margin = graph.margin
    if x > margin:
        return False
    return margin < y < (graph.height - margin)


class ZoomTool(BaseTool):

    graph = Alias('component')

    key_zoom_in = KeySpec(['+', '='], ignore='shift')
    key_zoom_out = KeySpec('-')

    # Enabling key for mouse interaction.
    enabling_key = KeySpec(None, modifier='shift')

    zoom_factor = Float(2)

    def _state_handlers_default(self):
        return {'drag_zoom_x': DragZoomX(self),
                'drag_zoom_y': DragZoomY(self)}

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

    def on_left_down(self, event):
        if not self.enabling_key.match(event):
            return
        if point_in_x_axis_area(self.graph, event.x, event.y):
            self.state_change(event, new_state='drag_zoom_x')
        elif point_in_y_axis_area(self.graph, event.x, event.y):
            self.state_change(event, new_state='drag_zoom_y')
