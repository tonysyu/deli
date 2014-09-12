from enable.api import ColorTrait
from traits.api import HasStrictTraits

from ..style import config


class BasePatchStylus(HasStrictTraits):
    """ A base object for styluses that draw polygons.
    """

    fill_color = ColorTrait(config.get('polygon.fill_color'))
    edge_color = ColorTrait(config.get('polygon.edge_color'))
