from evolution.messages.message import *
from evo_json.serializers.game_state import *


class ChooseFeedingServerMessage(GameState, Message):
    """ A Choose Feeding Sever Message """

    def __repr__(self) -> str:
        return name_of_class(self)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, ChooseFeedingServerMessage)

    @staticmethod
    def make_from_player_configs_and_watering_hole(player_config:         PlayerConfiguration,
                                                   food_on_watering_hole: Natural,
                                                   other_players:         List[PlayerConfiguration]) \
            -> 'ChooseFeedingServerMessage':
        """ Make a Game State from the given arguments
        :param player_config: The Player Configuration that the PlayerState will be constructed for
        :param food_on_watering_hole: The food on the watering hole
        :param other_players: The other players in the game
        :return: The resulting Game State
        """
        game_state = GameState.make_from_player_configs_and_watering_hole(player_config,
                                                                          food_on_watering_hole,
                                                                          other_players)
        return ChooseFeedingServerMessage(game_state.food_bag,
                                          game_state.species_list,
                                          game_state.hand,
                                          game_state.food_on_watering_hole,
                                          game_state.other_player_boards)

    @staticmethod
    def deserialize(py_json: PyJSON) -> 'ChooseFeedingServerMessage':
        """ Deserialize the given value into a instance of this Serializer?
        :param py_json: A PyJSON value
        :return: An instance of this Deserialized
        """
        game_state = GameState.deserialize(py_json)
        return ChooseFeedingServerMessage(game_state.food_bag,
                                          game_state.species_list,
                                          game_state.hand,
                                          game_state.food_on_watering_hole,
                                          game_state.other_player_boards)

    def __repr__(self) -> str:
        return "{}(food_bag={}, species_list={}, hand={}, " \
               "food_on_watering_hole={}, other_player_boards={})" \
            .format(name_of_class(self), self.food_bag, self.species_list, self.hand, self.food_on_watering_hole, self.other_player_boards)

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, ChooseFeedingServerMessage) and
                (self.food_bag == cast(ChooseFeedingServerMessage, other).food_bag) and
                (self.species_list == cast(ChooseFeedingServerMessage, other).species_list) and
                (self.hand == cast(ChooseFeedingServerMessage, other).hand) and
                (self.food_on_watering_hole == cast(ChooseFeedingServerMessage, other).food_on_watering_hole) and
                (self.other_player_boards == cast(ChooseFeedingServerMessage, other).other_player_boards))
