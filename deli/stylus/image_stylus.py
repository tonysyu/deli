import numpy as np

from kiva.agg import GraphicsContextArray
from traits.api import Bool, HasStrictTraits, Instance


KIVA_DEPTH_MAP = {3: "rgb24", 4: "rgba32"}


def kiva_array_from_numpy_array(data):
    if data.shape[2] not in KIVA_DEPTH_MAP:
        msg = "Unknown colormap depth value: {}"
        raise RuntimeError(msg.format(data.shape[2]))
    kiva_depth = KIVA_DEPTH_MAP[data.shape[2]]

    # Data presented to the GraphicsContextArray needs to be contiguous.
    data = np.ascontiguousarray(data)
    return GraphicsContextArray(data, pix_format=kiva_depth)


class ImageStylus(HasStrictTraits):

    _cached_image = Instance(GraphicsContextArray)
    _cache_valid = Bool(False)

    def draw(self, gc, image, rect):
        if not self._cache_valid:
            self._compute_cached_image(image)
        x, y, width, height = rect

        if width <= 0 or height <= 0:
            return

        with gc:
            gc.draw_image(self._cached_image, rect)

    def _compute_cached_image(self, data):
        self._cached_image = kiva_array_from_numpy_array(data)
        self._cache_valid = True
