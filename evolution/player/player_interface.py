from evolution.species.sit_species_interface import *

"""PlayerConfiguration =  Tuple[NaturalPlus, OptListof[Species], Natural, OptListof[TraitCard]]"""
PlayerConfiguration = namedtuple('PlayerConfiguration', ['player_id', 'species_list', 'food_bag', 'hand'])


def is_player_config(value: Any) -> bool:
    """ Is the given value a Player Configuration
    :param value: The value
    :return: True if the given value is a Player Configuration, False otherwise
    """
    return is_collection(value, tuple, length=PLAYER_CONFIG_LEN) and \
        is_instance(value.player_id, int) and \
        is_list(value, of_type=ISpecies) and \
        is_instance(value.food_bag, Natural) and \
        is_list(value, of_type=ITraitCard)


class NoPlayerConfigurationClass(NoValue):
    """ The No Player Configuration class """

NoPlayerConfiguration = NoPlayerConfigurationClass()


OptPlayerConfiguration = Union[PlayerConfiguration, NoPlayerConfigurationClass]


class PlayerId(int):
    """ A class representing a Players Id """
    @staticmethod
    def is_instance(value: Any) -> bool:
        return isinstance(value, int)


class NoPlayerIdClass(NoValue):
    """ No Player Id Class """

NoPlayerId = NoPlayerIdClass()

OptPlayerId = Union[PlayerId, NoPlayerIdClass]

class InvalidPlayerClass(NoValue):
    """ An Invalid Player class """

InvalidPlayer = InvalidPlayerClass()

OptPlayer = Union[InvalidPlayerClass, 'IPlayer']


class IPlayer(object, metaclass=ABCMeta):
    """ An interface for PlayerState """

    @property
    @abstractmethod
    def player_id(self) -> NaturalPlus:
        """ Get the Player's id """
        raise NotImplementedError("player_id")

    @player_id.setter
    @abstractmethod
    def player_id(self, player_id: NaturalPlus) -> None:
        """ Set the Player's id """
        raise NotImplementedError("player_id")

    @abstractmethod
    def species_neighbor_iter(self, next_index: Index = DEFAULT_START_INDEX):
        raise NotImplementedError("neighbor_iter")

    @property
    @abstractmethod
    def species_list(self) -> List[ISpecies]:
        """ Get the List of Species in the order they exist on the Board """
        raise NotImplementedError("species_list")

    @species_list.setter
    @abstractmethod
    def species_list(self, species_list: List[ISpecies]) -> None:
        """ Set the List of Species in the order they exist on the Board """
        raise NotImplementedError("species_list")

    @abstractmethod
    def add_species(self, species: ISpecies) -> None:
        """ Add the given species to this Player State's list of Species
        Effect: Modifies the species_list by adding the given species to the end
        :param species: The Species being added
        """

    @property
    @abstractmethod
    def num_species(self) -> Natural:
        """ Returns the number of species this external_players has"""
        raise NotImplementedError("num_species")

    @property
    @abstractmethod
    def food_bag(self) -> Natural:
        """ Get the number of Food Tokens in this Player's Food Bag """
        raise NotImplementedError("food_bag")

    @food_bag.setter
    @abstractmethod
    def food_bag(self, food_bag: Natural) -> None:
        """ Set the number of Food Tokens in this Player's Food Bag """
        raise NotImplementedError("food_bag")

    @property
    def hand(self) -> List[ITraitCard]:
        """ Get this Player's Hand """
        raise NotImplementedError("hand")

    @hand.setter
    @abstractmethod
    def hand(self, hand: List[ITraitCard]) -> None:
        """ Set this Player's Hand """
        raise NotImplementedError("hand")

    @abstractmethod
    def remove_species_at_index(self,
                                species_index:    Index,
                                deck:             IDeck,
                                species_list:     OptList[ISpecies] = NoList) -> None:
        """ Removes the species at given index and draw cards from the deck
        Effect: Removes species from species list and adds cards to hand
        :param species_index: The index of the species being removed
        :param deck: Dealer's deck of cards
        :param species_list: The Species list it could be removed from
        """
        raise NotImplementedError("remove_species_at_index")

    @abstractmethod
    def can_be_attacked_by(self, attacker: ISpecies, defender_index: Index) -> bool:
        """ Can the Species at the given defender index within this Player's list of Species be attacked by the given
        Carnivore?
        :param attacker: The attacker
        :param defender_index: The index of the defender
        :return: True if the Carnivore can attack the Species at the index, False otherwise
        """
        raise NotImplementedError("can_be_attacked_by")

    @abstractmethod
    def feed_next_species(self, index_of_current_species: Index, watering_hole: IWateringHole) -> None:
        """ Feeds the next Species in this Player's species_list if it exists
        Effect: Modifies the next Species if it exists by feeding it and it's cooperation chain
        :param index_of_current_species: The index of current species
        :param watering_hole: The watering hole
        """
        raise NotImplementedError("feed_next_species")

    @abstractmethod
    def get_species_at_index(self, species_index: Index) -> ISpecies:
        """ Get the species at the given index
        :param species_index: The Index of the Species
        :return: The Species at the given IndexOfSpecies or raise IndexError
        """
        raise NotImplementedError("get_species_at_index")

    @property
    @abstractmethod
    def hand_size(self) -> Natural:
        """ The size of the Player's hand """
        raise NotImplementedError("hand_size")

    @abstractmethod
    def has_species_at_index(self, species_index: Index) -> bool:
        """ Does this Player have a Species at the given index?
        :param species_index: The index of the species
        :return: True if this has a Species at the index, False otherwise
        """
        raise NotImplementedError("has_species_at_index")
