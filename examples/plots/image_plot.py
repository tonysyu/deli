from skimage import data

from deli.demo_utils import Window
from deli.plot_canvas import PlotCanvas
from deli.renderer.image_renderer import ImageRenderer
from deli.utils.data_structures import NoisyDict


class Demo(Window):

    def setup_canvas(self):
        image = data.lena()
        pd = NoisyDict(image=image)

        canvas = PlotCanvas(data=pd)
        height, width = image.shape[:2]
        canvas.data_bbox.bounds = (0, 0, width, height)

        renderer = ImageRenderer(data=image, data_bbox=canvas.data_bbox)
        canvas.add(renderer)
        return canvas


if __name__ == '__main__':
    demo = Demo()
    demo.configure_traits()
