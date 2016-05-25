from evolution.messages.player_messages.action_choice import *
from evolution.messages.player_messages.player_response import *

OptValidAction = Union['InvalidActionClass', 'Action']


class InvalidActionClass(NoValue):
    """ The No-Action """

InvalidAction = InvalidActionClass()


class Action(PlayerResponse):
    """ Represents an Action that a Player can make with a Food Card """
    def __init__(self,
                 food_card_choice:     FoodCardChoice,
                 gain_population_list: List[GainPopulation],
                 gain_body_list:       List[GainBody],
                 gain_board_list:      List[GainBoard],
                 replace_trait_list:   List[ReplaceTrait]) -> None:
        """ Constructs an Action
        :param food_card_choice: The card being played as a food card
        :param gain_population_list: List of  population gains
        :param gain_body_list: List of body size gains
        :param gain_board_list: List of Species Board gains
        :param replace_trait_list: List of Trait replacements
        """
        self._food_card_choice = Unset      # type: FoodCardChoice
        self._gain_population_list = Unset  # type: List[GainPopulation]
        self._gain_body_list = Unset        # type: List[GainBody]
        self._gain_board_list = Unset       # type: List[GainBoard]
        self._replace_trait_list = Unset    # type: List[ReplaceTrait]

        self.food_card_choice = food_card_choice
        self.gain_population_list = gain_population_list
        self.gain_body_list = gain_body_list
        self.gain_board_list = gain_board_list
        self.replace_trait_list = replace_trait_list

    def is_valid(self, dealer: IDealer, player: IPlayer):
        """ Is this action valid given the player and the dealers?
        :param dealer: The Dealer of the game
        :param player: The Player who gave this Action
        """
        player_copy = player.deep_copy()
        watering_hole_copy = deepcopy(dealer.watering_hole)
        rem_hand = rem_list(player_copy.hand)
        for action_choice in self.ordered_action_choices:
            if action_choice.is_valid(player_copy, rem_hand, watering_hole_copy):
                action_choice.apply(player_copy, rem_hand, watering_hole_copy)
            else:
                return False

        return True

    def apply(self, dealer: IDealer, player: IPlayer) -> None:
        """ Apply this action on the given Player and Dealer
        Effect: Modify the given Player State and the watering hole of the Dealer according to this action
        :param dealer: The Dealer
        :param player: The Player
        """
        rem_hand = rem_list(player.hand)
        [action_choice.apply(player, rem_hand, dealer.watering_hole) for action_choice in self.ordered_action_choices]
        player.hand = rem_hand.clean_list

    @property
    def ordered_action_choices(self) -> List[ActionChoice]:
        """ Get the Ordered Action Choices
        :return: The Ordered Action Choices
        """
        action_choices = [self.food_card_choice]
        action_choices += self.gain_board_list
        action_choices += self.gain_population_list
        action_choices += self.gain_body_list
        action_choices += self.replace_trait_list
        return action_choices

    def serialize(self) -> PyJSON:
        """ Serialize this value into a its PyJSON equivalent?
        :return: The serialized JSON
        """
        return [self.food_card_choice.serialize(),
                serialize_list(self.gain_population_list),
                serialize_list(self.gain_body_list),
                serialize_list(self.gain_board_list),
                serialize_list(self.replace_trait_list)]

    @staticmethod
    def can_deserialize(py_json: PyJSON) -> bool:
        """ Can this Serializers deserialize the given PyJSON value?
        :param py_json: A PyJSON value
        :return: True if this can deserialize the given value, False otherwise
        """
        return (is_list(py_json, length=PJ_ACTION4_LEN) and
                FoodCardChoice.can_deserialize(py_json[0]) and
                can_deserialize_list(GainPopulation, py_json[1]) and
                can_deserialize_list(GainBody,       py_json[2]) and
                can_deserialize_list(GainBoard,      py_json[3]) and
                can_deserialize_list(ReplaceTrait,   py_json[4]))

    @staticmethod
    def deserialize(py_json: PyJSON) -> 'Action':
        """ Deserialize the given value into a instance of this Serializer?
        :param py_json: A PyJSON value
        :return: An instance of this Deserialized
        """
        return Action(FoodCardChoice.deserialize(py_json[0]),
                      deserialize_list(GainPopulation, py_json[1]),
                      deserialize_list(GainBody, py_json[2]),
                      deserialize_list(GainBoard, py_json[3]),
                      deserialize_list(ReplaceTrait, py_json[4]))

    def __repr__(self):
        return "Action({}, {}, {}, {}, {})".format(self.food_card_choice,
                                                   self.gain_population_list,
                                                   self.gain_body_list,
                                                   self.gain_board_list,
                                                   self.replace_trait_list)

    def __eq__(self, other):
        return isinstance(other, Action) and \
               self.food_card_choice == cast(Action, other).food_card_choice and \
               self.gain_population_list == cast(Action, other).gain_population_list and \
               self.gain_body_list == cast(Action, other).gain_body_list and \
               self.gain_board_list == cast(Action, other).gain_board_list and \
               self.replace_trait_list == cast(Action, other).replace_trait_list

    @property
    def food_card_choice(self) -> FoodCardChoice:
        """ Get the Food Card Choice """
        return assert_set(self._food_card_choice)

    @food_card_choice.setter
    def food_card_choice(self, food_cards_choice: FoodCardChoice) -> None:
        """ Set the Food Card Choice """
        assert_type(food_cards_choice, of_type=FoodCardChoice, func_name="food_cards_choice")
        self._food_card_choice = food_cards_choice

    @property
    def gain_population_list(self) -> List[GainPopulation]:
        """ Get the List of GainPopulation """
        return assert_set(self._gain_population_list)

    @gain_population_list.setter
    def gain_population_list(self, gain_population_list: List[GainPopulation]) -> None:
        """ Set the List of GainPopulation """
        assert_type(gain_population_list, list, of_type=GainPopulation, func_name="gain_population_list")
        self._gain_population_list = gain_population_list

    @property
    def gain_body_list(self) -> List[GainBody]:
        """ Get the List of GainBody """
        return assert_set(self._gain_body_list)

    @gain_body_list.setter
    def gain_body_list(self, gain_body_list: List[GainBody]) -> None:
        """ Set the List of GainBody """
        assert_type(gain_body_list, list, of_type=GainBody, func_name="gain_body_list")
        self._gain_body_list = gain_body_list

    @property
    def gain_board_list(self) -> List[GainBoard]:
        """ Get the List of GainBoard """
        return assert_set(self._gain_board_list)

    @gain_board_list.setter
    def gain_board_list(self, gain_board_list: List[GainBoard]) -> None:
        """ Set the List of GainBoard """
        assert_type(gain_board_list, list, of_type=GainBoard, func_name="gain_board_list")
        self._gain_board_list = gain_board_list

    @property
    def replace_trait_list(self) -> List[ReplaceTrait]:
        """ Get the List of ReplaceTrait """
        return assert_set(self._replace_trait_list)

    @replace_trait_list.setter
    def replace_trait_list(self, replace_trait_list: List[ReplaceTrait]) -> None:
        """ Set the List of ReplaceTrait """
        assert_type(replace_trait_list, list, of_type=ReplaceTrait, func_name="replace_trait_list")
        self._replace_trait_list = replace_trait_list
