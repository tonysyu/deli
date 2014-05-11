from skimage import data

from enable.api import Component, ComponentEditor
from traits.api import HasStrictTraits, Instance
from traitsui.api import UItem, View

from deli.plot import Plot
from deli.renderer.image_renderer import ImageRenderer
from deli.tools.pan_tool import PanTool
from deli.tools.zoom_tool import ZoomTool
from deli.utils.data_structures import NoisyDict


WIDTH = 900
HEIGHT = 500

class Demo(HasStrictTraits):
    plot = Instance(Component)

    traits_view = View(
        UItem('plot', editor=ComponentEditor(size=(WIDTH, HEIGHT))),
        resizable=True, title="Basic x-y plots"
    )

    def _plot_default(self):
        image = data.lena()
        pd = NoisyDict(image=image)

        plot = Plot(data=pd)
        height, width = image.shape[:2]
        plot.data_bbox.bounds = (0, 0, width, height)

        renderer = ImageRenderer(data=image, data_bbox=plot.data_bbox)
        plot.add(renderer)
        plot.renderers['image'] = [renderer]
        PanTool.attach_to(plot)
        ZoomTool.attach_to(plot)

        plot.data_bbox.bounds = (0, 0, 2*width, height)
        return plot


if __name__ == '__main__':
    demo = Demo()
    demo.configure_traits()
