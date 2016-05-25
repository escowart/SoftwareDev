from evo_json.serializers.player_state import *


class GameState(PlayerState):
    """ A class representing a Game State in the Remote Protocol """

    def __init__(self,
                 food_bag:              Natural,
                 species_list:          List[Species],
                 hand:                  List[TraitCard],
                 food_on_watering_hole: Natural,
                 other_player_boards:   List[SpeciesBoards]) -> None:
        """ Construct a Game State
        :param food_bag: The food bag of the Player
        :param species_list: The Species list of the Player
        :param hand: The hand of the Player
        :param food_on_watering_hole: The food on the watering hole of the game
        :param other_player_boards: The other players in the game
        """
        PlayerState.__init__(self, food_on_watering_hole, food_bag, species_list, hand)
        self._other_player_boards = Unset     # type: List[SpeciesBoards]

        self.other_player_boards = other_player_boards

    def serialize(self) -> PyJSON:
        """ Serialize this value into a its PyJSON equivalent?
        :return: The serialized JSON
        """
        return [self.food_bag,
                SpeciesBoards(self.species_list).serialize(),
                convert_to_pj_loc(self.hand),
                self.food_on_watering_hole,
                serialize_list(self.other_player_boards)]

    @staticmethod
    def can_deserialize(py_json: PyJSON) -> bool:
        """ Can this Serializers deserialize the given PyJSON value?
        :param py_json: The PyJSON
        :return: True if this can deserialize the given value, False otherwise
        """
        if (is_list(py_json, length=PJ_GAME_STATE_LEN) and
                is_natural(py_json[0]) and
                SpeciesBoards.can_deserialize(py_json[1]) and
                is_natural(py_json[3]) and
                all(SpeciesBoards.can_deserialize(other_player_board) for other_player_board in py_json[4])):
            try:
                [convert_from_pj_species_card(card) for card in py_json[2]]
                return True
            except ValueError:
                return False
        return False

    @staticmethod
    def deserialize(py_json: PyJSON) -> 'GameState':
        """ Deserialize the given value into a instance of this Serializer?
        :param py_json: A PyJSON value
        :return: An instance of this Deserialized
        """
        return GameState(py_json[0],
                         SpeciesBoards.deserialize(py_json[1]).species_list,
                         convert_from_pj_loc(py_json[2]),
                         py_json[3],
                         deserialize_list(SpeciesBoards, py_json[4]))

    @property
    def other_player_boards(self) -> List[SpeciesBoards]:
        """ Get the list of other player Species Boards """
        return assert_set(self._other_player_boards)

    @other_player_boards.setter
    def other_player_boards(self, other_player_boards: List[SpeciesBoards]) -> None:
        """ Set the list of other player Species Boards """
        assert_type(other_player_boards, list, of_type=SpeciesBoards, func_name="other_player_boards")
        self._other_player_boards = other_player_boards

    @property
    def other_player_configs(self) -> List[PlayerConfiguration]:
        """ Get the list of other player Configurations """
        return [boards.to_player_configuration() for boards in self.other_player_boards]

    @other_player_configs.setter
    def other_player_configs(self, other_player_configs: List[PlayerConfiguration]) -> None:
        """ Set the list of other player Configurations """
        assert_type(other_player_configs, list, of_type=PlayerConfiguration, func_name="other_player_configs")
        self._other_player_boards = other_player_configs

    @staticmethod
    def make_from_player_configs_and_watering_hole(player_config:         PlayerConfiguration,
                                                   food_on_watering_hole: Natural,
                                                   other_players:         List[PlayerConfiguration]) -> 'GameState':
        """ Make a Game State from the given arguments
        :param player_config: The Player Configuration that the PlayerState will be constructed for
        :param food_on_watering_hole: The food on the watering hole
        :param other_players: The other players in the game
        :return: The resulting Game State
        """
        player_state = PlayerState.make_from_watering_hole_player_configuration(NO_FOOD_TOKENS, player_config)
        return GameState(player_state.food_bag,
                         player_state.species_list,
                         player_state.hand,
                         food_on_watering_hole,
                         player_configs_to_species_boards_list(other_players))

    def __repr__(self) -> str:
        return "{}(food_bag={}, species_list={}, hand={}, food_on_watering_hole={}, other_player_boards={})" \
            .format(name_of_class(self), self.food_bag, self.species_list, self.hand, self.food_on_watering_hole, self.other_player_boards)

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, GameState) and
                (self.food_bag == cast(GameState, other).food_bag) and
                (self.species_list == cast(GameState, other).species_list) and
                (self.hand == cast(GameState, other).hand) and
                (self.food_on_watering_hole == cast(GameState, other).food_on_watering_hole) and
                (self.other_player_boards == cast(GameState, other).other_player_boards))
