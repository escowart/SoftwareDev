from evolution.messages.player_messages.all_player_messages import *
from evolution.external_players.external_player import *

OptAutomatedFeedingChoice = OptValidFeedingChoice
NoAutomatedFeedingChoice = InvalidFeedingChoice


def player_configs_to_players(player_configs: OptList[PlayerConfiguration] = NoList) -> List['Player']:
    """ Convert the given list of Player Cofigurations into a list of Players
    :param player_configs: The list of Player Configurations
    :return: The resulting list of Players
    """
    if player_configs == NoList:
        return []
    else:
        return [Player(*player_config) for player_config in player_configs]


class Player(IPlayer):
    """ A class representing a Player in the Game which is held by a dealers """

    def __init__(self,
                 player_id:            PlayerId,
                 species_list:         List[Species] = NoList,
                 food_bag:             Natural = PLAYER_STARTING_FOOD_TOKENS,
                 hand:                 OptList[TraitCard] = NoList,
                 external_player_type: type(ExternalPlayer) = NoType,
                 external_player:      OptExternalPlayer = NoExternalPlayer,
                 has_forgon_this_turn: bool = HASNT_FORGON,
                 player_name:          OptStr = NoStr) -> None:
        """ Construct a Player
        :param player_id: The id of the Player
        :param species_list: The Species this Player has in the order they appear on the Board
        :param food_bag: The food bag of the Player which stores the food that the player
        :param hand: The hand of the Player
        """
        self._player_id = Unset              # type: int
        self._species_list = Unset           # type: List[Species]
        self._food_bag = Unset               # type: Natural
        self._hand = Unset                   # type: List[TraitCard]
        self._external_player = Unset        # type: OptExternalPlayer
        self._has_forgon_this_turn = Unset   # type: bool
        self._player_name = Unset            # type: OptStr

        self.player_id = player_id
        self.food_bag = food_bag
        self.species_list = species_list
        self.hand = hand
        self.make_external_player(external_player_type, external_player)
        self.has_forgon_this_turn = has_forgon_this_turn
        self.player_name = player_name

    def call_external_player_method(self,
                                    dealer: OptDealer,
                                    method,
                                    *method_args,
                                    **method_kwargs) -> OptPlayerResponse:
        """ Call the given method on the external player with the given arguments
        :param dealer: The dealers of the game
        :param method: The method being called
        :param method_args: The arguments to the method
        :param method_kwargs: The keyword arguments to the method
        """
        try:
            response = self.call_external_player_method_time_timeout(dealer, method, *method_args, **method_kwargs)
            return response
        except Exception as e:
            self.shut_down()
            return InvalidMessage

    @timeout(SERVER_MESSAGE_TIMEOUT)
    def call_external_player_method_time_timeout(self,
                                                 dealer: OptDealer,
                                                 method,
                                                 *method_args,
                                                 **method_kwargs) -> OptPlayerResponse:
        """ Call the given method on the external player with the given arguments
        :param dealer: The dealers of the game
        :param method: The method being called
        :param method_args: The arguments to the method
        :param method_kwargs: The keyword arguments to the method
        """
        self.give_player_config_to_external_player()

        response = method(*method_args, **method_kwargs)
        if (response != InvalidMessage) and response.is_valid(dealer, self):
            return response
        else:
            return InvalidMessage

    def send_new_player(self) -> bool:
        """ Send the New Player message to the Client, and return whether the message was successfully sent
        Effect: Sends a message over the socket to the Client
        :return: Whether the message was successfully sent
        """
        response = self.call_external_player_method(NoDealer, self.external_player.send_new_player)
        if response == InvalidMessage:
            return False
        else:
            return True

    def start_turn(self, food_on_watering_hole: Natural) -> OptMessage:
        """ Start the Turn by send the external Player their Player's state
        :param food_on_watering_hole: The food on the watering hole
        Effect: Start the Turn by sending the external player this Player's state
        :return: The Message the start_turn return, or Invalid Message
        """
        return self.call_external_player_method(NoDealer, self.external_player.start_turn, food_on_watering_hole)

    def shut_down(self) -> None:
        """ Tell this Player to Shut down and close its socket if it has one
        Effect: Close the socket if it holds a Proxy Player
        :return: The Message the shut_down return, or Invalid Message
        """
        self.call_external_player_method(NoDealer, self.external_player.shut_down)

    def choose_feeding(self, dealer: IDealer) -> OptValidFeedingChoice:
        """ Get the feeding choice of this Player, returns NoFeedingChoice if it cannot feed.
        :param dealer: The dealers of the Game
        :return: The automated Player Feeding Choice if it can be automated,
            NoChoice if no automation is possible
        """
        feeding_choice = self.choose_automated_feeding(dealer)
        if feeding_choice == NoAutomatedFeedingChoice:
            response = self.call_external_player_method(dealer,
                                                        self.external_player.choose_feeding,
                                                        dealer.food_on_watering_hole,
                                                        dealer.configuration_sequence_without(self))

            return InvalidFeedingChoice if response == InvalidMessage else cast(FeedingChoice, response)
        else:
            return feeding_choice

    def choose_action(self, dealer: IDealer) -> OptValidAction:
        """ Tell the external player to choose an Action and return it
        :param dealer: The Dealer of the Game
        :return: Optional Action that this player chose
        """
        first_half, second_half = dealer.split_configuration_sequence(self)
        response = self.call_external_player_method(dealer, self.external_player.choose_action, first_half, second_half)
        return InvalidAction if response == InvalidMessage else cast(Action, response)

    def update(self,
               player_id:    OptPlayerId = NoPlayerId,
               species_list: OptSpecies = NoSpecies,
               food_bag:     OptNatural = NoNatural,
               hand:         OptList[TraitCard] = NoList) -> None:
        """ Update this Player with its field if they are NoValue
        Effect: Updates the Client Player's fields
        :param player_id: The id of Player
        :param species_list: The Species list
        :param food_bag: The food bag of th ePlayer
        :param hand: The hand of the Player
        """
        if player_id != NoPlayerId:
            self.player_id = player_id
        if species_list != NoSpecies:
            self.species_list = species_list
        if food_bag != NoNatural:
            self.food_bag = food_bag
        if hand != NoList:
            self.hand = hand

        self.give_player_config_to_external_player()

    def choose_automated_feeding(self, dealer: IDealer) -> OptAutomatedFeedingChoice:
        """ Get the automated feeding  choice of this Player, returns NoAutomatedFeedingChoice if it cannot be automated
            either because their are no choices available or their are too many choices.
        :param dealer: The dealers of the Game
        :return: The automated Player Feeding Choice if it can be automated,
            NoAutomatedFeedingChoice if no automation is possible
        """
        player_sequence = dealer.player_sequence
        species_index = self.get_only_feeder_index(player_sequence)
        if species_index != NoIndex:
            species_index = cast(Index, species_index)
            species = self.species_list[species_index]

            if species.can_attack(player_sequence) and (not species.can_store_more_fat):
                return NoAutomatedFeedingChoice
            elif species.can_feed_as_vegetarian() and (not species.can_store_more_fat):
                return FeedVegetarianChoice(species_index)
            elif species.can_store_more_fat:
                return StoreFatChoice(species_index, min(species.fat_tissue_need, dealer.food_on_watering_hole))

        return NoAutomatedFeedingChoice

    def feed_scavengers(self, watering_hole: WateringHole) -> None:
        """ Feed the Scavengers of this PlayerState
        Effect: Modifies the Scavengers and the WateringHole by feeding any Scavengers that can feed and any of their
        cooperation Chain
        :param watering_hole: The Watering Hole
        """
        [species.feed(cast(Index, index), self, watering_hole) for index, species in enumerate(self.species_list)
         if species.has_trait(ScavengerCard)]

    def feed_next_species(self, index_of_current_species: Index, watering_hole: WateringHole) -> None:
        """ Feeds the next Species in this Player's species_list if it exists
        Effect: Modifies the next Species if it exists by feeding it and it's cooperation chain
        :param index_of_current_species: The index of current species
        :param watering_hole: The watering hole
        """
        next_index = index_of_current_species + 1  # type: Index

        if self.has_species_at_index(next_index):
            next_species = self.species_list[next_index]
            next_species.feed(next_index, self, watering_hole)

    def get_only_feeder_index(self, player_sequence: IPlayerSequence) -> OptIndex:
        """ Get the Index of the only Feeder-Species
        :param player_sequence: The Player Sequence in the Game
        :return: The Index of the only Feeder, NoIndex if their are either no feeders or more than 1 feeder
        """
        can_feed_list = [species.can_feed_or_store(player_sequence) for species in self.species_list]

        if can_feed_list.count(True) == AUTOMATE_COUNT:
            return can_feed_list.index(True)
        else:
            return NoIndex

    def remove_species_at_index(self,
                                species_index:    Index,
                                deck:             Deck,
                                species_list:     OptList[Species] = NoList) -> None:
        """ Removes the species at given index and draw cards from the deck
        Effect: Removes species from species list and adds cards to hand
        :param species_index: The index of the species being removed
        :param deck: Dealer's deck of cards
        :param species_list: The Species list it could be removed from
        """
        species_int = cast(int, species_index)
        if species_list == NoList:
            self.species_list.pop(species_int)
        else:
            cast(List, species_list).pop(species_int)

        drawn_cards = deck.draw_cards(EXTINCT_DRAW_CARD)
        self.add_to_hand(drawn_cards)

        evo_print("{}: Extinction of Species {}, Draws: {}".format(self.player_str, species_index, drawn_cards))

    def display(self, display_player_configuration: Callable[[PlayerConfiguration], None]) -> None:
        """ Show the gui for this player
        Effect: Opens up a window showing this player's configuration
        :param display_player_configuration: this player's configuration
        """
        display_player_configuration(self.player_configuration)

    def can_be_attacked_by(self, attacker: Carnivore, defender_index: Index) -> bool:
        """ Can the Species at the given defender index within this Player's list of Species be attacked by the given
        Carnivore?
        :param attacker: The attacker
        :param defender_index: The index of the defender
        :return: True if the Carnivore can attack the Species at the index, False otherwise
        """
        left_neighbor, defender, right_neighbor = self.get_species_at_index_with_neighbors(defender_index)
        return defender.is_attackable(attacker, left_neighbor, right_neighbor)

    def all_species_trigger_fertile(self) -> None:
        """ Trigger the Fertile trait of any Species with the Trait
        Effect: Modifies each Player/Species by the Fertile Card
        """
        [species.trigger_fertile() for species in self.species_list]

    def all_species_trigger_long_neck(self, watering_hole: WateringHole) -> None:
        """ Trigger the Long Neck trait of any Species with the Trait
        Effect: Modifies each Species by the Long Neck
        :param watering_hole: The Watering Hole
        """
        [species.trigger_long_neck(cast(Index, species_index), self, watering_hole)
         for species_index, species in enumerate(self.species_list)]

    def all_species_move_fat_food(self) -> None:
        """ Move the stored fat food for each species
        Effect: Modifies each Species by moving any store fat food if it can into the number of food tokens
        """
        [species.move_fat_food() for species in self.species_list]

    def all_species_reduce_to_fed_population(self, deck: Deck) -> None:
        """ Reduce the population of each species of each player to its fed population
        Effect: Modifies each Species with unfed population by reducing its population to its fed population.
                    If any species goes extinct then it is removed from the self.species_list and cards are drawn from
                     the deck.
        :param deck: The deck of the Game
        """
        rem_species_list = rem_list(self.species_list)
        [species.reduce_by_unfed_population(self, cast(Index, index), deck, rem_species_list)
         for index, species in enumerate(rem_species_list)]
        self.species_list = rem_species_list.clean_list

    def move_fed_food_to_food_bag(self) -> None:
        """ Move the fed food of each of the Species of each of the Player States
        Effect: Modifies each Species by removing its fed food and moving it to its Player's food bag
        """
        self.food_bag += sum([species.grab_fed_food() for species in self.species_list])

    def add_new_species_if_has_none(self):
        """ Add a new species to this Player's species_list if it has None
        Effect: Modifies the species list if this has no species"""
        if not self.has_any_species:
            self.species_list.append(Species())

    def draw_card_if_wanted(self, deck: Deck, num_cards_wanted: Natural) -> Natural:
        """ Draw a card if this player wants more cards
        Effect: Removes the Card from the deck and adds it to this Player's hand
        """
        if NO_CARDS_WANTED == num_cards_wanted:
            return num_cards_wanted

        drawn_card = deck.draw_card()
        self.add_to_hand([drawn_card])
        evo_print("{}: Draws {}".format(self.player_str, drawn_card))
        return num_cards_wanted - 1

    @property
    def num_cards_wanted(self) -> NaturalPlus:
        """ Number of cards that this player needs at the beginning of the round """
        return max(self.num_species, NEW_SPECIES_AT_START_OF_TURN) + MINIMUM_HAND_SIZE

    def has_species_at_index(self, species_index: Index) -> bool:
        """ Does this Player have a Species at the given index?
        :param species_index: The index of the species
        :return: True if this has a Species at the index, False otherwise
        """
        return is_index(species_index) and species_index < self.num_species

    def species_at_index_has_trait_at_index(self, species_index: Index, trait_index: Index) -> bool:
        """ Does the Species at the given Index in this Player's species_list have a trait at the given index?
        :param species_index: The index of the Species
        :param trait_index: The index of the Trait
        :return: True if this has a Trait at the index in Species at the index, False otherwise
        """
        species = self.species_list[species_index]
        return species.has_trait_at_index(trait_index)

    @property
    def any_hungry_species(self) -> bool:
        """ Are any of this PlayerState's Species Hungry
        :return: True if there are any hungry species in this PlayerState, False otherwise
        """
        return any(species.is_hungry for species in self.species_list)

    @property
    def any_extinct_species(self) -> bool:
        """ Are there any extinct species in this PlayerState?
        :return: True if there are any extinct Species in this PlayerState
        """
        return any(species.is_extinct for species in self.species_list)

    @property
    def any_hungry_vegetarians(self):
        """ Does this Player have any hungry vegetarians? """
        return any((species.is_hungry and species.is_vegetarian) for species in self.species_list)

    def give_food_to_species(self, species_index: Index, num_food_tokens: Natural) -> None:
        """ Give the num_food_tokens to the PlayerState's Species at the given Index
        Effect: Modifies the species at the given index's number of food tokens accordingly
        :param species_index: The Index of the Species
        :param num_food_tokens: The number of food tokens being handed
        """
        species = self.species_list[species_index]
        species.give_food(num_food_tokens)

    def can_any_species_feed_or_store(self, player_sequence: IPlayerSequence) -> bool:
        """ Can any of this Player's Species be feed or store?
        :param player_sequence: All the Players in the Configuration including this Player
        :return: True if any of the Species of this Player can still feed, False otherwise
        """
        return ((not self.has_forgon_this_turn) and
                any(species.can_feed_or_store(player_sequence) for species in self.species_list))

    def can_any_species_attack_or_store(self, player_sequence: IPlayerSequence) -> bool:
        """ Can any of these Player's Species attack or store fat food?
        :param player_sequence: All the Players in the Configuration including this Player
        :return: True if any of the Species of this Player can attack or store food, False otherwise
        """
        return ((not self.has_forgon_this_turn) and
                any(species.can_attack(player_sequence) or species.can_store_more_fat for species in
                    self.species_list))

    def give_player_config_to_external_player(self) -> None:
        """ Give the external player this Player's Configuration """
        self.external_player.player_configuration = self.player_configuration

    def can_add_to_attribute_of_species_at_index(self,
                                                 species_index:     Index,
                                                 species_attribute: SpeciesAttribute,
                                                 amount_to_add:     Natural) -> bool:
        """ Can the species at the given index add to the given type of attribute?
        :param species_index: The index of the Species
        :param species_attribute: The attribute
        :param amount_to_add: The amount being added to the attribute
        :return: True if the attribute of the species can gain value, False otherwise
        """
        species = self.species_list[species_index]
        return species_attribute.can_add_to_attribute(species, amount_to_add)

    @property
    def player_id(self) -> PlayerId:
        """ Get the Player's id """
        return assert_set(self._player_id)

    @player_id.setter
    def player_id(self, player_id: PlayerId) -> None:
        """ Set the Player's id """
        assert_type(player_id, of_type=PlayerId, func_name="player_id")
        self._player_id = player_id

    @property
    def species_list(self) -> List[Species]:
        """ Get the List of Species in the order they exist on the Board """
        return assert_set(self._species_list)

    @species_list.setter
    def species_list(self, species_list: List[Species] = NoList) -> None:
        """ Get the List of Species in the order they exist on the Board """
        if species_list == NoList:
            species_list = []

        assert_type(species_list, collection_type=list, of_type=Species)
        self._species_list = species_list

    def add_species(self, species: Species) -> None:
        """ Add the given species to this Player State's list of Species
        Effect: Modifies the species_list by adding the given species to the end
        :param species: The Species being added
        """
        self.species_list.append(species)

    @property
    def food_bag(self) -> Natural:
        """ Get the number of Food Tokens in this Player's Food Bag """
        return assert_set(self._food_bag)

    @food_bag.setter
    def food_bag(self, food_bag: Natural) -> None:
        """ Set the number of Food Tokens in this Player's Food Bag """
        assert_type(food_bag, of_type=Natural, func_name="food_bag")
        self._food_bag = food_bag

    @property
    def hand(self) -> List[TraitCard]:
        """ Get this Player's Hand """
        return assert_set(self._hand)

    @hand.setter
    def hand(self, hand: OptList[TraitCard] = NoList) -> None:
        """ Set this Player's Hand """
        if hand == NoList:
            hand = []

        assert_type(hand, collection_type=list, of_type=TraitCard, func_name="hand")
        self._hand = cast(List[TraitCard], hand)

    def add_to_hand(self, cards: List[TraitCard]) -> None:
        """ Add the given cards to this Player's hand
        Effect: Modifies the hand by adding the cards to the front
        :param cards: The cards being added to the hand
        """
        self.hand = cards + self.hand

    @property
    def has_external_player(self) -> bool:
        """ Does this Player have an External Player to communicate with? """
        return self.external_player != NoExternalPlayer

    @property
    def external_player(self) -> OptExternalPlayer:
        """ Get the External Player which is how the Dealer communicates through this Player """
        return assert_set(self._external_player)

    @external_player.setter
    def external_player(self, external_player: OptExternalPlayer) -> None:
        """ Set the External Player which is how the Dealer communicates through this Player """
        if external_player != NoExternalPlayer:
            assert_type(external_player, of_type=ExternalPlayer, func_name="external_player")

        self._external_player = external_player

    def make_external_player(self,
                             external_player_type: type(ExternalPlayer) = NoType,
                             external_player:      OptExternalPlayer = NoExternalPlayer) -> None:
        """ Make or Set the External Player of this Player
        Effect: Modifies this Players external Player
        :param external_player_type: The optional type of external player
        :param external_player: The optional external player
        """
        if external_player != NoExternalPlayer:
            self.external_player = external_player
        elif external_player_type != NoType:
            self.external_player = external_player_type(self.player_id, self.player_configuration)
        else:
            self.external_player = NoExternalPlayer

    @property
    def hand_size(self) -> Natural:
        """ The size of the Player's hand """
        return len(self.hand)

    @property
    def is_hand_empty(self) -> bool:
        """ Is the Player's hand empty? """
        return len(self.hand) == 0

    @property
    def num_species(self) -> Natural:
        """ Get the number of Species """
        return len(self.species_list)

    @property
    def has_any_species(self) -> bool:
        """ Does this Player have at least one Species? """
        return 0 < self.num_species

    @property
    def all_cards(self) -> List[TraitCard]:
        """ Get all the cards in this Player State """
        all_cards = self.hand[:]
        for species in self.species_list:
            all_cards += species.trait_cards
        return all_cards

    @property
    def player_configuration_without_hand_and_bag(self) -> PlayerConfiguration:
        """ Get the Configuration of this Player without its hand for passing this Player to other Players """
        return PlayerConfiguration(self.player_id, deepcopy(self.species_list), NO_FOOD_TOKENS, [])

    @property
    def player_configuration(self) -> PlayerConfiguration:
        """ Get the Configuration of this Player """
        return PlayerConfiguration(self.player_id, deepcopy(self.species_list), self.food_bag, deepcopy(self.hand))

    @player_configuration.setter
    def player_configuration(self, p_config: PlayerConfiguration) -> None:
        """ Set the Configuration of this player"""
        if not is_player_config(p_config):
            raise SetValueError("player_configuration: Must be a PlayerConfiguration, got: {}".format(p_config))

        self.player_id = p_config.player_id
        self.species_list = p_config.species_list
        self.food_bag = p_config.food_bag
        self.hand = p_config.hand

    @property
    def has_forgon_this_turn(self) -> bool:
        """ Has this Player forgon this turn? """
        return assert_set(self._has_forgon_this_turn)

    @has_forgon_this_turn.setter
    def has_forgon_this_turn(self, has_forgon_this_turn: bool) -> None:
        """ Set whether this Player forgon this turn? """
        assert_type(has_forgon_this_turn, of_type=bool, func_name="has_forgon_this_turn")
        self._has_forgon_this_turn = has_forgon_this_turn

    @property
    def player_name(self) -> str:
        """ Get the Player's name """
        return assert_set(self._player_name)

    @player_name.setter
    def player_name(self, player_name: str) -> None:
        """ Set the Player's name """
        assert_type(player_name, of_type=(str, NoStrClass), func_name="player_name")
        self._player_name = player_name

    def get_species_at_index(self, species_index: Index) -> Species:
        """ Get the species at the given index
        :param species_index: The Index of the Species
        :return: The Species at the given IndexOfSpecies or raise IndexError
        """
        return self.species_list[species_index]

    def species_neighbor_iter(self, next_species_index: Index = DEFAULT_START_INDEX) -> SpeciesNeighborIterator:
        """ Get this PlayerState's Species List as an Iterator of its neighbors as well
        :param next_species_index: The next index of the iterator
        :return: The Species List Neighbor Iterator
        """
        return SpeciesNeighborIterator(self.species_list, next_species_index)

    def get_species_at_index_with_neighbors(self, species_index: Index) -> Tuple[OptSpecies, Species, OptSpecies]:
        """ Get the Species at the index with neighbors
        :param species_index: The index of the Species
        :return: The left neighbor, the species, the right neighbor
        """
        species_iter = self.species_neighbor_iter(species_index)
        return next(species_iter)

    def get_ordered_hand(self, key: type(OrderedKey)) -> List[TraitCard]:
        """ Returns an ordered version of this Player's hand
        :param key: The key that determines the order of the hand
        :return: An ordered version of this Player's hand
        """
        ordered_hand = sorted(self.hand[:], key=key)
        ordered_hand.reverse()
        return ordered_hand

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Player) and \
               self.player_id == cast(Player, other).player_id and \
               self.species_list == cast(Player, other).species_list and \
               self.food_bag == cast(Player, other).food_bag and \
               self.hand == cast(Player, other).hand

    def __repr__(self) -> str:
        return "{}({}, {}, {}, {})".format(name_of_class(self),
                                           self.player_id,
                                           self.species_list,
                                           self.food_bag,
                                           self.hand)

    def deep_copy(self) -> 'Player':
        """ Construct a deep copy of this player without the external player
        :return: The new copy of this Player
        """
        return Player(deepcopy(self.player_id),
                      deepcopy(self.species_list),
                      deepcopy(self.food_bag),
                      deepcopy(self.hand))

    @property
    def player_str(self) -> str:
        """ The Player string """
        return "\t\tPlayer {}".format(self.player_id)

    @property
    def name_str(self) -> str:
        """ The Player name str """
        if self.player_name == NoStr:
            return ""
        return ", {}, ".format(self.player_name)
