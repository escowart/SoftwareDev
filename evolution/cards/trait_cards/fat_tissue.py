from evolution.cards.trait_card import *


'''--------------FatTissueCard--------------'''


class FatTissueCard(TraitCard):
    def __init__(self,
                 food_card_tokens: FoodCardTokens = NoFoodCardTokens,
                 stored_food: Natural = FAT_TISSUE_STARTING_FOOD) -> None:
        """ Construct a FatTissue Trait Card
        :param food_card_tokens: The number of food tokens associated with this FatTissueCard
        :param stored_food: The food currently stored on the FatTissueCard from last round's storage
        """
        description = "Fat Tissue allows a species to store as many food tokens as its body-size count. In a " \
                      "physical game, the additional food is stored on the actual card. It must be used to feed the " \
                      "species at the beginning of the next evolution round, before any food is taken from the " \
                      "watering hole."
        TraitCard.__init__(self, food_card_tokens, description)
        self._stored_food = Unset  # type: Natural

        self.stored_food = stored_food

    @property
    def name(self) -> str:
        """ Get the name of this TraitCard """
        return "Fat Tissue"

    @property
    def stored_food(self) -> Natural:
        """ Gets the Number of Food Tokens stored as Fat Tissue """
        if self._stored_food == Unset:
            raise ValueError("stored_food: Not Set to Natural")

        return self._stored_food

    @stored_food.setter
    def stored_food(self, stored_food: Natural) -> None:
        """ Set the Stored Fat Food """
        if not is_natural(stored_food):
            raise SetValueError("stored_food: Must be Natural")

        self._stored_food = stored_food

    def take_food(self) -> Natural:
        """ Takes the food from this FatTissue card, returning the food stored and reducing the food stored to 0
        :return: The number of food tokens taken
        """
        num_tokens_taken = self.stored_food
        self.stored_food = FAT_TISSUE_STARTING_FOOD
        return num_tokens_taken

    def store_food(self, food: Natural) -> None:
        """ Store the given amount of Food as Fat Tissue
        :param food: The food being stored
        """
        self.stored_food += food

    def __eq__(self, other):
        return isinstance(other, FatTissueCard) and (cast(FatTissueCard, other).stored_food == self.stored_food) and \
               TraitCard.__eq__(self, other)

    def __repr__(self):
        return "FatTissueCard({}, {})".format(self.food_card_tokens, self.stored_food)