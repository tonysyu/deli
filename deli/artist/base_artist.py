from traits.api import HasStrictTraits, Property

from ..core.serializable_mixin import SerializableMixin


class BaseArtist(HasStrictTraits, SerializableMixin):

    label = Property

    def _get_label(self):
        return self.__class__.__name__
