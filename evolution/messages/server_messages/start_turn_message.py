from evolution.messages.message import *
from evo_json.serializers.player_state import *


class StartTurnServerMessage(PlayerState, Message):
    """ A Start Turn Sever Message """

    def __repr__(self) -> str:
        return name_of_class(self)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, StartTurnServerMessage)

    @staticmethod
    def make_from_watering_hole_player_configuration(food_on_watering_hole: Natural,
                                                     player_config: PlayerConfiguration) -> 'StartTurnServerMessage':
        """ Convert the given Player Configuration into a StartTurnServerMessage
        :param food_on_watering_hole: The food on the watering hole
        :param player_config: The Player Configuration that the StartTurnServerMessage will be constructed for
        :return: The resulting StartTurnServerMessage
        """
        player_state = PlayerState.make_from_watering_hole_player_configuration(food_on_watering_hole, player_config)
        return StartTurnServerMessage(player_state.food_on_watering_hole,
                                      player_state.food_bag,
                                      player_state.species_list,
                                      player_state.hand)

    @staticmethod
    def deserialize(py_json: PyJSON) -> 'StartTurnServerMessage':
        """ Deserialize the given value into a instance of this Serializer?
        :param py_json: A PyJSON value
        :return: An instance of this Deserialized
        """
        player_state = PlayerState.deserialize(py_json)
        return StartTurnServerMessage(player_state.food_on_watering_hole,
                                      player_state.food_bag,
                                      player_state.species_list,
                                      player_state.hand)
