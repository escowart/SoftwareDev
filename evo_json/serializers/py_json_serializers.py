from evolution.all_interfaces import *


def serialize_list(serializer_list: List['Serializer']) -> List[PyJSON]:
    """ Serialize the given list of serializers,
    :param serializer_list: The list of serializers
    :return: The resulting Serialization
    """
    return [serializer.serialize() for serializer in serializer_list]


S = TypeVar('Serializer')


def can_deserialize_list(serializer_type: type(S), py_json: List[PyJSON]) -> bool:
    """ Can the given Serializer type deserialize the given PyJSON if it is a list
    :param serializer_type: The type of serializers
    :param py_json: The py_json trying to be deserailized
    :return: True if the PyJSON can be deserialize, false otherwise
    """
    return is_list(py_json) and all(serializer_type.can_deserialize(elem) for elem in py_json)


def deserialize_list(serializer_type: type(S), py_json: List[PyJSON]) -> List[S]:
    """ Deserialize the given PyJSON list using the given serialize type
    :param serializer_type: The type of serializers
    :param py_json: The py_json trying to be deserialized
    :return: The instances of the given serializer
    """
    return [serializer_type.deserialize(elem) for elem in py_json]


class Serializer(object, metaclass=ABCMeta):
    """ A Protocol Serializer """

    @abstractmethod
    def serialize(self) -> PyJSON:
        """ Serialize this value into a its PyJSON equivalent?
        :return: The serialized JSON
        """
        raise NotImplementedError("serialize")

    @staticmethod
    @abstractmethod
    def can_deserialize(py_json: PyJSON) -> bool:
        """ Can this Serializers deserialize the given PyJSON value?
        :param py_json: A PyJSON value
        :return: True if this can deserialize the given value, False otherwise
        """
        raise NotImplementedError("can_deserialize")

    @staticmethod
    @abstractmethod
    def deserialize(py_json: PyJSON) -> 'Serializer':
        """ Deserialize the given value into a instance of this Serializer?
        :param py_json: A PyJSON value
        :return: An instance of this Deserialized
        """
        raise NotImplementedError("deserialize")