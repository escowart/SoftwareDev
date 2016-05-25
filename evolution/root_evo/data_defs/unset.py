from typing import TypeVar, Union, Any, Tuple


class UnsetClass(object):
    """ A class representing an UnSet Value """
    def __repr__(self) -> str:
        return "Unset"

    def __eq__(self, other):
        return isinstance(other, UnsetClass)

Unset = UnsetClass()


class UnsetValueError(ValueError):
    def __init__(self, *args, **kwargs) -> None:
        ValueError.__init__(self, *args, **kwargs)

A = TypeVar('A')

def assert_set(value: A) -> A:
    """ Assert the given vale is set, Raises an UnsetValueError if nset
    :param value: The value
    :return: The value if set
    :raises: UnsetValue if unset
    """
    if value == Unset:
        raise UnsetValueError()

    return value

