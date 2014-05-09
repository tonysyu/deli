from numpy import linspace

from enable.api import Component, ComponentEditor
from traits.api import HasStrictTraits, Instance
from traitsui.api import UItem, View

from deli.plot import Plot
from deli.tools.data_cursor_tool import DataCursorTool
from deli.utils.data_structures import NoisyDict


class Demo(HasStrictTraits):
    plot = Instance(Component)

    traits_view = View(
        UItem('plot', editor=ComponentEditor(size=(900, 500))),
        resizable=True, title="Basic x-y plots"
    )

    def _plot_default(self):
        x = y = linspace(0, 1)
        pd = NoisyDict(x=x, y=y)

        plot = Plot(data=pd)
        plot.title.text = "Line Plot"
        renderer = plot.plot(('x', 'y'))[0]

        # DataCursorTool.attach_to(renderer)
        tool = DataCursorTool(component=renderer)
        renderer.overlays.append(tool)
        renderer.tools.append(tool)
        renderer.active_tool = tool
        plot.active_tool = tool
        return plot


if __name__ == '__main__':
    demo = Demo()
    demo.configure_traits()
