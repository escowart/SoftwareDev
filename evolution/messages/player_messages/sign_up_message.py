from evolution.messages.message import *

OptSignUpMessage = Union['SignUpMessage', InvalidMessageClass]


class SignUpMessage(Message):
    """ A sign-up Player Message """
    def __init__(self, info: str=HELLO_WORLD_STR):
        """ Construct a SignUpMessage with the given info
        :param info: The info of the Player
        """
        self._info = Unset  # type: OptStr

        self.info = info

    def serialize(self) -> PyJSON:
        """ Serialize this value into a its PyJSON equivalent?
        :return: The serialized JSON
        """
        return self.info if self.info != NoStr else HELLO_WORLD_STR

    @staticmethod
    def can_deserialize(py_json: PyJSON) -> bool:
        """ Can this Serializers deserialize the given PyJSON value?
        :param py_json: A PyJSON value
        :return: True if this can deserialize the given value, False otherwise
        """
        return isinstance(py_json, str)

    @staticmethod
    def deserialize(py_json: PyJSON) -> 'SignUpMessage':
        """ Deserialize the given value into a instance of this Serializer?
        :param py_json: A PyJSON value
        :return: An instance of this Deserialized
        """
        return SignUpMessage(py_json)

    def __repr__(self) -> str:
        return "{}()".format(name_of_class(self))

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, SignUpMessage)

    @property
    def info(self) -> OptStr:
        """ Get the info of the Player """
        return assert_set(self._info)

    @info.setter
    def info(self, info: str) -> None:
        """ Set the info of the Player """
        assert_type(info, of_type=str, func_name="info")
        if info == HELLO_WORLD_STR:
            info = NoStr

        self._info = info