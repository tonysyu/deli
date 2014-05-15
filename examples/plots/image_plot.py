from skimage import data

from deli.demo_utils import Window
from deli.plot_canvas import PlotCanvas
from deli.renderer.image_renderer import ImageRenderer


class Demo(Window):

    def setup_canvas(self):
        canvas = PlotCanvas()
        renderer = ImageRenderer(data=data.lena())
        canvas.add(renderer)
        return canvas


if __name__ == '__main__':
    demo = Demo()
    demo.configure_traits()
