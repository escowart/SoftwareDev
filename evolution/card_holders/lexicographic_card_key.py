from evolution.cards.trait_card_interface import *


@total_ordering
class LexicographicCardKey(OrderedKey):
    def __init__(self, card: ITraitCard) -> None:
        self.card = card

    def __gt__(self, other: ITraitCard) -> bool:
        """ Checks if this card is greater than the given card
        :param other: The TraitCard it is comparing itself to
        :return: True if this card is greater than the given card
        """
        return (self.card.name > other.card.name) or \
               ((self.card.name == other.card.name) and (self.card.food_card_tokens > other.card.food_card_tokens))

    def __eq__(self, other: ITraitCard) -> bool:
        """ Checks if this card is equal to the given card
        :param other: The TraitCard it is comparing itself to
        :return: True if this card is equal to the given card
        """
        return (self.card.name == other.card.name) and (self.card.food_card_tokens == other.card.food_card_tokens)

    def __repr__(self) -> str:
        return "LexicographicCardKey({})".format(self.card)

