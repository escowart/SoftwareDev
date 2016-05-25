from evolution.root_evo.data_defs.type_value import *

OptNatural = Union['NoNaturalClass', 'Natural']


def is_opt_natural(value: Any) -> bool:
    """ Is the given value an OptNatural?
    :param value: The value being checked
    :return: True if value is an OptNatural, False otherwise
    """
    return (value == NoNatural) or is_natural(value)


class NoNaturalClass(NoValue):
    """ The No-Natural class """

NoNatural = NoNaturalClass()


class Natural(int):
    """ A Natural Number """

    @staticmethod
    def is_instance(value):
        """ Is the given value a Natural?"""
        return is_natural(value)


def is_natural(value: Any) -> bool:
    """ Is the given value a Natural?
    :param value: Any value
    :return: True if the value is a Natural, False otherwise
    """
    return isinstance(value, int) and (0 <= value)


"""-----------NaturalPlus-----------"""

class NaturalPlus(Natural):
    """ A Natural Plus Number """
    @staticmethod
    def is_instance( value):
        """ Is the given value a Natural?"""
        return is_natural_plus(value)


# A NaturalPlus is a Natural >= 1


def is_natural_plus(value: Any) -> bool:
    """ Is the given value a natural plus
    :param value: The value being checked
    :return: True if the value is a natural plus, False otherwise
    """
    return isinstance(value, int) and (1 <= value)


