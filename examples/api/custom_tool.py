from numpy import linspace

from enable.api import Component, ComponentEditor
from traits.api import HasStrictTraits, Instance
from traitsui.api import UItem, View

from deli.plot_canvas import PlotCanvas
from deli.tools.base_tool import BaseTool, BaseToolState
from deli.tools.key_spec import KeySpec, shift_key
from deli.utils.data_structures import NoisyDict


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


class Demo(HasStrictTraits):
    canvas = Instance(Component)

    traits_view = View(
        UItem('canvas', editor=ComponentEditor(size=(900, 500))),
        resizable=True, title="Basic x-y plots"
    )

    def _canvas_default(self):
        x = y = linspace(0, 1)
        pd = NoisyDict(x=x, y=y)

        canvas = PlotCanvas(data=pd)
        canvas.title.text = "Line Plot"
        canvas.plot(('x', 'y'))

        PrintTool.attach_to(canvas)
        return canvas


if __name__ == '__main__':
    demo = Demo()
    demo.configure_traits()
