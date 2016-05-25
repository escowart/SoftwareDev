from evolution.all_root_evo import *

class PlayedCard(object, metaclass=ABCMeta):
    """ A class representing a Played Card which is either a TraitCard or FaceDownCard """

    @staticmethod
    def is_instance(value) -> bool:
        """ Is the given vale a PlayedCard? """
        return is_played_card(value)

    @abstractmethod
    def flip(self) -> 'OptTraitCard':
        """ Flip this Played Card
        :return: The flipped card
        """
        raise NotImplementedError('flip')


def is_played_card(value: Any) -> bool:
    """ Is the given value a PlayedCard?
    :param value: The value being checked
    :return: True if the value is a PlayedCard, otherwise False
    """
    return isinstance(value, ITraitCard) or isinstance(value, FaceDownCard)


def flip_all(played_cards: List[PlayedCard]) -> List['ITraitCard']:
    """ Flip all the FaceDown Cards in the List and remove any that are none
    :param played_cards: The Played Cards
    :return: The Trait Cards
    """
    return [played_card.flip() for played_card in played_cards if played_card.flip() != NoTraitCard]


class FaceDownCard(object):
    def __init__(self, opt_trait_card: 'OptTraitCard' = 'NoTraitCard') -> None:
        """ Create a Face Down Card with either the TraitCard being played face down or None for FaceDownCards that are
        sent to each external_players
        :param opt_trait_card:  The OptTraitCard played Face down
        """
        self._opt_trait_card = Unset  # type: OptTraitCard

        self.opt_trait_card = opt_trait_card

    @property
    def opt_trait_card(self) -> 'OptTraitCard':
        """ Get the OptTraitCard """
        if self._opt_trait_card == Unset:
            raise UnsetValueError("opt_trait_card")

        return self._opt_trait_card

    @opt_trait_card.setter
    def opt_trait_card(self, opt_trait_card: 'OptTraitCard') -> None:
        """ Set the TraitCard """
        if not isinstance(opt_trait_card, 'OptTraitCard'):
            raise SetValueError("opt_trait_card: Must be OptTraitCard, got: {}".format(opt_trait_card))

        self._opt_trait_card = opt_trait_card

    def flip(self) -> 'OptTraitCard':
        """ Flip this Played Card
        :return: The flipped card
        """
        return self.opt_trait_card

    def __repr__(self) -> str:
        print("FaceDownCard({})".format(self.opt_trait_card))

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, FaceDownCard) and (self.opt_trait_card == cast(FaceDownCard, other).opt_trait_card)


class OptTraitCard(object, metaclass=ABCMeta):
    """ An OptTraitCard is one of:
        - NoTraitCard
        - ITraitCard
    """


class NoTraitCardClass(OptTraitCard):
    """ The No-TraitCard """
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, NoTraitCardClass)

    def __repr__(self) -> str:
        return "NoTraitCard"

NoTraitCard = NoTraitCardClass()


class ITraitCard(object, metaclass=ABCMeta):
    """ An interface for TraitCards """

    def flip(self) -> 'ITraitCard':
        """ Flip this Played Card
        :return: The flipped card
        """
        return self

    @abstractmethod
    def blocks_attack(self,
                      defender,
                      attacker,
                      defenders_left_neighbor,
                      defenders_right_neighbor,
                      owner_flag: OptSituationFlag = NoSituationFlag) -> bool:
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
        raise NotImplementedError("blocks_attack")

    @property
    def name(self) -> str:
        """ Get the name of this TraitCard """
        raise NotImplementedError("name")

    @property
    def food_card_tokens(self) -> 'FoodCardTokens':
        """ Get the Number of Food Tokens on the Card """
        raise NotImplementedError("food_card_tokens")


OptFoodCardTokens = Union['NoFoodCardTokensClass', 'FoodCardTokens']


class NoFoodCardTokensClass(object):
    """ The No-FoodCardTokens class """
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, NoFoodCardTokensClass)

    def __repr__(self) -> str:
        return "NoFoodCardTokens"

    def __gt__(self, other) -> bool:
        """ If this card has no food tokens it can't be greater than anything"""
        return False

NoFoodCardTokens = NoFoodCardTokensClass()


class FoodCardTokens(int):
    """ The FoodCardTokens class """
