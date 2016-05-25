from evolution.messages.message import *


class NewPlayerServerMessage(Message):
    """ A New Player Server Message """

    def __init__(self, player_id: PlayerId) -> None:
        """ A class representing a New Player
        :param player_id: The id of the player
        """
        self._player_id = Unset        # type: PlayerId

        self.player_id = player_id

    @property
    def player_id(self) -> PlayerId:
        """ Get the Player's Id"""
        return assert_set(self._player_id)

    @player_id.setter
    def player_id(self, player_id: PlayerId) -> None:
        """ Set this player's id to player_id """
        assert_type(player_id, of_type=PlayerId, func_name="player_id")
        self._player_id = player_id

    def serialize(self) -> PyJSON:
        """ Serialize this value into a its PyJSON equivalent?
        :return: The serialized JSON
        """
        return self.player_id

    @staticmethod
    def can_deserialize(py_json: PyJSON) -> bool:
        """ Can this Serializers deserialize the given PyJSON value?
        :param py_json: A PyJSON value
        :return: True if this can deserialize the given value, False otherwise
        """
        return is_instance(py_json, int)

    @staticmethod
    def deserialize(py_json: PyJSON) -> 'NewPlayerServerMessage':
        """ Deserialize the given value into a instance of this Serializer?
        :param py_json: A PyJSON value
        :return: An instance of this Deserialized
        """
        return NewPlayerServerMessage(cast(PlayerId, py_json))

    def __repr__(self) -> str:
        return "{}(id={})".format(name_of_class(self), self.player_id)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, NewPlayerServerMessage) and \
               (self.player_id == cast(NewPlayerServerMessage, other).player_id)