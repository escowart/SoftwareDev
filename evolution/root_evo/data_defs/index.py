from evolution.root_evo.data_defs.natural import *

OptIndex = Union['NoIndexClass', 'Index']


def is_opt_index(value: Any) -> bool:
    """ Is the given value an OptIndex?
    :param value: The value being checked
    :return: True if value is an OptIndex, False otherwise
    """
    return (value == NoIndex) or is_index(value)


class NoIndexClass(NoValue):
    """ The No Index class"""

NoIndex = NoIndexClass()


class Index(Natural):
    """ A class representing an Index """
    @staticmethod
    def is_instance(value):
        return is_index(value)

is_index = is_natural
