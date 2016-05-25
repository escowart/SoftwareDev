from evolution.cards.trait_card import *


class PackHuntingCard(TraitCard):
    def __init__(self, food_card_tokens: FoodCardTokens = NoFoodCardTokens) -> None:
        """ Construct a Pack Hunting Card
        :param food_card_tokens: The food tokens associated with this PackHuntingCard
        """
        description = "Pack Hunting adds this species population size to its body size for attacks on other species."
        TraitCard.__init__(self, food_card_tokens, description)

    @property
    def name(self) -> str:
        """ Get the name of this TraitCard """
        return "Pack Hunting"

    def __eq__(self, other):
        return isinstance(other, PackHuntingCard) and TraitCard.__eq__(self, other)

    def __repr__(self):
        return "PackHuntingCard({})".format(self.food_card_tokens)
