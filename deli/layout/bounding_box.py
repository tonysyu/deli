import numpy as np
from matplotlib.transforms import Bbox

from traits.api import Event, HasStrictTraits, Instance, Property


__all__ = ['BoundingBox']


def calc_bounds(x, current_bounds):
    x_min, x_max = current_bounds
    x_lo = min(np.min(x), x_min)
    x_hi = max(np.max(x), x_max)
    if x_lo < x_min or x_hi > x_max:
        return (x_lo, x_hi)
    else:
        return None


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
    def from_rect(cls, rect):
        """ Return bounding box from rect given as (x0, y0, width, height).

        Override this since matplotlib returns `Bbox`, not subclass, instance.
        """
        x0, y0, width, height = rect
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
    def from_rect(cls, rect):
        return cls.from_mpl_bbox(MPLBbox.from_rect(rect))

    @classmethod
    def from_size(cls, size):
        rect = [0, 0] + list(size)
        return cls.from_mpl_bbox(MPLBbox.from_rect(rect))

    @classmethod
    def from_extents(cls, x0, y0, x1, y1):
        return cls.from_mpl_bbox(MPLBbox.from_extents(x0, y0, x1, y1))

    @classmethod
    def from_mpl_bbox(cls, bbox):
        instance = cls(_bbox=bbox)
        bbox.changed.connect(instance._bbox_updated)
        return instance

    def copy(self):
        return self.__class__.from_rect(self.rect)

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

    rect = BboxProperty('bounds')

    width = BboxProperty('width', readonly=True)

    height = BboxProperty('height', readonly=True)

    size = Property

    def update_from_x_data(self, x_data):
        x_span = calc_bounds(x_data, self.x_limits)
        if x_span is not None:
            self.x_limits = x_span

    def update_from_y_data(self, y_data):
        y_span = calc_bounds(y_data, self.y_limits)
        if y_span is not None:
            self.y_limits = y_span

    def update_from_extents(self, x_min, y_min, x_max, y_max):
        x0 = min(x_min, self.x_limits[0])
        x1 = max(x_max, self.x_limits[1])
        y0 = min(y_min, self.y_limits[0])
        y1 = max(y_max, self.y_limits[1])
        self.rect = (x0, y0, x1 - x0, y1 - y0)

    def _get_size(self):
        return (self.width, self.height)

    def _set_size(self, size):
        self.rect = (self.x0, self.y0) + tuple(size)
