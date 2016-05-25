from evolution.cards.trait_card_interface import *


class OptWateringHole(object, metaclass=ABCMeta):
    """ A OptWateringHole is one of:
        - WateringHole
        - NoWateringHole
    """


class NoWateringHoleClass(OptWateringHole):
    """ A NoWateringHole """

    def __eq__(self, other):
        return isinstance(other, NoWateringHoleClass)

NoWateringHole = NoWateringHoleClass()


class IWateringHole(OptWateringHole, metaclass=ABCMeta):
    """ An interface of the Watering Hole """

    @abstractmethod
    def add_food_card_tokens(self, food_card: ITraitCard) -> None:
        """ Adds the number of food tokens on the food card to the watering hole
        Effect: Modifies the number of tokens the watering hole has
        :param food_card: The food card to turned into the food
        """
        raise NotImplementedError("add_food_card_tokens")
