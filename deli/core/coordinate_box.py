from enable.enable_traits import bounds_trait, coordinate_trait
from traits.api import Enum, HasStrictTraits, Instance, Property, Tuple

from ..layout.ab_constrainable import ABConstrainable
from ..layout.constraints_namespace import ConstraintsNamespace
from ..layout.utils import add_symbolic_constraints, STRENGTHS


ConstraintPolicyEnum = Enum('ignore', *STRENGTHS)


def get_from_constraints_namespace(self, name):
    """ Property getter for all attributes that come from the constraints
    namespace.

    """
    return getattr(self._constraints_vars, name)


class CoordinateBox(HasStrictTraits):
    """
    Represents a box in screen space, and provides convenience properties to
    access bounds and coordinates in a variety of ways.

    Primary attributes (not properties):
        origin : [x, y]
        size : [width, height]

    Secondary attributes (properties):
        x, y   : coordinates of the lower-left pixel of the box
        width  : the number of horizontal pixels in the box; equal to x2-x+1
        height : the number of vertical pixels in the box; equal to y2-y+1

    Note that setting x and y will modify the origin, but setting any of the
    other secondary attributes will modify the size of the box.
    """

    size = bounds_trait

    # The origin relative to the container.  If container is None, then
    # origin will be set to (0,0).
    origin = coordinate_trait

    x = Property

    y = Property

    width = Property

    height = Property

    rect = Property

    # -----------------------------------------------------------------------
    # Constraints-based layout
    # -----------------------------------------------------------------------

    # A read-only symbolic object that represents the left boundary of
    # the component
    left = Property(fget=get_from_constraints_namespace)

    # A read-only symbolic object that represents the right boundary
    # of the component
    right = Property(fget=get_from_constraints_namespace)

    # A read-only symbolic object that represents the bottom boundary
    # of the component
    bottom = Property(fget=get_from_constraints_namespace)

    # A read-only symbolic object that represents the top boundary of
    # the component
    top = Property(fget=get_from_constraints_namespace)

    # A read-only symbolic object that represents the width of the
    # component
    layout_width = Property(fget=get_from_constraints_namespace)

    # A read-only symbolic object that represents the height of the
    # component
    layout_height = Property(fget=get_from_constraints_namespace)

    # A read-only symbolic object that represents the vertical center
    # of the component
    v_center = Property(fget=get_from_constraints_namespace)

    # A read-only symbolic object that represents the horizontal
    # center of the component
    h_center = Property(fget=get_from_constraints_namespace)

    # A size hint for the layout
    layout_size_hint = Tuple(0.0, 0.0)

    # How strongly a layout box hugs it's width hint.
    hug_width = ConstraintPolicyEnum('weak')

    # How strongly a layout box hugs it's height hint.
    hug_height = ConstraintPolicyEnum('weak')

    # How strongly a layout box resists clipping its contents.
    resist_width = ConstraintPolicyEnum('strong')

    # How strongly a layout box resists clipping its contents.
    resist_height = ConstraintPolicyEnum('strong')

    # A namespace containing the constraints for this CoordinateBox
    _constraints_vars = Instance(ConstraintsNamespace)

    # The list of hard constraints which must be applied to the object.
    _hard_constraints = Property

    # The list of size constraints to apply to the object.
    _size_constraints = Property

    # -----------------------------------------------------------------------
    # Property setters and getters
    # -----------------------------------------------------------------------

    def _get_x(self):
        return self.origin[0]

    def _set_x(self, val):
        self.origin[0] = val

    def _get_y(self):
        return self.origin[1]

    def _set_y(self, val):
        self.origin[1] = val

    def _get_width(self):
        return self.size[0]

    def _set_width(self, val):
        old_value = self.size[0]
        self.size[0] = val
        self.trait_property_changed('width', old_value, val)

    def _get_height(self):
        return self.size[1]

    def _set_height(self, val):
        old_value = self.size[1]
        self.size[1] = val
        self.trait_property_changed('height', old_value, val)

    def _get_rect(self):
        return self.origin + self.size

    def __constraints_vars_default(self):
        obj_name = self.id if hasattr(self, 'id') else ''
        cns_names = ConstraintsNamespace(type(self).__name__, obj_name)
        add_symbolic_constraints(cns_names)
        return cns_names

    def _get__hard_constraints(self):
        """ Generate the constraints which must always be applied.
        """
        left = self.left
        bottom = self.bottom
        width = self.layout_width
        height = self.layout_height
        cns = [left >= 0, bottom >= 0, width >= 0, height >= 0]
        return cns

    def _get__size_constraints(self):
        """ Creates the list of size hint constraints for this box.
        """
        cns = []
        push = cns.append
        width_hint, height_hint = self.layout_size_hint
        width = self.layout_width
        height = self.layout_height
        hug_width, hug_height = self.hug_width, self.hug_height
        resist_width, resist_height = self.resist_width, self.resist_height
        if width_hint >= 0:
            if hug_width != 'ignore':
                cn = (width == width_hint) | hug_width
                push(cn)
            if resist_width != 'ignore':
                cn = (width >= width_hint) | resist_width
                push(cn)
        if height_hint >= 0:
            if hug_height != 'ignore':
                cn = (height == height_hint) | hug_height
                push(cn)
            if resist_height != 'ignore':
                cn = (height >= height_hint) | resist_height
                push(cn)

        return cns


# Register with ABConstrainable so that layout helpers will recognize
# CoordinateBox instances.
ABConstrainable.register(CoordinateBox)
