from deli.serialization.manager import SerializationManager
from deli.serialization.default_adapter import DefaultAdapter


class A(object):
    pass


class B(object):
    pass


def test_register():
    manager = SerializationManager()
    assert not manager.is_serializable(A())

    manager.register(DefaultAdapter, A)
    assert manager.is_serializable(A())


def test_copy():
    manager = SerializationManager()
    manager.register(DefaultAdapter, A)

    # A copy of the SerializationManager should be able to adapt `A` too.
    copied = manager.copy()
    assert copied.is_serializable(A())

    # Registering `B` to `copied` allows it (but not `manager`) to adapt `B`.
    copied.register(DefaultAdapter, B)
    assert copied.is_serializable(B())
    assert not manager.is_serializable(B())
