import numpy as np

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
        x = np.linspace(0, 2 * np.pi)
        pd = NoisyDict(x=x, y1=np.sin(x), y2=np.cos(x))

        plot = Plot(data=pd)
        plot.title.text = "Line Plot"

        for y_name, color in zip(('y1', 'y2'), ('black', 'red')):
            renderer = plot.plot(('x', y_name), color=color)[0]
            DataCursorTool.attach_to(renderer)

        return plot


if __name__ == '__main__':
    demo = Demo()
    demo.configure_traits()
