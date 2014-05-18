from enable.enable_traits import bounds_trait, coordinate_trait
from traits.api import HasStrictTraits, Property


class CoordinateBox(HasStrictTraits):
    """
    Represents a box in screen space, and provides convenience properties to
    access bounds and coordinates in a variety of ways.

    Primary attributes (not properties):
        position : [x, y]
        bounds : [width, height]

    Secondary attributes (properties):
        x, y   : coordinates of the lower-left pixel of the box
        x2, y2 : coordinates of the upper-right pixel of the box
        width  : the number of horizontal pixels in the box; equal to x2-x+1
        height : the number of vertical pixels in the box; equal to y2-y+1

    Note that setting x and y will modify the position, but setting any of the
    other secondary attributes will modify the bounds of the box.
    """

    bounds = bounds_trait

    # The position relative to the container.  If container is None, then
    # position will be set to (0,0).
    position = coordinate_trait

    x = Property

    y = Property

    x2 = Property

    y2 = Property

    width = Property

    height = Property

    #------------------------------------------------------------------------
    # Property setters and getters
    #------------------------------------------------------------------------

    def _get_x(self):
        return self.position[0]

    def _set_x(self, val):
        self.position[0] = val

    def _get_y(self):
        return self.position[1]

    def _set_y(self, val):
        self.position[1] = val

    def _get_width(self):
        return self.bounds[0]

    def _set_width(self, val):

        if isinstance(val, basestring):
            try:
                val = float(val)
            except:
                pass

        old_value = self.bounds[0]
        self.bounds[0] = val
        self.trait_property_changed( 'width', old_value, val )

    def _get_height(self):
        return self.bounds[1]

    def _set_height(self, val):
        if isinstance(val, basestring):
            try:
                val = float(val)
            except:
                pass
        old_value = self.bounds[1]
        self.bounds[1] = val
        self.trait_property_changed( 'height', old_value, val )

    def _get_x2(self):
        if self.bounds[0] == 0: return self.position[0]
        return self.position[0] + self.bounds[0] - 1

    def _set_x2(self, val):
        self.position[0] = val - self.bounds[0] + 1

    def _get_y2(self):
        if self.bounds[1] == 0:
            return self.position[1]
        return self.position[1] + self.bounds[1] - 1

    def _set_y2(self, val):
        self.position[1] = val - self.bounds[1] + 1
