from skimage import data

from enable.api import Component, ComponentEditor
from traits.api import HasStrictTraits, Instance
from traitsui.api import UItem, View

from deli.plot_canvas import PlotCanvas
from deli.renderer.image_renderer import ImageRenderer
from deli.tools.pan_tool import PanTool
from deli.tools.zoom_tool import ZoomTool
from deli.utils.data_structures import NoisyDict


WIDTH = 900
HEIGHT = 500

class Demo(HasStrictTraits):
    canvas = Instance(Component)

    traits_view = View(
        UItem('canvas', editor=ComponentEditor(size=(WIDTH, HEIGHT))),
        resizable=True, title="Basic x-y plots"
    )

    def _canvas_default(self):
        image = data.lena()
        pd = NoisyDict(image=image)

        canvas = PlotCanvas(data=pd)
        height, width = image.shape[:2]
        canvas.data_bbox.bounds = (0, 0, width, height)

        renderer = ImageRenderer(data=image, data_bbox=canvas.data_bbox)
        canvas.add(renderer)
        canvas.renderers['image'] = [renderer]
        PanTool.attach_to(canvas)
        ZoomTool.attach_to(canvas)

        canvas.data_bbox.bounds = (0, 0, 2*width, height)
        return canvas


if __name__ == '__main__':
    demo = Demo()
    demo.configure_traits()
