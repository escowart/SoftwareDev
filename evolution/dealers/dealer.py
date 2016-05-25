from evolution.dealers.player_sequence import *


class Dealer(IDealer):
    """ A class representing a Dealer of the Evolution Game """

    def __init__(self,
                 player_sequence:          PlayerSequence,
                 watering_hole:            OptWateringHole = NoWateringHole,
                 deck:                     OptDeck = NoDeck) -> None:
        """ Construct a Dealer with the player sequence
        :param player_sequence: The Sequence of Players
        :param watering_hole: The Watering Hole
        :param deck: The Deck of Cards
        """
        self._player_sequence = Unset       # type: PlayerSequence
        self._watering_hole = Unset         # type: WateringHole
        self._deck = Unset                  # type: Deck

        self.player_sequence = player_sequence
        self.watering_hole = watering_hole
        self.deck = deck

    @staticmethod
    def make_evolution_dealer(players: List[Player]) -> 'Dealer':
        """ Make the Dealer from the given list of Players
        :param players: The Players in the game
        :return: The newly created Dealer
        """
        return Dealer(PlayerSequence(players), deck=Deck.create_deck())

    def run_evolution(self) -> None:
        """ Run the Game Evolution
        Effect: Prints the Resulting Game
        """
        print(START_MESSAGE)
        turn = 0
        while not self.is_game_over:
            turn += 1
            evo_print("\nTurn {} Begins".format(turn))
            self.step1()
            actions = self.step2_and_step3()
            self.step4(actions)
            self.end_turn()

        print("\nEvolution Ends After {} Turns\n\nFinal Scores:".format(turn))
        self.end_game()

    def step1(self) -> None:
        """ Start the next Turn of the Game by suffleling the deck and sending the Players their Cards
          and new Species Boards if they need one
        Effect: Modifies the Deck by removing Cards and Adds cards to player hands
        """
        evo_print("\n\tStep 1:")
        self.shuffle_deck()
        self.deal()
        self.start_turn()

    def step2_and_step3(self) -> List[Action]:
        """ Get the Actions from each of the Players
        :return: The Actions of each Player
        """
        evo_print("\n\tStep 2 & Step 3:")
        [evo_print("\t\t{}".format(player)) for player in self.player_sequence]
        evo_print("")
        player_sequence_copy = self.player_sequence.copy()
        result = []
        for player in player_sequence_copy:
            player_action = player.choose_action(self)

            if player_action == InvalidAction:
                self.kick_player(player)
            else:
                result.append(player_action)

        return result

    def step4(self, actions: List[Action]) -> None:
        """ Preform the given actions on the Player in the player_sequence which called it
            len(actions) == self.num_players
            actions[i] is applied on self.player_sequence[i]
        :param actions: The actions being applied on the players
        """
        self.apply_actions(actions)
        evo_print("\n\tStep 4:")
        self.trigger_food_card_flip_traits()
        evo_print("\t\tWatering Hole: {}\n".format(self.watering_hole))
        [evo_print("\t\t{}".format(player)) for player in self.player_sequence]
        evo_print("")
        self.all_species_move_fat_food()
        self.feed()

    def end_turn(self) -> None:
        """ End the Turn by reducing the population of all species that where not fed enough,
            then move the fed tokens to the food bag of their player
            then clean the watering hole of all cards
        Effect: Modifies any species which unfed population, moves extinct species,
                then modifies all species with tokens and player's food bags
                then modifies the watering hole by removing the cards from it
        """
        self.all_species_reduce_to_fed_population()
        self.all_players_move_fed_food_to_food_bag()
        self.clean_watering_hole()

    def end_game(self) -> None:
        """ End the Game by printing the results and telling all players to shutdown
        Effect: Closes all open sockets in the players
        """
        self.print_results()
        [player.shut_down() for player in self.player_sequence]

    def start_turn(self) -> None:
        """ Start the Turn by send each Player their current state
        Effect: Start the Turn by sending each player their state
        """
        player_sequence_copy = self.player_sequence.copy()
        for player in player_sequence_copy:
            if player.start_turn(self.food_on_watering_hole) == InvalidMessage:
                self.kick_player(player)

    def apply_actions(self, actions: List[Action]) -> None:
        """ Preform the given actions on the Player in the player_sequence which called it
            len(actions) == self.num_players
            actions[i] is applied on self.player_sequence[i]
        Effect: Modifies each player by the corresponding action
        :param actions: The actions being applied on the players
        """
        if not is_list(actions, of_type=Action, length=self.num_players):
            raise ValueError("apply_actions: Must be given a List[Action] of length: {}, got: {}"
                             .format(self.num_players, actions))

        for player, action in zip(self.player_sequence, actions):
            evo_print("{}: {}".format(player.player_str, action))
            action.apply(self, player)

    def trigger_food_card_flip_traits(self) -> None:
        """ Trigger the Food Card Flip Traits of any Species of any Player in order
        Effect: Modifies Players and Species according to the Food Card Flip Traits
        """
        self.all_species_trigger_fertile()
        self.all_species_trigger_long_neck()

    def all_species_trigger_fertile(self) -> None:
        """ Trigger the Fertile trait of any Species with the Trait
        Effect: Modifies each Player/Species by the Fertile Card
        """
        [player.all_species_trigger_fertile() for player in self.player_sequence]

    def all_species_trigger_long_neck(self) -> None:
        """ Trigger the Long Neck trait of any Species with the Trait
        Effect: Modifies each Player/Species by the Long Neck
        """
        [player.all_species_trigger_long_neck(self.watering_hole) for player in self.player_sequence]

    def all_species_move_fat_food(self) -> None:
        """ Move the stored fat food for each species in each of the player states
        Effect: Modifies each Species by moving any store fat food if it can into the number of food tokens
        """
        [player.all_species_move_fat_food() for player in self.player_sequence]

    def feed(self) -> None:
        """ Perform the Feeding Phase of the Evolution Game, Continue Feeding Until Every Player can no longer feed or
            store food or their are no more tokens on the watering hole
        Effect: Any species in any of the Players in the player_sequence which either feeds or stores food
            or is attacked or has a trait automatically trigger a feeding.
        """
        [self.feed1(player, feeding_choice) for player, feeding_choice in self.player_feeding_sequence_iter]

    def feed1(self, player: Player, feeding_choice: FeedingChoice) -> None:
        """ Applies the feeding choice on this Dealer and the given Player if valid
        Effect: Modifies the Player sequence by feeding the given player
            which will modify the species being fed and can modify any Player/Species in the Game.
        :param player: The player being fed
        :param feeding_choice: The Choice the Player is making
        """
        feeding_choice.apply(self, player)
        evo_print("{}: {}".format(player.player_str, feeding_choice))

    def kick_player(self, player: Player) -> None:
        """ Kick the given Player from the game
        :param player: The Player
        Effect: Modifies the Player Sequence by removing the player
        """
        self.player_sequence.kick_player(player)

    def can_player_feed_or_store(self, player: Player) -> bool:
        """ Can the given Player State attack or store?
        :param player: The Player
        :return: True if the given Player State can attack or store, False otherwise
        """
        return player.can_any_species_feed_or_store(self.player_sequence)

    def can_player_attack_or_store(self, player: Player):
        """ Can the given Player State attack or store?
        :param player: The Player
        :return: True if the given Player State can attack or store, False otherwise
        """
        return player.can_any_species_attack_or_store(self.player_sequence)

    def feed_species(self, species_index: Index, player: Player) -> None:
        """ Feeds the Species at the given index of the given PlayerStates species_list
        Effect: Feeds the Species and modifies any changed species accordingly
        :param species_index: Species Index of the species to be fed
        :param player: Player that owns the species to be fed
        """
        species = player.species_list[species_index]
        species.feed(species_index, player, self.watering_hole)

    def feed_scavengers(self) -> None:
        """ Go through each PlayerState in sequential order and feed each of the Scavengers
        Effect: Modifies each of the Scavengers of Each Player who can feed, Modifies the WateringHole by taking tokens
        for feeding. Also feeds the cooperation chain of any Scavengers.
        """
        [player.feed_scavengers(self.watering_hole) for player in self.player_sequence]

    def get_feeding_choice(self, player: Player) -> OptAutomatedFeedingChoice:
        """ Get the Automate the feeding for the given player state.
        :param player: The Player
        :return: FeedingChoice if the player can feed, otherwise NoAutomatedFeedingChoice
        """
        return player.choose_feeding(self.player_sequence, self.food_on_watering_hole)

    def all_species_reduce_to_fed_population(self) -> None:
        """ Reduce the population of each species of each player to its fed population
        Effect: Modifies each Species with unfed population by reducing its population to its fed population
        """
        [player.all_species_reduce_to_fed_population(self.deck) for player in self.player_sequence]

    def all_players_move_fed_food_to_food_bag(self) -> None:
        """ Move the fed food of each of the Species of each of the Player States
        Effect: Modifies each Species by removing its fed food and moving it to its Player's food bag
        """
        [player.move_fed_food_to_food_bag() for player in self.player_sequence]

    def shuffle_deck(self) -> None:
        """ Shuffles the deck into lexographical order
        Effect: Modifies the deck by putting the cards into lexographical order
        """
        self.deck.order(LexicographicCardKey)

    def deal(self) -> None:
        """ Deal cards to all player and new Species Boards to any player who have none
        Effect: Modifies the hands and can add one species board to each player, and removed cards from the Deck
        """
        self.add_new_species_if_player_has_none()

        player_wanted_list = self.player_cards_wanted_list
        while any((0 < num_wanted_cards) for num_wanted_cards in player_wanted_list):
            self.all_players_draw_card(player_wanted_list)

    def add_new_species_if_player_has_none(self) -> None:
        """ Add a new species to any player who doesn't have any Species
        Effect: Modifies the species list of any Player who doesn't have any Species
        """
        [player.add_new_species_if_has_none() for player in self.player_sequence]

    def all_players_draw_card(self, player_wanted_list: List[Natural]):
        """ Hand a card to each player who still wants a Card
        Effect: Adds a card to each player who wants one
        """
        for player_index, player in enumerate(self.player_sequence):
            player_cards_wanted = player_wanted_list[player_index]
            player_cards_wanted = player.draw_card_if_wanted(self.deck, player_cards_wanted)
            player_wanted_list[player_index] = player_cards_wanted

    @property
    def player_cards_wanted_list(self) -> List[Natural]:
        """ Get the Player Cards want list """
        return [player.num_cards_wanted for player in self.player_sequence]

    def clean_watering_hole(self) -> None:
        """ Clean the Watering Hole by removing all Food Cards
        Effect: Modifies the Watering Hole to have no Food Cards
        """
        self.watering_hole.clean_cards()

    @property
    def is_game_over(self) -> bool:
        """ Is the game over? """
        return (not self.are_there_still_players_in_game) or (not self.are_there_enough_cards_in_deck)

    @property
    def are_there_still_players_in_game(self) -> bool:
        """ Are there no players left in this Game? """
        return NO_PLAYERS_IN_GAME < self.num_players

    @property
    def are_there_enough_cards_in_deck(self) -> bool:
        """ Are there enough cards in the deck to continue playing """
        return self.total_cards_wanted <= self.num_cards_in_deck

    @property
    def num_cards_in_deck(self) -> bool:
        """ Get the number of cards left in the Deck """
        return len(self.deck)

    @property
    def total_cards_wanted(self) -> Natural:
        """ Get the total cards wanted by each of the players combined """
        return sum([player.num_cards_wanted for player in self.player_sequence])

    @property
    def player_sequence(self) -> PlayerSequence:
        """ Get the Sequence of Player States """
        return assert_set(self._player_sequence)

    @player_sequence.setter
    def player_sequence(self, player_sequence: PlayerSequence) -> None:
        """ Set the Sequence of Player States """
        assert_type(player_sequence, of_type=PlayerSequence, func_name="player_sequence")
        self._player_sequence = player_sequence

    @property
    def configuration_sequence_without(self):
        """ Configuration Sequence without the given Player """
        return self.player_sequence.configuration_sequence_without

    def get_player_list_without(self, player: Player) -> List[Player]:
        """ Get the Player List without the given player
        :param player: The Player
        :return: The Player Sequence as a list without the given Player
        """
        return self.player_sequence.get_player_list_without(player)

    def get_player_list_with_player_at_end(self, player: Player) -> List[Player]:
        """ Get the Player List with the given player moved to the end of the list
        :param player: The State of the Player
        :return: The sequence as a list with the player moved to the end of the list
        """
        return self.get_player_list_without(player) + [player]

    @property
    def player_feeding_sequence_iter(self) -> PlayerSequence.PlayerFeedableSequenceIterator:
        """ Get the Feedable Player Sequence Iterator """
        return self.player_sequence.feedable_player_sequence_iter(self)

    @property
    def num_players(self) -> Natural:
        """ Get the number of players in this Configuration """
        return len(self.player_sequence)

    @property
    def watering_hole(self) -> WateringHole:
        """ Get the Watering Hole """
        return assert_set(self._watering_hole)

    @watering_hole.setter
    def watering_hole(self, watering_hole: OptWateringHole) -> None:
        """ Set the Watering Hole """
        if watering_hole == NoWateringHole:
            watering_hole = WateringHole()

        assert_type(watering_hole, of_type=WateringHole, func_name="watering_hole")

        self._watering_hole = watering_hole

    @property
    def food_on_watering_hole(self) -> Natural:
        """ Get the number of food tokens on the Watering Hole """
        return self.watering_hole.num_food_tokens

    @property
    def is_watering_hole_empty(self) -> bool:
        """ Is the watering hole empty? """
        return self.watering_hole.is_empty

    @property
    def deck(self) -> Deck:
        """ Get the Deck of TraitCards """
        return assert_set(self._deck)

    @deck.setter
    def deck(self, deck: Deck) -> None:
        """ Set the Deck of TraitCards """
        deck = Deck() if deck == NoDeck else deck

        assert_type(deck, of_type=Deck, func_name="deck")

        self._deck = deck

    @property
    def player_config_sequence(self) -> List[PlayerConfiguration]:
        """ The Player Configuration Sequence """
        return [player.player_configuration for player in self.player_sequence]

    def split_configuration_sequence(self, player: Player) \
            -> Tuple[List[PlayerConfiguration], List[PlayerConfiguration]]:
        """ Get the Configuration Sequence split in half at the index of the given player without the player
        :param player: The player that the list is split before and after
        :return: The two Configuration Sequences
        """
        return self.player_sequence.split_configuration_sequence(player)

    @property
    def configuration(self) -> Configuration:
        """ Get the Configuration of the Game """
        return Configuration(deepcopy(self.player_sequence), deepcopy(self.watering_hole), deepcopy(self.deck))

    @configuration.setter
    def configuration(self, configuration: Configuration) -> None:
        """ Set the Configuration of the Game"""
        if not is_configuration(configuration):
            raise SetValueError("configuration: Must be a Configuration, got: {}".format(configuration))

        self.player_sequence = deepcopy(configuration.player_sequence)
        self.watering_hole = deepcopy(configuration.watering_hole)
        self.deck = deepcopy(configuration.deck)

    def grab_food_token_from_watering_hole(self) -> Natural:
        """ Grab a food token from the watering hole
        Effect: Modifies the number of tokens the watering hole has
        :return: 1 food token if tokens are on the watering hole, 0 otherwise
        """
        if self.is_watering_hole_empty:
            result = NO_FOOD_TOKENS
        else:
            result = DEFAULT_FOOD_TOKENS_GRABBED

        return self.watering_hole.take_food(result)

    def any_duplicate_cards(self,
                            player_sequence: PlayerSequence = NoPlayerSequence,
                            deck: OptDeck = NoDeck) -> bool:
        """ Does this Configuration have any duplicate TraitCards?
        :param player_sequence: The Player Sequence
        :param deck: The Deck of Cards
        :return: True if there are any duplicates TraitCards in the Configuration, False otherwise
        """
        all_cards = self.get_all_player_sequence_cards(player_sequence)
        all_cards += self.get_all_deck_cards(deck)
        return (any_duplicates(all_cards, lambda x, y: (x == y) and (x.food_card_tokens != NoFoodCardTokens)) or
                Dealer.is_invalid_card_count(all_cards))

    @staticmethod
    def is_invalid_card_count(trait_cards: List[TraitCard]):
        """ Does the given TraitCards list have an invalid number of cards for any type
        :param trait_cards: The TraitCards
        :return: True if there is an invalid card count, False otherwise
        """
        trait_types_cards_list = [type(trait_card) for trait_card in trait_cards]
        return any(not trait_type.is_valid_card_count(trait_types_cards_list.count(trait_type))
                   for trait_type in trait_types_cards_list)

    def get_all_player_sequence_cards(self, player_sequence: OptPlayerSequence = NoPlayerSequence) -> List[TraitCard]:
        """ Get all the cards of the player sequence
        :param player_sequence: The Player sequence
        :return: All the TraitCards of all the players
        """
        player_sequence = self.player_sequence if player_sequence == NoPlayerSequence else player_sequence

        return player_sequence.all_cards

    def get_all_deck_cards(self, deck: OptDeck = NoDeck) -> List[TraitCard]:
        """ Get the deck of cards from either the given deck or self.deck
        :param deck: The optional deck
        :return: The cards in that deck
        """
        deck = self.deck if deck == NoDeck else deck
        return deck.cards

    def reset_forgo_for_all_players(self) -> None:
        """ Reset all the players so they haven't forgon a choice this turn
         Effect: Modfies the has_forgon_this_turn field of each player
         """
        return self.player_sequence.reset_forgo_for_all_players()

    def display(self, display_configuration: Callable[[Configuration], None]) -> None:
        """ Show the Gui of this dealers's configuration
        :param display_configuration: this dealers's configuration
        Effect: Opens up a window showing this dealers's configuration
        """
        display_configuration(self.configuration)

    def print_results(self) -> None:
        """ Print the resulting scores of each player by the number of tokens in their food bag
        Effect: Prints the resulting scores
        """
        player_list = sorted(self.player_sequence.player_list, key=lambda player: player.player_id)
        for index, player in enumerate(player_list):
            print("{} player{} id: {} score: {}".format(index+1, player.name_str, player.player_id, player.food_bag))

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Dealer) and \
               self.player_sequence == cast(Dealer, other).player_sequence and \
               self.watering_hole == cast(Dealer, other).watering_hole and \
               self.deck == cast(Dealer, other).deck

    def __repr__(self) -> str:
        return "Deck({}, {}, {})".format(self.player_sequence,
                                         self.watering_hole,
                                         self.deck)


def any_duplicate_player_ids(player_sequence: PlayerSequence) -> bool:
    """ Are their any duplicate player ids in the given player sequence?
    :param player_sequence: The Player State Sequence
    :return: True if the any Player States have duplicate ids, False otherwise
    """
    return any_duplicates(player_sequence.player_list, lambda x, y: (x.player_id == y.player_id))
