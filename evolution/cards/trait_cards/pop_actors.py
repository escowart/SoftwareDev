from evolution.cards.trait_card import *


class FertileCard(TraitCard):

    def __init__(self, food_card_tokens: FoodCardTokens = NoFoodCardTokens) -> None:
        """
        :param food_card_tokens: The food tokens associated with this FertileCard
        """
        description = "FertileCard automatically adds one animal to the population when the food cards are revealed."
        TraitCard.__init__(self, food_card_tokens, description)

    @property
    def name(self) -> str:
        """ Get the name of this TraitCard """
        return "Fertile"

    def __eq__(self, other):
        return isinstance(other, FertileCard) and TraitCard.__eq__(self, other)

    def __repr__(self):
        return "FertileCard({})".format(self.food_card_tokens)