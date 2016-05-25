from evolution.external_players.all_external_players import *


class PlayerSequence(IPlayerSequence):
    """ A class representing a Dealer's Player Sequence """

    def __init__(self, player_list: List[Player]) -> None:
        """ Construct a Player Sequence
        :param player_list: The list of players in this sequence in order
        """
        self._player_list = Unset  # type: List[Player]

        self.player_list = player_list

    def kick_player(self, player: Player) -> None:
        """ Kick the Player this Player Sequence
        Effect: Modifies this Player Sequence by removing the Player at the given Index
        :param player: The Player being removed
        """
        player.shut_down()
        self.player_list.remove(player)
        evo_print("{} has been Kick".format(player.player_str))

    def copy(self) -> 'PlayerSequence':
        """ Get a Copy of this Player Sequence """
        return PlayerSequence(self.player_list[:])

    @property
    def player_list(self) -> List[Player]:
        """ Get the list of Players in this sequence in order """
        return assert_set(self._player_list)

    @player_list.setter
    def player_list(self, player_list: List[Player]) -> None:
        """ Set the list of Players in this sequence in order """
        assert_type(player_list, list, of_type=Player, func_name="player_list")
        self._player_list = player_list

    def __iter__(self) -> List[Player]:
        """ Get the iterator for this Player Sequence """
        return iter(self.player_list)

    def __len__(self) -> Natural:
        """ Get the length of this """
        return len(self.player_list)

    def __getitem__(self, player_index: Index) -> Player:
        """ Get the Player at the given index """
        return self.player_list[player_index]

    def __setitem__(self, player_index: Index, player: Player) -> None:
        """ Set the Player at the given index """
        self.player_list[player_index] = player

    def __add__(self, other_sequence: 'PlayerSequence') -> 'PlayerSequence':
        return PlayerSequence(self.player_list + other_sequence.player_list)

    def __repr__(self) -> str:
        return "PlayerSequence({})".format(self.player_list)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, PlayerSequence) and (self.player_list == cast(PlayerSequence, other).player_list)

    @property
    def num_players(self) -> Natural:
        """ Get the number of Players in the Sequence """
        return len(self)

    def feedable_player_sequence_iter(self, dealer: IDealer) -> 'PlayerSequence.PlayerFeedableSequenceIterator':
        """ Get this Player Sequence as a Feedable Player Sequence Iterator
        :param watering_hole: The watering hole
        :return: The Feedable Player Sequence Iterator
        """
        return PlayerSequence.PlayerFeedableSequenceIterator(dealer)

    def sequence_starting_with(self, start_index: Index) -> 'PlayerSequence':
        """ Get the Player Sequence starting with the given index
        :param start_index: The starting index
        """
        return self[start_index:] + self[:start_index]

    def get_player_list_with_player_at_end(self, player: Player) -> List[Player]:
        """ Get the Player List with the given player moved to the end of the list
        :param player: The State of the Player
        :return: The sequence as a list with the player moved to the end of the list
        """
        return self.get_player_list_without(player) + [player]

    def index(self, player: Player) -> Index:
        """ Get the index of the given Player
        :param player: The Player
        :return: The index of the player
        """
        return self.player_list.index(player)

    @property
    def all_cards(self) -> List[TraitCard]:
        """ Get all the cards in this Sequence """
        cards = []
        for player in self:
            cards += player.all_cards

        return cards

    def get_player_list_without(self, player: Player) -> List[Player]:
        """ Get the Player List without the given player
        :param player: The Player
        :return: The sequence as a list without the given player
        """
        player_list_copy = self.player_list[:]
        player_list_copy.remove(player)
        return player_list_copy

    @property
    def configuration_sequence(self) -> List[PlayerConfiguration]:
        """ Get this Sequence as a List of Player Configurations """
        return [player.player_configuration_without_hand_and_bag for player in self]

    def split_configuration_sequence(self, player: Player) -> Tuple[List[PlayerConfiguration],
                                                                    List[PlayerConfiguration]]:
        """ Get the Configuration Sequence split in half at the index of the given player without the player
        :param player: The player that the list is split before and after
        :return: The two Configuration Sequences
        """
        config_sequence = self.configuration_sequence
        player_index = self.index(player)
        first_half = config_sequence[:player_index]
        second_half = config_sequence[player_index:]
        second_half.pop(DEFAULT_START_INDEX)
        return first_half, second_half

    def configuration_sequence_without(self, player: Player) -> List[PlayerConfiguration]:
        """ Get this Sequence without the given Player as a List of Player Configurations
        :param player: The Player being removed
        :return: The Player Configuration Sequence without the given player
        """
        player_index = self.index(player)
        conf_sequence = self.configuration_sequence[:]
        conf_sequence.pop(player_index)
        return conf_sequence

    def reset_forgo_for_all_players(self) -> None:
        """ Reset the has_forgon_this_turn field for all Players in this Sequence
        Effect: Modfies each players has_forgon_this_turn field
        """
        for player in self:
            player.has_forgon_this_turn = HASNT_FORGON

    class PlayerFeedableSequenceIterator(Iterator[Player]):
        """ A iterator for iterating over the feedable player in a Player Sequence """
        def __init__(self,
                     dealer:            IDealer,
                     previous_index:    OptStartIterationIndex=StartIterationIndex) -> None:
            """ Construct a Feedable Player Iterator
            :param player_sequence: The Player Sequence
            :param watering_hole: The watering hole of the game
            :param previous_index: The previous player who fed's index
            """
            Iterator.__init__(self, previous_index)
            self.dealer = dealer
            self.dealer.reset_forgo_for_all_players()

        def __next__(self) -> Tuple[Player, FeedingChoice]:
            """ Get the next Player in this Feedable Player Sequence
            Effect: Moves the last_player_index to the index of the Player State that was returned
            :return: The next Player State and the FeedingChoice of that Player
            :raise: Stop Iterator if not Player State remains
            """
            if self.watering_hole.is_empty:
                self.stop_iteration()

            next_feedable_index = self.next_feedable_player_index

            if next_feedable_index == StopIterationIndex:
                self.stop_iteration()

            player, choice = self.get_player_and_feeding_choice(self.dealer, next_feedable_index)

            if choice == InvalidFeedingChoice:
                self.player_sequence.kick_player(player)
                return next(self)

            self.previous_index = next_feedable_index
            return player, choice

        def get_player_and_feeding_choice(self,
                                          dealer:       IDealer,
                                          player_index: Index) -> Tuple[Player, OptValidFeedingChoice]:
            """ Get the Player at the given index and their Feeding Choice
            :param dealer: The Dealer of the Game
            :param player_index: The index of the Player
            :return: The Player and their Feeding Choice
            """
            player = self.player_sequence[player_index]
            choice = player.choose_feeding(dealer)
            return player, choice

        @property
        def next_feedable_player_index(self) -> OptStopIterationIndex:
            """ Get the next player index of this Sequence
            :return: The next Player State's index or NoFeedablePlayerIndex if no Player State can feed
            """
            if is_index(self.next_index_in_cycle):
                for player in self.sequence_starting_with(self.next_index_in_cycle):
                    if player.can_any_species_feed_or_store(self.player_sequence):
                        return self.index(player)
                    else:
                        player.has_forgon_this_turn = HAS_FORGON

            return StopIterationIndex

        def stop_iteration(self) -> None:
            """ Clears the previous feeding choice of each player and raises a StopIteration
            :raises: StopIteration to stop the iterator
            """
            raise StopIteration()

        @property
        def num_players(self) -> Natural:
            """ Get the number of Players in the Sequence """
            return self.player_sequence.num_players

        def sequence_starting_with(self, start_index: Index) -> 'PlayerSequence':
            """ Get the Player Sequence starting with the given index
            :param start_index: The starting index
            """
            return self.player_sequence.sequence_starting_with(start_index)

        @property
        def item_list(self) -> List[Item]:
            """ Get the List[Item] that is being iterated over """
            return self.player_sequence.player_list

        @property
        def player_sequence(self) -> 'PlayerSequence':
            """ Get the Player Sequence """
            return self.dealer.player_sequence

        @player_sequence.setter
        def player_sequence(self, player_sequence: 'PlayerSequence') -> None:
            """ Set the Player Sequence """
            self.dealer.player_sequence = player_sequence

        @property
        def watering_hole(self) -> WateringHole:
            """ Get the WateringHole """
            return self.dealer.watering_hole

        @property
        def food_on_watering_hole(self) -> Natural:
            """ Get the WateringHole """
            return self.dealer.food_on_watering_hole

        @watering_hole.setter
        def watering_hole(self, watering_hole: WateringHole) -> None:
            """ Set the WateringHole"""
            self.dealer.watering_hole = watering_hole

