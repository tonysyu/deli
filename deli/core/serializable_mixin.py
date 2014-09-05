class SerializableMixin(object):

    def serialize(self):
        """Return serialized attributes for this class.
        """
        serialized_children = self._serialize_children()
        serialized_values = self.serialize_shallow()
        values = serialized_values[self.label]

        assert len(set(values).intersection(serialized_children)) == 0
        serialized_values[self.label].update(serialized_children)

        return serialized_values

    def serialize_shallow(self):
        """Return serialized attributes for this class, not including children.
        """
        return {self.label: {}}

    def _iter_children(self):
        """Yield child objects for serialization."""
        return ()

    def _serialize_children(self):
        attrs = {}
        for child in self._iter_children():
            assert child.label not in attrs
            attrs.update(child.serialize())
        return attrs
