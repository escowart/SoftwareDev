from evo_json.serializers.py_json_serializers import *
from evolution.species.all_species import *


class Message(Serializer, metaclass=ABCMeta):
    """ A Message over the wire which is a Serializer"""


class InvalidMessageClass(NoValue):
    """ The Invalid Message class """

InvalidMessage = InvalidMessageClass()

OptMessage = Union[Message, InvalidMessageClass]


class Response(Message, metaclass=ABCMeta):
    """ Response over a wire which is a Serializer """

OptResponse = Union[Response, InvalidMessageClass]


class ValidNoResponseClass(Response, NoValue):
    """ A No Response for when message are sent to an external player that require not response """

    def serialize(self) -> PyJSON:
        """ Serialize this value into a its PyJSON equivalent?
        :return: The serialized JSON
        """
        return PYJSON_NULL

    @staticmethod
    def can_deserialize(py_json: PyJSON) -> bool:
        """ Can this Serializers deserialize the given PyJSON value?
        :param py_json: A PyJSON value
        :return: True if this can deserialize the given value, False otherwise
        """
        return True

    @staticmethod
    def deserialize(py_json: PyJSON) -> 'ValidNoResponseClass':
        """ Deserialize the given value into a instance of this Serializer?
        :param py_json: A PyJSON value
        :return: An instance of this Deserialized
        """
        return ValidNoResponse


ValidNoResponse = ValidNoResponseClass()