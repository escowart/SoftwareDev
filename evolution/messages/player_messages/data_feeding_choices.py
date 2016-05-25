from evolution.species.all_species import *


class OptDataFeedingChoice(object, metaclass=ABCMeta):
    """ A OptDataFeedingChoice is one of:
        - NoDataFeedingChoice
        - DataFeedingChoice
    """


class NoDataFeedingChoiceClass(OptDataFeedingChoice):
    """ The No-DataFeedingChoice """
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, NoDataFeedingChoiceClass)

NoDataFeedingChoice = NoDataFeedingChoiceClass()


class DataFeedingChoice(OptDataFeedingChoice, metaclass=ABCMeta):
    """A DataFeedingChoice is one of:
        - ForgoAttack
        - FeedVegetarian
        - StoreFat
        - AttackWithCarnivore
    A FeedingChoice contains the actual objects that were chosen with the indices of a PlayerFeedingChoice
    """
    pass


class DataForgoChoice(DataFeedingChoice):
    """
    Represents a external_players's choice to not attack
    """
    def __repr__(self):
        return "PlayerForgoChoice()"

    def __eq__(self, other):
        return isinstance(other, DataForgoChoice)


class DataFeedVegetarian(DataFeedingChoice):
    """
    Wrapper holding the Vegetarian that a external_players has chosen to feed
    """
    def __init__(self, vegetarian: ISpecies) -> None:
        self.vegetarian = vegetarian  # type: ISpecies

    def __eq__(self, other):
        return isinstance(other, DataFeedVegetarian) and \
               self.vegetarian == cast(DataFeedVegetarian, other).vegetarian

    def __repr__(self):
        return "FeedVegetarian({})".format(self.vegetarian)


class DataStoreFat(DataFeedingChoice):
    """
    Wrapper holding the Species a external_players wishes to store fat on, as well as the number of food tokens to store
    """
    def __init__(self, species: ISpecies, num_food_to_store: NaturalPlus) -> None:
        """ Store a number of food tokens as Fat for the Species
        :param species: The Species
        :param num_food_to_store: The amount of food being stored
        """
        self.species = species  # type: Species
        self.num_food_to_store = num_food_to_store  # type: NaturalPlus

    def __repr__(self):
        return "StoreFood({}, {})".format(self.species, self.num_food_to_store)

    def __eq__(self, other):
        if not isinstance(other, DataStoreFat):
            return False
        other_sf = cast(DataStoreFat, other)
        return self.species == other_sf.species and \
               self.num_food_to_store == other_sf.num_food_to_store


class DataAttackWithCarnivore(DataFeedingChoice):
    """
    Wrapper holding the involved parties a external_players has chosen for an attack
    """
    def __init__(self, carnivore: ISpecies, target_player: IPlayer, target_species: ISpecies) -> None:
        """ Construct an Attack with Carnivore to feed that Carnivore
        :param carnivore: Your Carnivore
        :param target_player: The target external_players
        :param target_species: The target Species of the target external_players
        """
        self.carnivore = carnivore  # type: Carnivore
        self.target_player = target_player  # type: IPlayer
        self.target_species = target_species  # type: Species

    def __repr__(self):
        return "PlayerAttackWithCarnivore({},{},{})".format(self.carnivore, self.target_player, self.target_species)

    def __eq__(self, other):
        if not isinstance(other, DataAttackWithCarnivore):
            return False
        other_awc = cast(DataAttackWithCarnivore, other)
        return self.carnivore == other_awc.carnivore and \
               self.target_player == other_awc.target_player and \
               self.target_species == other_awc.target_species
