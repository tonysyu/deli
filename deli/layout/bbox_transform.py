from matplotlib.transforms import ( # noqa
    blended_transform_factory, IdentityTransform,
    Transform as BaseTransform,
    BboxTransform as _MPLBboxTransform,
)


class BboxTransform(_MPLBboxTransform):
    """ Transform from one bounding box to another.

    This is a very thin wrapper around Matplotlib's `BboxTransform` to work
    with our custom `BoundingBox` class.
    """

    def __init__(self, bbox0, bbox1):
        super(BboxTransform, self).__init__(bbox0._bbox, bbox1._bbox)


def blend_xy_transforms(x_transform, y_transform):
    return blended_transform_factory(x_transform, y_transform)
