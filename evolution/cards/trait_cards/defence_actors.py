from evolution.cards.trait_card import *


class HornCard(TraitCard):

    def __init__(self, food_card_tokens: FoodCardTokens = NoFoodCardTokens) -> None:
        """ Construct a Horn Card
        :param food_card_tokens: The food tokens associated with this HornCard
        """
        description = "Horns kills one animal of an attacking CarnivoreCard species before the attack is completed."
        TraitCard.__init__(self, food_card_tokens, description)

    @property
    def name(self) -> str:
        """ Get the name of this TraitCard """
        return "Horn"

    def __eq__(self, other):
        return isinstance(other, HornCard) and TraitCard.__eq__(self, other)

    def __repr__(self):
        return "HornCard({})".format(self.food_card_tokens)