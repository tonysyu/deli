from numpy import linspace
from scipy.special import jn

from deli.demo_utils import Window
from deli.plot_canvas import PlotCanvas
from deli.utils.data_structures import NoisyDict


class Demo(Window):

    def setup_canvas(self):
        x = linspace(-2.0, 10.0, 100)
        pd = NoisyDict(x=x)
        for i in range(5):
            pd['y' + str(i)] = jn(i, x)

        canvas = PlotCanvas(data=pd)
        canvas.title.text = "Line Plot"
        canvas.plot(('x', 'y0', 'y1', 'y2'), color='red')
        canvas.plot(('x', 'y3'), color='blue')
        return canvas


if __name__ == '__main__':
    demo = Demo()
    demo.configure_traits()
