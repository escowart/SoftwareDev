from evolution.cards.trait_card import *


class CarnivoreCard(TraitCard):
    def __init__(self, food_card_tokens: FoodCardTokens = NoFoodCardTokens) -> None:
        """ Construct a Carnivore Card
        :param food_card_tokens: The food tokens associated with this CarnivoreCard
        """
        TraitCard.__init__(self, food_card_tokens,
                           "CarnivoreCard must attack to eat during the evolution stage.")

    @property
    def food_card_tokens(self) -> FoodCardTokens:
        """ Get the number of tokens as a FoodCard """
        return assert_set(self._food_card_tokens)

    @food_card_tokens.setter
    def food_card_tokens(self, food_card_tokens: OptFoodCardTokens) -> None:
        """ Set the Number of Food Tokens
        :param food_card_tokens: The new number_of_tokens
        :raise: ValueError if sent invalid value
        """
        if food_card_tokens != NoFoodCardTokens:
            assert_type(food_card_tokens, of_type=int, func_name="food_card_tokens")

            if not (CARNIVORE_MIN_FOOD_TOKENS <= food_card_tokens <= CARNIVORE_MAX_FOOD_TOKENS):
                raise SetValueError("food_card_tokens: Must be in range [{}, {}], got: {}"
                             .format(CARNIVORE_MIN_FOOD_TOKENS, CARNIVORE_MAX_FOOD_TOKENS, food_card_tokens))

        self._food_card_tokens = food_card_tokens

    @staticmethod
    def is_valid_card_count(card_count: Natural) -> bool:
        """ Is the given card count valid?
        :param card_count: The card count
        :return: True if the given card count valid, False otherwise
        """
        return card_count <= (CARNIVORE_MAX_FOOD_TOKENS - CARNIVORE_MIN_FOOD_TOKENS + 1)


    @property
    def name(self) -> str:
        """ Get the name of this TraitCard """
        return "Carnivore"

    def __eq__(self, other):
        return isinstance(other, CarnivoreCard) and TraitCard.__eq__(self, other)

    def __repr__(self):
        return "CarnivoreCard({})".format(self.food_card_tokens)

    @staticmethod
    def create_all_cards(traitcard_type: type("TraitCard")) -> List["TraitCard"]:
        """ Create all cards of the given type
        :param traitcard_type: Type of TraitCard
        :return: List of TraitCard of all the possible cards of this type
        """
        return [CarnivoreCard(i) for i in range(CARNIVORE_MIN_FOOD_TOKENS, CARNIVORE_MAX_FOOD_TOKENS + 1)]
