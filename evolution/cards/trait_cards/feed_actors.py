from evolution.cards.trait_card import *


class CooperationCard(TraitCard):

    def __init__(self, food_card_tokens: FoodCardTokens = NoFoodCardTokens) -> None:
        """
        :param food_card_tokens: The food tokens associated with this CooperationCard
        """
        description = "CooperationCard automatically feeds the species to its right one token of food every time it " \
                      "eats (taken from the common food supply at the watering hole)."
        TraitCard.__init__(self, food_card_tokens, description)

    @property
    def name(self) -> str:
        """ Get the name of this TraitCard """
        return "Cooperation"

    def __eq__(self, other):
        return isinstance(other, CooperationCard) and TraitCard.__eq__(self, other)

    def __repr__(self):
        return "CooperationCard({})".format(self.food_card_tokens)


class ScavengerCard(TraitCard):

    def __init__(self, food_card_tokens: FoodCardTokens = NoFoodCardTokens) -> None:
        """
        :param food_card_tokens: The food tokens associated with this ScavengerCard
        """
        description = "Scavenger automatically eats one food token every time a Carnivore eats another species."
        TraitCard.__init__(self, food_card_tokens, description)

    @property
    def name(self) -> str:
        """ Get the name of this TraitCard """
        return "Scavenger"

    def __eq__(self, other):
        return isinstance(other, ScavengerCard) and TraitCard.__eq__(self, other)

    def __repr__(self):
        return "ScavengerCard({})".format(self.food_card_tokens)


class ForagingCard(TraitCard):

    def __init__(self, food_card_tokens: FoodCardTokens = NoFoodCardTokens) -> None:
        """
        :param food_card_tokens: The food tokens associated with this ForagingCard
        """
        description = "Foraging enables this species to eat two tokens of food for every evolution."
        TraitCard.__init__(self, food_card_tokens, description)

    @property
    def name(self) -> str:
        """ Get the name of this TraitCard """
        return "Foraging"

    def __eq__(self, other):
        return isinstance(other, ForagingCard) and TraitCard.__eq__(self, other)

    def __repr__(self):
        return "ForagingCard({})".format(self.food_card_tokens)


class LongNeckCard(TraitCard):

    def __init__(self, food_card_tokens: FoodCardTokens = NoFoodCardTokens) -> None:
        """
        :param food_card_tokens: The food tokens associated with this LongNeckCard
        """
        description = "Long Neck automatically adds one food token for the entire species when the food cards are " \
                      "revealed."
        TraitCard.__init__(self, food_card_tokens, description)

    @property
    def name(self) -> str:
        """ Get the name of this TraitCard """
        return "Long Neck"

    def __eq__(self, other):
        return isinstance(other, LongNeckCard) and TraitCard.__eq__(self, other)

    def __repr__(self):
        return "LongNeckCard({})".format(self.food_card_tokens)