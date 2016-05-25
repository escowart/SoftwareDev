from evolution.messages.message import *


class OkayServerMessage(Response):
    """ An Okay Server Message """

    def serialize(self) -> PyJSON:
        """ Serialize this value into a its PyJSON equivalent?
        :return: The serialized JSON
        """
        return OKAY

    @staticmethod
    def can_deserialize(py_json: PyJSON) -> bool:
        """ Can this Serializers deserialize the given PyJSON value?
        :param py_json: A PyJSON value
        :return: True if this can deserialize the given value, False otherwise
        """
        return py_json == OKAY

    @staticmethod
    def deserialize(py_json: PyJSON) -> 'OkayServerMessage':
        """ Deserialize the given value into a instance of this Serializer?
        :param py_json: A PyJSON value
        :return: An instance of this Deserialized
        """
        return OkayServerMessage()

    def __repr__(self) -> str:
        return name_of_class(self)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, OkayServerMessage)