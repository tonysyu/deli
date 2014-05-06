from numpy import linspace
from scipy.special import jn

from enable.api import Component, ComponentEditor
from traits.api import HasStrictTraits, Instance
from traitsui.api import UItem, View

from deli.plot import Plot
from deli.tools.pan_tool import PanTool
from deli.tools.zoom_tool import ZoomTool
from deli.utils.data_structures import NoisyDict


class Demo(HasStrictTraits):
    plot = Instance(Component)

    traits_view = View(
        UItem('plot', editor=ComponentEditor(size=(900, 500))),
        resizable=True, title="Basic x-y plots"
    )

    def _plot_default(self):
        x = linspace(-2.0, 10.0, 100)
        pd = NoisyDict(x=x)
        for i in range(5):
            pd['y' + str(i)] = jn(i, x)

        plot = Plot(data=pd)
        plot.title.text = "Line Plot"
        plot.plot(('x', 'y0', 'y1', 'y2'), color='red')
        plot.plot(('x', 'y3'), color='blue')

        ZoomTool.attach_to(plot)
        PanTool.attach_to(plot)

        return plot


if __name__ == '__main__':
    demo = Demo()
    demo.configure_traits()
