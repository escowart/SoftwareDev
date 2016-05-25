from functools import total_ordering
from evolution.root_evo.data_defs.index import *

V = TypeVar('V')


class OptOrderedKey(Generic[V]):
    """ An OptOrderedKey is one of:
        - NoOrderedKey
        - OrderedKey[V]
    """


class NoOrderedKeyClass(OptOrderedKey):
    """ A No-OrderingKey """

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, NoOrderedKeyClass)

NoOrderedKey = NoOrderedKeyClass()


@total_ordering
class OrderedKey(OptOrderedKey[V]):
    """ A class representing a Pick Key which has a __gt__ and __eq__ for ordering
    """

    @abstractmethod
    def __gt__(self, other: V) -> bool:
        """ Is this OrderingKey greater to the given OrderingKey? """
        raise NotImplementedError("__gt__")

    @abstractmethod
    def __eq__(self, other: V) -> bool:
        """ Is this OrderingKey equal to the given OrderingKey? """
        raise NotImplementedError("__gt__")


class PseudoOrderedKey(OrderedKey):
    """ A Pseudo Ordered Key which is always less than everything """

    def __init__(self, value: Any) -> None:
        """ Does nothing """
        pass

    def __gt__(self, other: V) -> bool:
        """ Is this OrderingKey greater to the given OrderingKey? """
        return False

    def __eq__(self, other: V) -> bool:
        """ Is this OrderingKey equal to the given OrderingKey? """
        return False

