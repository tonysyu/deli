import numpy as np

from traits.api import HasStrictTraits, Instance
from traitsui.api import Item, View

from deli.core.component_editor import ComponentEditor
from deli.core.constraints_container import ConstraintsContainer
from deli.layout.api import align, vbox
from deli.plot_canvas import PlotCanvas
from deli.plots.line_plot import LinePlot
from deli.plots.scatter_plot import ScatterPlot


class Demo(HasStrictTraits):

    figure = Instance(ConstraintsContainer)
    line_canvas = Instance(PlotCanvas)
    scatter_canvas = Instance(PlotCanvas)

    traits_view = View(
        Item('figure',
             editor=ComponentEditor(),
             show_label=False,
        ),
        resizable=True,
        title="Subplots using constraints container",
        width=500, height=500,
    )

    def _figure_default(self):
        figure = ConstraintsContainer(bounds=(500,500), padding=50)

        figure.add(self.line_canvas, self.scatter_canvas)
        figure.layout_constraints = [
            vbox(self.line_canvas, self.scatter_canvas),
            align('layout_height', self.line_canvas, self.scatter_canvas),
        ]
        return figure

    def _line_canvas_default(self):
        canvas = PlotCanvas()
        canvas.title.text = "Line Plot"

        x = np.linspace(0, 10.0, 100)
        plot = LinePlot(x_data=x, y_data=np.sin(x))
        canvas.add(plot)
        return canvas

    def _scatter_canvas_default(self):
        canvas = PlotCanvas()
        canvas.title.text = "Scatter Plot"

        x = np.linspace(0, 10.0, 100)
        plot = ScatterPlot(x_data=x, y_data=np.sin(x))
        canvas.add(plot)
        return canvas


if __name__ == "__main__":
    demo = Demo()
    demo.configure_traits()
