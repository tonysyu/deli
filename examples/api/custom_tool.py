from numpy import linspace

from traits.api import Instance

from deli.demo_utils import TraitsWindow
from deli.graph import Graph
from deli.plots.line_plot import LinePlot
from deli.tools.base_tool import BaseTool, BaseToolState
from deli.tools.key_spec import KeySpec, shift_key


class PrintTool(BaseTool):
    """ Tool that prints current mouse position if the shift-key is pressed.

    This tool delegates the actual action to PrintOnMove.
    """

    print_key = shift_key

    def _state_handlers_default(self):
        return {'print': PrintOnMove(self, enabling_key=self.print_key)}

    def on_key_pressed(self, event):
        if self.print_key.match(event):
            self.state_change(event, new_state='print')


class PrintOnMove(BaseToolState):
    """ Tool state that prints the current position when the mouse is moved.

    Note that this class returns control to the parent tool when the enabling
    key is released.
    """

    enabling_key = Instance(KeySpec)

    def on_mouse_move(self, event):
        print "Mouse at ({}, {})".format(event.x, event.y)

    def on_key_released(self, event):
        if self.enabling_key.match(event):
            self.exit_state(event)


class Demo(TraitsWindow):

    def setup_graph(self):
        graph = Graph()
        graph.title.text = "Line Plot"

        x = y = linspace(0, 1)
        plot = LinePlot(x_data=x, y_data=y)
        graph.add_plot(plot)

        PrintTool.attach_to(graph.canvas)
        return graph


if __name__ == '__main__':
    demo = Demo()
    demo.configure_traits()
