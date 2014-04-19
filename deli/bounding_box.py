import numpy as np
from matplotlib.transforms import Bbox

from traits.api import Event, HasStrictTraits, Instance, Property


__all__ = ['BoundingBox']


class Signal(object):
    """ Signal that calls all connected handlers when fired.

    This event signal is connected to `MPLBbox`, which is not a HasTraits
    class, and thus, cannot fire Traits events.
    """

    def __init__(self):
        self._handlers = []

    def connect(self, handler):
        self._handlers.append(handler)

    def fire(self, *args):
        for handler in self._handlers:
            handler(*args)


class MPLBbox(Bbox):
    """ Bounding box represented by two (x, y) pairs.

    Subclass Matplotlib's `Bbox` to fire an event when the bounds are changed.
    """

    def __init__(self, points):
        self.changed = Signal()
        super(MPLBbox, self).__init__(points)

    def invalidate(self):
        super(MPLBbox, self).invalidate()
        self.changed.fire()

    @classmethod
    def from_bounds(cls, x0, y0, width, height):
        """ Return bounding box from bounds given as (x0, y0, width, height).

        Override this since matplotlib returns `Bbox`, not subclass, instance.
        """
        return cls.from_extents(x0, y0, x0 + width, y0 + height)

    @classmethod
    def from_extents(cls, x0, y0, x1, y1):
        """ Return bounding box from extents given as (x0, y0, x1, y1).

        Override this since matplotlib returns `Bbox`, not subclass, instance.
        """
        points = np.array([[x0, y0],
                           [x1, y1]], dtype=np.float_)
        return cls(points)


def BboxProperty(attr_name, readonly=False):
    """ Property trait that accesses an attr on a BoundingBox's `_bbox` trait.

    Parameters
    ----------
    attr_name : str
        Name of attribute on `BoundingBox._bbox` (i.e. matplotlib's `Bbox`).
    readonly : bool
        If True, no setter is defined for this property.
    """

    def _bbox_getter(attr_name):
        def get_attr(self):
            return getattr(self._bbox, attr_name)
        return get_attr

    def _bbox_setter(attr_name):
        def set_attr(self, value):
            return setattr(self._bbox, attr_name, value)
        return set_attr

    if readonly:
        return Property(fget=_bbox_getter(attr_name))
    return Property(fget=_bbox_getter(attr_name),
                    fset=_bbox_setter(attr_name))


class BoundingBox(HasStrictTraits):
    """ Bounding box represented by two (x, y) pairs.

    This is a traits-wrapper around matplotlib's `Bbox`. Whenever the
    underlying bounding-box is changed, the `updated` event is fired.
    """

    _bbox = Instance(MPLBbox)

    updated = Event

    @classmethod
    def from_bounds(cls, x0, y0, width, height):
        return cls.from_mpl_bbox(MPLBbox.from_bounds(x0, y0, width, height))

    @classmethod
    def from_extents(cls, x0, y0, x1, y1):
        return cls.from_mpl_bbox(MPLBbox.from_extents(x0, y0, x1, y1))

    @classmethod
    def from_mpl_bbox(cls, bbox):
        instance = cls(_bbox=bbox)
        bbox.changed.connect(instance._bbox_updated)
        return instance

    def _bbox_updated(self):
        """Callback method for observer pattern."""
        self.updated = True

    #--------------------------------------------------------------------------
    #  Bounds Accessors
    #--------------------------------------------------------------------------

    x0 = BboxProperty('x0')

    x1 = BboxProperty('x1')

    y0 = BboxProperty('y0')

    y1 = BboxProperty('y1')

    x_limits = BboxProperty('intervalx')

    y_limits = BboxProperty('intervaly')

    bounds = BboxProperty('bounds')

    width = BboxProperty('width', readonly=True)

    height = BboxProperty('height', readonly=True)
