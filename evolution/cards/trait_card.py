from evolution.all_interfaces import *


class TraitCard(ITraitCard, metaclass=ABCMeta):
    """ A class representing a Trait Card which is Played on either the Watering Hole as a Food Card or is played
    on a Species as a Trait.
    """

    def __init__(self,
                 food_card_tokens: FoodCardTokens = NoFoodCardTokens,
                 description:      str = TRAIT_CARD_DEFAULT_DESC) -> None:
        """ Construct a TraitCard with its number of food tokens on the card
        :param food_card_tokens: The number of food tokens on the card
        :param description: The description on the card
        """
        self._food_card_tokens = Unset  # type: FoodCardTokens
        self._description = Unset       # type: str

        self.food_card_tokens = food_card_tokens
        self.description = description

    @property
    def food_card_tokens(self) -> FoodCardTokens:
        """ Get the Number of Food Tokens on the Card """
        return assert_set(self._food_card_tokens)

    @food_card_tokens.setter
    def food_card_tokens(self, food_card_tokens: OptFoodCardTokens) -> None:
        """ Set the Number of Food Tokens on the Card """
        if food_card_tokens != NoFoodCardTokens:
            assert_type(food_card_tokens, of_type=int, func_name="food_card_tokens")

            if not(TRAIT_CARD_MIN_FOOD_TOKENS <= food_card_tokens <= TRAIT_CARD_MAX_FOOD_TOKENS):
                raise SetValueError("food_card_tokens: Must be in range [{}, {}], got: {}"
                                .format(TRAIT_CARD_MIN_FOOD_TOKENS, TRAIT_CARD_MAX_FOOD_TOKENS, food_card_tokens))

        self._food_card_tokens = food_card_tokens

    @property
    def is_trait(self) -> bool:
        """ Is this TraitCard actual just a Trait without a Food Card value? """
        return self.food_card_tokens == NoFoodCardTokens

    @property
    def description(self) -> str:
        """ Get the description of the Card """
        return assert_set(self._description)

    @description.setter
    def description(self, description: str) -> None:
        """ Set the description """
        assert_type(description, of_type=str, func_name="description")
        self._description = description

    @property
    def name(self) -> str:
        """ Get the name of this TraitCard """
        raise NotImplementedError("name")

    @staticmethod
    def is_valid_card_count(card_count: Natural) -> bool:
        """ Is the given card count valid?
        :param card_count: The card count
        :return: True if the given card count valid, False otherwise
        """
        return card_count <= (TRAIT_CARD_MAX_FOOD_TOKENS - TRAIT_CARD_MIN_FOOD_TOKENS + 1)

    def blocks_attack(self,
                      defender:                 'ISituationSpecies',
                      attacker:                 'ISituationSpecies',
                      defenders_left_neighbor:  'OptSituationSpecies' = 'NoSituationSpecies',
                      defenders_right_neighbor: 'OptSituationSpecies' = 'NoSituationSpecies',
                      owner_flag:                OptSituationFlag = NoSituationFlag) -> bool:
        """ Does this TraitCard block attacks from a given attacker and the defenders neighbors
        :param defender:                 The defending Species
        :param attacker:                 The attacking Carnivore
        :param defenders_left_neighbor:  The defender's left neighbor,
        :param defenders_right_neighbor: The defender's right neighbor
        :param owner_flag:               The owner of this Trait
        :return:                         True if this blocks attacks from the given attacker, False otherwise

        Invariants:
        owner_flag = DEFENDER_RIGHT_NEIGHBOR_FLAG => defenders_right_neighbor is not None
        owner_flag = DEFENDER_LEFT_NEIGHBOR_FLAG  => defenders_left_neighbor  is not None
        """
        return False

    def __eq__(self, other):
        """ Abstract equality, called by subclasses
        :param other: the other value
        :return: True if the given TraitCard equals this one, False otherwise
        """
        return isinstance(other, TraitCard) and (self.food_card_tokens ==
                                                 cast(TraitCard, other).food_card_tokens)

    @staticmethod
    def create_all_cards(traitcard_type: type("TraitCard")) -> List["TraitCard"]:
        """ Create all cards of the given type
        :param traitcard_type: Type of TraitCard
        :return: List of TraitCard of all the possible cards of this type
        """
        return [traitcard_type(i) for i in range(TRAIT_CARD_MIN_FOOD_TOKENS, TRAIT_CARD_MAX_FOOD_TOKENS + 1)]


