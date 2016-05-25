from evo_json.serializers.species_boards import *


def serialize_player_configuration_as_player_state(player_config: PlayerConfiguration) -> PyJSON:
    """ Serialize the given Player Configuration as a Player State
    :param player_config: The Player's Configuration
    :return: The PyJSON
    """
    player_state = PlayerState.make_from_player_configuration(player_config)
    return player_state.serialize()


class PlayerState(Serializer):
    """ A class representing a Species Board in the Remote Protocol """
    def __init__(self,
                 food_on_watering_hole: Natural,
                 food_bag:              Natural,
                 species_list:          List[Species],
                 hand:                  List[TraitCard],) -> None:
        """ Construct a Species Boards
        :param species_list: The List of Species
        """
        self._food_on_watering_hole = Unset   # type: Natural
        self._food_bag = Unset                # type: Natural
        self._species_list = Unset            # type: List[Species]
        self._hand = Unset                    # type: List[TraitCard]

        self.food_bag = food_bag
        self.species_list = species_list
        self.hand = hand
        self.food_on_watering_hole = food_on_watering_hole

    def serialize(self) -> PyJSON:
        """ Serialize this value into a its PyJSON equivalent?
        :return: The serialized JSON
        """
        return [self.food_on_watering_hole,
                self.food_bag,
                SpeciesBoards(self.species_list).serialize(),
                convert_to_pj_loc(self.hand)]

    @staticmethod
    def can_deserialize(py_json: PyJSON) -> bool:
        """ Can this Serializers deserialize the given PyJSON value?
        :param py_json: A PyJSON value
        :return: True if this can deserialize the given value, False otherwise
        """
        if (is_list(py_json, length=PJ_PLAYER_STATE_LEN) and
                is_natural(py_json[0]) and
                is_natural(py_json[1]) and
                SpeciesBoards.can_deserialize(py_json[2])):
            try:
                [convert_from_pj_species_card(card) for card in py_json[3]]
                return True
            except ValueError:
                return False

        return False

    @staticmethod
    def deserialize(py_json: PyJSON) -> 'PlayerState':
        """ Deserialize the given value into a instance of this Serializer?
        :param py_json: A PyJSON value
        :return: An instance of this Deserialized
        """
        return PlayerState(py_json[0],
                           py_json[1],
                           SpeciesBoards.deserialize(py_json[2]).species_list,
                           convert_from_pj_loc(py_json[3]))
    
    def to_player_configuration(self) -> PlayerConfiguration:
        """ Convert these Boards into a PlayerConfiguration """
        return PlayerConfiguration(NO_ID, self.species_list, self.food_bag, self.hand)

    @staticmethod
    def make_from_watering_hole_player_configuration(food_on_watering_hole: Natural,
                                                     player_config: PlayerConfiguration) -> 'PlayerState':
        """ Convert the given Player Configuration into a Player State
        :param food_on_watering_hole: The food on the watering hole
        :param player_config: The Player Configuration that the PlayerState will be constructed for
        :return: The resulting Player State
        """
        return PlayerState(food_on_watering_hole, player_config.food_bag, player_config.species_list, player_config.hand)

    @property
    def food_bag(self) -> Natural:
        """ Get the food bag """
        return assert_set(self._food_bag)

    @food_bag.setter
    def food_bag(self, food_bag: Natural) -> None:
        """ Set the food bag """
        assert_type(food_bag, of_type=Natural, func_name="food_bag")
        self._food_bag = food_bag

    @property
    def species_list(self) -> List[Species]:
        """ Get the list of Species """
        return assert_set(self._species_list)

    @species_list.setter
    def species_list(self, species_list: List[Species]) -> None:
        """ Set the list of Species """
        assert_type(species_list, list, of_type=Species, func_name="species_list")
        self._species_list = species_list

    @property
    def hand(self) -> List[TraitCard]:
        """ Get the list of Species """
        return assert_set(self._hand)

    @hand.setter
    def hand(self, hand: List[TraitCard]) -> None:
        """ Set the list of Species """
        assert_type(hand, list, of_type=TraitCard, func_name="hand")
        self._hand = hand

    @property
    def food_on_watering_hole(self) -> Natural:
        """ Get the food on the watering_hole"""
        return assert_set(self._food_on_watering_hole)

    @food_on_watering_hole.setter
    def food_on_watering_hole(self, food_on_watering_hole: Natural) -> None:
        """ Set the food on the watering hole """
        assert_type(food_on_watering_hole, of_type=Natural, func_name="food_on_watering_hole")
        self._food_on_watering_hole = food_on_watering_hole

    def __repr__(self) -> str:
        return "{}(watering_hole={}, food_bag={}, species_list={}, hand={})" \
            .format(name_of_class(self), self.food_on_watering_hole, self.food_bag, self.species_list, self.hand)

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, PlayerState) and
                (self.food_on_watering_hole == cast(PlayerState, other).food_on_watering_hole) and
                (self.food_bag == cast(PlayerState, other).food_bag) and
                (self.species_list == cast(PlayerState, other).species_list) and
                (self.hand == cast(PlayerState, other).hand))