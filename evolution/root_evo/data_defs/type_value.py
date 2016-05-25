from evolution.root_evo.data_defs.data_defs import *
from evolution.root_evo.constants import *



def name_of_class(value: Any) -> str:
    """ Get the name of the class of the given value
    :param value: The value
    :return: The name of the class
    """
    return value.__class__.__name__


def remove_class_str(no_class_str: str) -> str:
    """ Remove the Class String from the given value
    :param no_class_str: The no class string being passed in
    :return: The resulting string without the class name
    """
    class_str_len = len(CLASS_STR)
    if (class_str_len <= len(no_class_str)) and (no_class_str[-class_str_len:] == CLASS_STR):
        return no_class_str[:-class_str_len]
    return no_class_str


class NoValue(object):
    """ A No Value class for constructing None values with specified names with the format
    class No<type>Class(NoValue):
        # doc-string: This iss the actual class value extending this NoValue
    No<type> = No<type>Class()

    Call '==' to check equality on the non-class No<type>
    """
    def __repr__(self) -> str:
        name = name_of_class(self)
        return remove_class_str(name)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__)


class NoStrClass(NoValue):
    """ The No String class """

NoStr = NoStrClass()

OptStr = Union[str, NoStrClass]


class NoTypeClass(object):
    """ The No Type class"""

NoType = NoTypeClass()

Type = Union[type, Tuple[type]]

OptType = Union[Type, NoTypeClass]


def has_is_instance_method(type_val: type):
    """ Does the given type have an is_instance method?
    :param type_val: A type
    :return: True if the given type has an is_instance method, False otherwise
    """
    return IS_INSTANCE_STR in dir(type_val)


class IsInstanceType(object):
    """ An interface for Types to define their own is_instance method """
    @staticmethod
    def is_instance(value: Any) -> bool:
        """ Is the given value an instance of this type?
        :param value: The value being checked
        :return: True if the given value is an instance of this class, False otherwise
        """