import typing
from evolution.root_evo.collections.list_interface import *


def is_instance(value: Any, of_type: Type):
    """ Is the given value an instance of the given type of Tuple of types?
    :param value: The value being check
    :param of_type: The type of Tuple of Types being check against
    :return: True if the value is of the given type, False otherwise
    """
    if of_type == NoType:
        return False
    elif isinstance(of_type, tuple):
        return any(is_instance(value, type_val) for type_val in of_type)
    elif has_is_instance_method(of_type):
        return cast(IsInstanceType, of_type).is_instance(value)
    else:
        return isinstance(value, of_type)


def is_collection(value:           Any,
                  collection_type: CollectionType,
                  of_type:         OptType = NoType,
                  min_len:         OptNatural = NoNatural,
                  length:          OptNatural = NoNatural,
                  max_len:         OptNatural = NoNatural) -> bool:
    """ Is the given value a List
    :param value: The value being checked
    :param collection_type: The type of collection
    :param of_type: The Type requirement of each element
    :param min_len: The minimum allowed length
    :param length: The length
    :param max_len: The maximum allowed length
    :return: True if all conditions are met, False otherwise
    """
    if of_type == CollectionType:
        return False

    return (is_instance(value, collection_type) and
            ((of_type == NoType)    or all(is_instance(item, of_type) for item in value)) and
            ((min_len == NoNatural) or (min_len <= len(value))) and
            ((length  == NoNatural) or (length  == len(value))) and
            ((max_len == NoNatural) or (max_len >= len(value))))


def is_list(value: Any,
            of_type: OptType = NoType,
            min_len: OptNatural = NoNatural,
            length:  OptNatural  = NoNatural,
            max_len: OptNatural = NoNatural) -> bool:
    """ Is the given value a List
    :param value: The value being checked
    :param of_type: The Type requirement of each element
    :param min_len: The minimum allowed length
    :param length: The length
    :param max_len: The maximum allowed length
    :return: True if all conditions are met, False otherwise
    """
    return is_collection(value, list, of_type, min_len, length, max_len)


class SetValueError(ValueError):
    def __init__(self, *args, **kwargs) -> None:
        ValueError.__init__(self, *args, **kwargs)


class AssertTypeError(ValueError):
    def __init__(self, *args, **kwargs) -> None:
        ValueError.__init__(self, *args, **kwargs)


def assert_type(value:           Any,
                collection_type: OptCollectionType = NoType,
                of_type:         OptType = NoType,
                func_name:       OptStr = NoStr,
                exception_msg:   OptStr = NoStr,
                min_value:       Any = NoOrderedKey,
                max_value:       Any = NoOrderedKey,
                coll_min_len:    OptNatural = NoNatural,
                coll_len:        OptNatural = NoNatural,
                coll_max_len:    OptNatural = NoNatural) -> None:
    """ Assert that the given value is of the given types or type Tuple with the given exception message
    :param value: The value
    :param collection_type: The collection type
    :param of_type: The types that it could be
    :param func_name: The name of the function or method raising the exception
    :param exception_msg: The exception's message
    :param min_value: The minimum value
    :param max_value: The maximum value
    :param coll_min_len: The minimum allowed length
    :param coll_len: The length
    :param coll_max_len: The maximum allowed length
    :raises: SetValueError if not of the types
    """
    error_msg = assert_type_error_message(value, collection_type, of_type, func_name, min_value, max_value,
                                          exception_msg, coll_min_len, coll_len, coll_max_len)

    if ((collection_type == NoType) and
            is_instance(value, of_type) and
            ((min_value == NoOrderedKey) or (min_value <= value)) and
            ((max_value == NoOrderedKey) or (value <= max_value))) or \
            ((collection_type != NoType) and is_collection(value,
                                                           collection_type,
                                                           of_type,
                                                           coll_min_len,
                                                           coll_len,
                                                           coll_max_len)):
        return
    else:
        raise AssertTypeError(error_msg)


def str_of_type(type_val: Type) -> str:
    """ Convert the Collection Type to a String
    :param type_val: The type's value
    """
    if type_val == list:
        return LIST_STR
    elif type_val == tuple:
        return TUPLE_STR
    elif NAME_STR in dir(type_val):
        return type_val.__name__
    else:
        return str(type_val)


def assert_type_error_message(value:         Any,
                              collection:    OptCollectionType = NoType,
                              of_type:       OptType = NoType,
                              func_name:     OptStr = NoStr,
                              exception_msg: OptStr = NoStr,
                              min_value:     Any = NoOrderedKey,
                              max_value:     Any = NoOrderedKey,
                              coll_min_len:  OptNatural = NoNatural,
                              coll_len:      OptNatural = NoNatural,
                              coll_max_len:  OptNatural = NoNatural) -> str:
    """ Assert that the given value is of the given types or type Tuple with the given exception message
    :param value: The value
    :param collection: The collection type
    :param of_type: The types that it could be
    :param func_name: The name of the function or method raising the exception
    :param exception_msg: The exception's message
    :param min_value: The minimum value
    :param max_value: The maximum value
    :param coll_min_len: The minimum allowed length
    :param coll_len: The length
    :param coll_max_len: The maximum allowed length
    :return: The exception message
    """
    if exception_msg == NoStr:
        exception_msg = "" if func_name == NoStr else (str(func_name) + ":")

        if collection == NoType:
            exception_msg += " Must be {}".format(str_of_type(of_type))
            exception_msg += "" if min_value == NoOrderedKey else ", of value >= {}".format(min_value)
            exception_msg += "" if max_value == NoOrderedKey else ", of value <= {}".format(max_value)
        else:
            exception_msg += " Must be {}[{}]".format(str_of_type(collection), str_of_type(of_type))
            exception_msg += "" if coll_min_len == NoNatural else ", of min length: {}".format(coll_min_len)
            exception_msg += "" if coll_min_len == NoNatural else ", of length: {}".format(coll_len)
            exception_msg += "" if coll_min_len == NoNatural else ", of max length: {}".format(coll_max_len)

        exception_msg += ", got: {}".format(value)

    return exception_msg


class List(typing.List[Item], IList):
    """ Extension of the typing.List to be considered an OptList """


def eq_comparator(value_x, value_y):
    return value_x == value_y


def is_comparator(value_x, value_y):
    return value_x is value_y


def type_comparator(type_x, type_y):
    return type(type_x) is type(type_y)


def of_type_comparator(value_x, type_y):
    return type(value_x) is type_y


def any_duplicates(list_a: List[Any], equality_comparator: Callable[[Any, Any], bool] = eq_comparator):
    """ Are their any duplicates in the given list where they equal according to the comparator
    :param list_a: The list being checked for duplicates
    :param equality_comparator: The equality comparator which determines duplicates
    :return: True if any duplicates were found, False otherwise
    """
    return any(any(equality_comparator(elem, list_a[j])
                   for j in range(i + 1, len(list_a)))
               for i, elem in enumerate(list_a))


def does_list_contain(list_a: List[Any], value: Any, equality_comparator: Callable[[Any, Any], bool] = eq_comparator):
    """ Does the given list contain the given value according to the comparator
    :param list_a: The list being checked
    :param value: The value being checked
    :param equality_comparator: The equality comparator
    :return: True if the list does contain, False otherwise
    """
    return any(equality_comparator(t_elem, value) for t_elem in list_a)
