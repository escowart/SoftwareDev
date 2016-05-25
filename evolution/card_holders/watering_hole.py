from evolution.cards.all_cards import *


class WateringHole(IWateringHole):
    """ A class representing the Game's Watering Hole Boards """

    def __init__(self,
                 num_food_tokens:        Natural=STARTING_BOARD_FOOD_TOKENS,
                 played_cards:           OptList[PlayedCard]=NoList) -> None:
        """ Construct a WateringHole
        :param num_food_tokens: The number of food tokens currently on the watering hole
        :param played_cards: The Cards on the Watering Hole
        """
        self._num_food_tokens = Unset         # type: Natural
        self._played_cards = Unset            # type: List[PlayedCard]

        self.num_food_tokens = num_food_tokens
        self.played_cards = played_cards

    def add_food_card_tokens(self, food_card: TraitCard) -> None:
        """ Adds the number of food tokens on the food card to the watering hole
        Effect: Modifies the number of tokens the watering hole has
        :param food_card: The food card to turned into the food
        """
        new_food = max(self.num_food_tokens + food_card.food_card_tokens, NO_FOOD_TOKENS)
        self.num_food_tokens = new_food
        self.played_cards.append(food_card)

    @property
    def is_empty(self) -> bool:
        """Is this watering hole empty?"""
        return self.num_food_tokens <= 0

    def take_food(self, num_tokens: Natural) -> Natural:
        """ Takes food token from watering hole
        Effect: Modifies the number of tokens the watering hole has
        :param num_tokens: The number of tokens to take
        :return: Number of food tokens taken
        """
        if self.is_empty:
            raise ValueError("take_food: No food left on the watering hole")

        num_tokens = min(self.num_food_tokens, num_tokens)
        self.num_food_tokens -= num_tokens
        return num_tokens

    def clean_cards(self) -> None:
        """ Clean this Watering Hole by removing all Food Cards
        Effect: Modifies this Watering Hole to have no Food Cards
        """
        self.played_cards = []

    @property
    def num_food_tokens(self) -> Natural:
        """ Get the number of food tokens """
        return assert_set(self._num_food_tokens)

    @num_food_tokens.setter
    def num_food_tokens(self, num_food_tokens: Natural) -> None:
        """ Set the number of food tokens """
        assert_type(num_food_tokens, of_type=Natural, func_name="num_food_tokens")

        self._num_food_tokens = num_food_tokens

    @property
    def played_cards(self) -> List[TraitCard]:
        """ Get the played cards on this Species """
        return assert_set(self._played_cards)

    @played_cards.setter
    def played_cards(self, played_cards: OptList[TraitCard] = NoList) -> None:
        """ Set the played cards on this Species """
        if played_cards == NoList:
            played_cards = []

        assert_type(played_cards, collection_type=list, of_type=TraitCard)

        self._played_cards = cast(List[TraitCard], played_cards)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, WateringHole) and \
               self.num_food_tokens == cast(WateringHole, other).num_food_tokens and \
               self.played_cards == cast(WateringHole, other).played_cards

    def __repr__(self) -> str:
        return "WateringHole({}, {})".format(self.num_food_tokens, self.played_cards)