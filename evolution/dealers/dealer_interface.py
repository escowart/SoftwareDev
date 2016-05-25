from evolution.dealers.player_sequence_interface import *

"""Configuration =  Tuple[PlayerSequence, WateringHole, Deck]"""
Configuration = namedtuple('Configuration', ['player_sequence', 'watering_hole', 'deck'])

def is_configuration(configuration: Configuration):
    return (isinstance(configuration.player_sequence,  IPlayerSequence) and
            isinstance(configuration.watering_hole, IWateringHole) and
            isinstance(configuration.deck, IDeck))


class NoDealerClass(NoValue):
    """ The No Dealer class"""

NoDealer = NoDealerClass()


OptDealer = Union['IDealer', NoDealerClass]


class IDealer(object, metaclass=ABCMeta):
    """Interface for dealers"""

    @property
    @abstractmethod
    def player_sequence(self) -> IPlayerSequence:
        """ Get the Sequence of Player States """
        raise NotImplementedError('player_sequence')

    @player_sequence.setter
    @abstractmethod
    def player_sequence(self, player_sequence: IPlayerSequence) -> None:
        """ Set the Sequence of Player States """
        raise NotImplementedError('player_sequence')

    @abstractmethod
    def feed_species(self, species_index: Index, player: IPlayer) -> None:
        """Feeds the Species at the given index of the given external_players
        Effect: Feeds the Species and modifies any changed species accordingly
        :param species_index: Species Index of the species to be fed
        :param player: Player that owns the species to be fed
        """
        raise NotImplementedError('feed_species')

    @abstractmethod
    def feed_scavengers(self) -> None:
        """ Go through each PlayerState in sequential order and feed each of the Scavengers
        Effect: Modifies the scavengers in each external_players's species to feed
        """

    @abstractmethod
    def grab_food_token_from_watering_hole(self) -> Natural:
        """ Grab a food token from the watering hole
        :return: 1 food token if tokens are on the watering hole, 0 otherwise
        """
        raise NotImplementedError('grab_food_token_from_watering_hole')

    @property
    @abstractmethod
    def deck(self) -> IDeck:
        """ Get the Deck of TraitCards """
        raise NotImplementedError("deck")

    @deck.setter
    @abstractmethod
    def deck(self, deck: IDeck) -> None:
        """ Set the Deck of TraitCards """
        raise NotImplementedError("deck")

    @abstractmethod
    def get_player_list_without(self, player_state: IPlayer) -> List[IPlayer]:
        """ Get the Player List without the given player_state
        :param player_state: The State of the Player
        :return: The sequence as a list without the given player_state
        """
        raise NotImplementedError("get_player_list_without")

    @abstractmethod
    def get_player_list_with_player_at_end(self, player_state: IPlayer) -> List[IPlayer]:
        """ Get the Player List with the given player_state moved to the end of the list
        :param player_state: The State of the Player
        :return: The sequence as a list with the player_state moved to the end of the list
        """
        raise NotImplementedError("get_player_list_with_player_state_at_end")

    @abstractmethod
    def can_player_attack_or_store(self, player: IPlayer):
        """ Can the given Player State attack or store?
        :param player: The Player
        :return: True if the given Player State can attack or store, False otherwise
        """
        raise NotImplementedError("can_player_attack_or_store")

    @abstractmethod
    def reset_forgo_for_all_players(self) -> None:
        """ Reset all the players so they haven't forgon a choice this turn
        Effect: Modfies the has_forgon_this_turn field of each player
        """
        raise NotImplementedError("reset_forgo_for_all_players")

    @property
    @abstractmethod
    def food_on_watering_hole(self) -> Natural:
        """ Get the number of food tokens on the Watering Hole """
        raise NotImplementedError("food_on_watering_hole")

    @property
    @abstractmethod
    def configuration_sequence_without(self):
        """ Configuration Sequence without the given Player """
        raise NotImplementedError("configuration_sequence_without")

    @abstractmethod
    def split_configuration_sequence(self, player: IPlayer) \
            -> Tuple[List[PlayerConfiguration], List[PlayerConfiguration]]:
        """ Get the Configuration Sequence split in half at the index of the given player without the player
        :param player: The player that the list is split before and after
        :return: The two Configuration Sequences
        """
        raise NotImplementedError("split_configuration_sequence")

    @property
    @abstractmethod
    def watering_hole(self) -> IWateringHole:
        """ Get the Watering Hole """
        raise NotImplementedError("watering_hole")

    @watering_hole.setter
    @abstractmethod
    def watering_hole(self, watering_hole: OptWateringHole) -> None:
        """ Set the Watering Hole """
        raise NotImplementedError("watering_hole")
