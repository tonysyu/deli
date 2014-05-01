from matplotlib.transforms import BboxTransform as BaseTransform


class BboxTransform(BaseTransform):
    """ Transform from one bounding box to another.

    This is a very thin wrapper around Matplotlib's `BboxTransform` to work
    with our custom `BoundingBox` class.
    """

    def __init__(self, bbox0, bbox1):
        super(BboxTransform, self).__init__(bbox0._bbox, bbox1._bbox)
