from evolution.external_players.external_player import *
from evolution.player.player import *


class AbsExternalPlayer(ExternalPlayer, metaclass=ABCMeta):
    """ A class representing an abstract external player whose methods other External Players use """

    """ A class representing the Silly Player which preforms a simple strategy """

    def __init__(self, player_id: int, player_configuration: PlayerConfiguration):
        """ Construct a SillyPlayer with its corresponding PlayerState
        :param player_id: The id of the Player
        :param player_configuration: This Silly Player's state
        """
        self._player_id = Unset  # type: int
        self._player = Unset     # type: Player

        self.player_id = player_id
        self.player_configuration = player_configuration

    @property
    def player_id(self) -> int:
        """ This external player's Player id"""
        if self._player_id == Unset:
            raise UnsetValueError("player_id")

        return self._player_id

    @player_id.setter
    def player_id(self, player_id: int) -> None:
        """ Set this external player's Player id"""
        if not isinstance(player_id, int):
            raise SetValueError("player_id: Must be int, got: {}".format(player_id))

        self._player_id = player_id

    @property
    def player(self) -> Player:
        """ Get the state of this  Silly Player """
        if self._player == Unset:
            raise UnsetValueError("state")

        return self._player

    @player.setter
    def player(self, player: Player) -> None:
        """ Set the state of this  Silly Player """
        assert_type(player, of_type=Player, func_name="player")

        self._player = player

    @property
    def player_configuration(self) -> PlayerConfiguration:
        """ This external Player's Configuration"""
        return self.player.player_configuration

    @player_configuration.setter
    def player_configuration(self, player_configuration: PlayerConfiguration):
        """ Set this external Player's Configuration """
        self.player = Player(*player_configuration)

    @property
    def own_species_list(self) -> List[Species]:
        """ Get this external Player's own species list """
        return self.player.species_list

    @property
    def hand(self) -> List[TraitCard]:
        """ Get this external Player's hand """
        return self.player.hand

    @property
    def hand_size(self) -> int:
        """ Get this external Player's hand size """
        return self.player.hand_size

    @property
    def ordered_hand(self) -> List[TraitCard]:
        """ Get this external Player's hand size """
        return self.player.get_ordered_hand(LexicographicCardKey)

    @property
    def num_species(self) -> Natural:
        """ Get the number of Species this Player owns """
        return len(self.own_species_list)

    def index_of_own_species(self, species: Species) -> Index:
        """ Get the index of the given species in this player's species list
        :param species: The Species you are looking for
        :return: The Index of the Species"""
        return self.own_species_list.index(species)

    def get_next_index_in_hand(self, ordered_hand: List[TraitCard]) -> Index:
        """ Get the index of the next TraitCard in hand
        Effect: Pops off the first card in the ordered hand
        :param ordered_hand: This player's ordered hand
        :return: The Index of the next TraitCard in hand
        """
        card = ordered_hand.pop()
        index = self.hand.index(card)
        return index