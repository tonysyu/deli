from numpy import linspace
from scipy.special import jn

from enable.api import Component, ComponentEditor
from traits.api import HasStrictTraits, Instance
from traitsui.api import Item, Group, View

from deli.utils.data_structures import NoisyDict
from deli.plot import Plot


class Demo(HasStrictTraits):
    plot = Instance(Component)

    traits_view = View(
        Group(
            Item(
                'plot',
                editor=ComponentEditor(size=(900, 500)),
                show_label=False
            ),
            orientation='vertical'),
        resizable=True, title="Basic x-y plots"
    )

    def _plot_default(self):
        # Create some x-y data series to plot
        x = linspace(-2.0, 10.0, 100)
        pd = NoisyDict(x=x)
        for i in range(5):
            pd['y' + str(i)] = jn(i, x)

        # Create some line plots of some of the data
        plot = Plot(pd, title="Line Plot")
        plot.plot(('x', 'y0', 'y1', 'y2'), color='red')
        plot.plot(('x', 'y3'), color='blue')

        return plot


if __name__ == '__main__':
    demo = Demo()
    demo.configure_traits()
