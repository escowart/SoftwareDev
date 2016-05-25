from evolution.species.sit_species import *

'''--------------Species--------------'''

Carnivore = 'Species'  # has_trait(CarnivoreCard)

Vegetarian = 'Species'  # not has_trait(CarnivoreCard)

FatSpecies = 'Species'  # has_trait(FatTissueCard)


def make_opt_sit_species(opt_species: OptSpecies, situation_position: SituationFlag) -> OptSituationSpecies:
    """ Make an OptSituationSpecies """
    if opt_species == NoSpecies:
        return NoSituationSpecies
    else:
        return SituationSpecies(cast(Species, opt_species), situation_position)


class Species(ISpecies):
    """ A Species owned by a Player with has Traits """

    def __init__(self,
                 fed_food: Natural = SPECIES_START_FOOD,
                 body_size:       Natural = SPECIES_START_BODY_SIZE,
                 population:      Natural = SPECIES_START_POP,
                 played_cards:    OptList[PlayedCard] = NoList) -> None:
        """ Construct a Species
        :param fed_food: The Number of Food Tokens this Species has been fed this Turn
        :param population: The population of the Species
        :param body_size: The Body Size of the Species
        :param played_cards: The Played cards of the Species
        """
        self._fed_food = Unset  # type: Natural
        self._population = Unset           # type: Natural
        self._body_size = Unset            # type: Natural
        self._played_cards = Unset         # type: List[PlayedCard]

        self.population = population  # DO NOT MOVE: population must be called before num_food_tokens
        self.fed_food = fed_food
        self.body_size = body_size
        self.played_cards = played_cards

    @property
    def is_species(self) -> bool:
        """ Is this OptSpecies a Species? """
        return True

    @property
    def fed_food(self) -> Natural:
        """ Get the number of food tokens fed """
        return assert_set(self._fed_food)

    @fed_food.setter
    def fed_food(self, fed_food: Natural) -> None:
        """ Set the number of food tokens fed """
        assert_type(fed_food, of_type=Natural, max_value=self.population, func_name="fed_food")
        self._fed_food = fed_food

    def grab_fed_food(self) -> Natural:
        """ Grab the food tokens from this Species
        Effect: Modifies fed_food to have no food
        """
        grabbed_food = self.fed_food
        self.fed_food = NO_FOOD_TOKENS
        return grabbed_food

    @property
    def population(self) -> Natural:
        """ Get the population of this Species """
        return assert_set(self._population)

    @population.setter
    def population(self, population: int) -> None:
        """ Set the population of this Species, Any population less than the extinction limit is set the extinction
            value.
        Effect: Modifies the num_food_tokens to population if it exceeds the new population
        """
        assert_type(population, of_type=int, max_value=SPECIES_MAX_POP, func_name="population")

        if population <= SPECIES_EXTINCTION_POP:
            population = SPECIES_EXTINCTION_POP

        self._population = population
        self.adjust_food_to_population()

    def adjust_food_to_population(self) -> None:
        """ Effect: Adjust the num_food_tokens to be equal to the population if it is greater """
        if (self._fed_food != Unset) and (self.population < self.fed_food):
            self.fed_food = self.population

    @property
    def body_size(self) -> Natural:
        """ Get the body size of this Species """
        return assert_set(self._body_size)

    @body_size.setter
    def body_size(self, body_size: Natural) -> None:
        """ Set the body_size of this Species """
        assert_type(body_size, of_type=Natural, min_value=SPECIES_MIN_BODY_SIZE, max_value=SPECIES_MAX_BODY_SIZE,
                    func_name="body_size")
        self._body_size = body_size

    @property
    def played_cards(self) -> List[PlayedCard]:
        """ Get the played cards on this Species """
        return assert_set(self._played_cards)

    @played_cards.setter
    def played_cards(self, played_cards: OptList[PlayedCard] = NoList) -> None:
        """ Set the played cards on this Species """
        if played_cards == NoList:
            played_cards = []

        assert_type(played_cards, collection_type=list, of_type=PlayedCard, func_name="played_cards",
                    coll_max_len=SPECIES_MAX_TRAITS_PER_SPECIES)

        played_cards_list = cast(List[PlayedCard], played_cards)

        if any_duplicates(flip_all(played_cards_list), type_comparator):
            raise SetValueError("played_cards: Cannot Have Trait Duplicates, got: {}".format(played_cards))

        self._played_cards = played_cards_list

    @property
    def trait_cards(self) -> List[ITraitCard]:
        """ Get the currently active traits of this Species """
        return [played_card for played_card in self.played_cards if isinstance(played_card, ITraitCard)]

    def has_trait(self, trait_type: type(ITraitCard)) -> bool:
        """ Does this Species have the a Trait Card of the given type?
        :param trait_type: The Trait Card type
        :return: True if this has a Trait Card of the given type, False otherwise
        """
        return does_list_contain(self.trait_cards, trait_type, of_type_comparator)

    @property
    def num_traits(self) -> Natural:
        """ Get the number of traits of this Species """
        return len(self.trait_cards)

    def has_trait_at_index(self, trait_index: Index) -> bool:
        """ Does this Species have a trait at the given index?
        :param trait_index: The index of the Trait
        :return: True if this has a Trait at the given Index, False otherwise
        """
        return is_index(trait_index) and trait_index < self.num_traits

    @property
    def any_traits(self) -> bool:
        """ Does this Species have any traits? """
        return self.num_traits > 0

    def get_card_at_index(self, index_on_board: Index) -> PlayedCard:
        """ Get the Card at the given index on the Species Board
        :param index_on_board: The index on the Species Board
        :return: The Card at the given index on the Species Board
        """
        return self.played_cards[index_on_board]

    @property
    def number_of_cards(self) -> Natural:
        """ Get the Number of Cards on the Board  """
        return len(self.played_cards)

    @property
    def max_number_of_cards_allowed(self) -> Natural:
        """ Get the Maximum Number of Cards Allowed """
        return SPECIES_MAX_TRAITS_PER_SPECIES

    @property
    def has_fat_tissue(self):
        """ Is the given value a Fat Species? """
        return self.has_trait(FatTissueCard)

    @property
    def fat_tissue(self) -> FatTissueCard:
        """ Get the Fat Tissue of this Species """
        for trait_card in self.trait_cards:
            if type(trait_card) == FatTissueCard:
                return trait_card

        raise ValueError("fat-tissue: No Fat Tissue")

    @property
    def stored_fat_food(self) -> Natural:
        """ Get the Number of Stored Fat Food Tokens """
        return self.fat_tissue.stored_food

    @stored_fat_food.setter
    def stored_fat_food(self, stored_fat_food: Natural) -> None:
        """ Set the Number of Stored Fat Food Tokens """
        if not (is_natural(stored_fat_food) and stored_fat_food <= self.body_size):
            raise SetValueError("stored_fat_food: Must be int between {} and {}.".format(SPECIES_MIN_BODY_SIZE,
                                                                                         self.body_size))

        self.fat_tissue.stored_food = stored_fat_food

    @property
    def has_stored_food(self) -> bool:
        """ Does this Species have stored food? """
        return self.has_fat_tissue and (self.stored_fat_food > 0)

    @property
    def can_store_more_fat(self) -> bool:
        """ Can this species store food in its fat? """
        return self.has_fat_tissue and (self.fat_tissue_need > 0)

    @property
    def movable_stored_fat_food(self) -> Natural:
        """ Get the amount of movable stored fat food """
        return min(self.population, self.stored_fat_food) - self.fed_food

    def move_fat_food(self) -> None:
        """ Move as fat-tissue food tokens as much fat tissue as this species can to the number of food tokens
        Effect: Removes amount of tokens in fat_tissue and moves it into num_food_tokens,
            does nothing if this species has no fat tissue
        """
        if self.has_fat_tissue:
            movable_fat_food = self.movable_stored_fat_food
            if movable_fat_food > 0:
                self.fed_food += movable_fat_food
                self.stored_fat_food -= movable_fat_food

    def can_store(self, fat_to_store: Natural) -> bool:
        """ Can the given amount of food be stored as Fat Tissue?
        :param fat_to_store: The fat to store
        :return: True if this Species can store the given amount of food, False otherwise
        """
        return (self.can_store_more_fat and (fat_to_store > 0) and
                (self.body_size >= (self.stored_fat_food + fat_to_store)))

    def store_fat(self, fat_to_store: Natural) -> None:
        """ Store the given amount of Fat in your Fat Tissue
        :param fat_to_store: The Fat to Store
        """
        self.stored_fat_food += fat_to_store

    @property
    def fat_tissue_need(self) -> Natural:
        """ The Fat Tissue Need of this Species"""
        return self.body_size - self.fat_tissue.stored_food

    @property
    def is_extinct(self) -> bool:
        """ Is this Species Extinct? """
        return self.population <= SPECIES_EXTINCTION_POP

    @property
    def is_extant(self) -> bool:
        """ Is this Species extant? """
        return not self.is_extinct

    @property
    def is_hungry(self) -> bool:
        """ Is this Species hungry? """
        return self.fed_food < self.population

    @property
    def is_carnivore(self) -> bool:
        """ Is this Species a Carnivore? """
        return self.has_trait(CarnivoreCard)

    @property
    def is_vegetarian(self) -> bool:
        """ Is this Species a Vegetarian? """
        return not self.is_carnivore

    @property
    def num_tokens_per_feed(self) -> Natural:
        """ How many tokens does this Species get per feeding """
        if self.has_trait(ForagingCard):
            return NUM_TOKENS_FOR_FORAGING_FEED
        else:
            return NUM_TOKENS_FOR_NORMAL_FEED

    @property
    def unfed_population(self) -> Natural:
        """ How many members of this species remain unfed """
        return self.population - self.fed_food

    @property
    def food_wanted(self) -> Natural:
        """ How much food does this Species want? """
        return min(self.num_tokens_per_feed, self.unfed_population)

    @property
    def is_done_feeding(self) -> bool:
        """ Is this Species done feeding? """
        return not self.is_hungry

    def give_food(self, food_added: Natural) -> None:
        """ Give the food to this Species
        :param food_added: The amount of food added
        """
        self.fed_food += food_added

    def can_feed_or_store(self, player_sequence: IPlayerSequence) -> bool:
        """ Can this species feed or store food?
        :param player_sequence: The Player Sequence
        :return: True if the Species can either feed or store food, False otherwise
        """
        return self.can_store_more_fat or self.can_feed(player_sequence)

    def can_feed(self, player_sequence: IPlayerSequence) -> bool:
        """ Can this Species feed given the Players in the game?
        :param player_sequence: The Player Sequence
        :return: True if this Species can feed, False otherwise
        """
        return self.can_feed_as_vegetarian() or self.can_attack(player_sequence)

    def can_feed_as_vegetarian(self) -> bool:
        """ Can this Species feed as a Vegetarian?
        :return: True if this can feed as a Vegetarian, False otherwise
        """
        return self.is_hungry and self.is_vegetarian

    def can_attack(self, player_sequence: IPlayerSequence) -> bool:
        """ Can this Species attack any Species of the given Player State's species_list ?
        :param player_sequence: The Player Sequence
        :return: True if this can attack anything but itself, False otherwise
        """
        return (self.is_hungry and self.is_carnivore and
                any(self.can_attack_player(player_state) for player_state in player_sequence))

    def feed(self, index_of_self: Index, player_state: IPlayer, watering_hole: WateringHole) -> None:
        """ Feed this Species which is at the given index within the given PlayerState
            and feed any in this Species's Cooperation Chain.
        Effect: Modifies this Species and any other species that are affected by its feeding
        :param index_of_self: The index of this Species
        :param player_state: The Player State
        :param watering_hole: The Watering Hole
        """
        grabbed_food = 0
        while (not watering_hole.is_empty) and (grabbed_food < self.food_wanted):
            grabbed_food += watering_hole.take_food(DEFAULT_FOOD_TOKENS_GRABBED)

        self.give_food(grabbed_food)

        for i in range(grabbed_food):
            if not watering_hole.is_empty and self.has_trait(CooperationCard):
                player_state.feed_next_species(index_of_self, watering_hole)

    def is_attackable(self,
                      attacker: 'Carnivore',
                      defenders_left_neighbor: OptSpecies = NoSpecies,
                      defenders_right_neighbor: OptSpecies = NoSpecies) -> bool:
        """ Can the given attacker attack the given defender given the defender's left and right neighbors?
        :param attacker:                 The attacking Carnivore
        :param defenders_left_neighbor:  The defender's left neighbor
        :param defenders_right_neighbor: The defender's right neighbor
        :return: True if the defender is attackable by the attacker, False otherwise
        """
        return not ((self is attacker) or attacker.is_vegetarian or
                    self._attacks_blocked(attacker, defenders_left_neighbor, defenders_right_neighbor))

    def can_attack_player(self, player_state: 'IPlayer') -> bool:
        """ Can this species attack any of the opponent's species as given in the list, assuming this is a Carnivore
        :param player_state: The State of the Player being attacked
        :return: True if this species can attack one or more of the given species, false otherwise
        """
        return self.best_attack_on_player(player_state, PseudoOrderedKey) != NoOrderedKeyWithIndex

    def best_attack_on_player(self, player_state: 'IPlayer', key_type: type(OrderedKey)) -> OptOrderedKeyWithIndex:
        """ Gets the best attack attack this species can manage on the given list of a external_players's species
        :param player_state: The State of the Player being attacked
        :param key_type: The key used to compare the species, greater than is better
        :return: The Optional Order
        """
        best_species_key = NoOrderedKey
        best_species_index = NoIndex

        for index, (left_neighbor, next_species, right_neighbor) in enumerate(player_state.species_neighbor_iter()):

            if next_species.is_attackable(self, left_neighbor, right_neighbor):
                cur_species_key = key_type(next_species)

                if (best_species_key == NoOrderedKey) or (cur_species_key > best_species_key):
                    best_species_index = index
                    best_species_key = cur_species_key

        return OptOrderedKeyWithIndex(best_species_key, cast(Index, best_species_index))

    def _attacks_blocked(self,
                         attacker: 'Carnivore',
                         defenders_left_neighbor: OptSpecies = NoSpecies,
                         defenders_right_neighbor: OptSpecies = NoSpecies) -> bool:
        """ Are attacks from the given attacker blocked by given defender or by the defender's left and right neighbors?
        :param attacker:                 The attacking Carnivore
        :param defenders_left_neighbor:  The defender's left neighbor
        :param defenders_right_neighbor: The defender's right neighbor
        :return: True if the defender is unattackable by the attacker, False otherwise
        """
        return any(Species._any_traits_blocks_attacks(self,
                                                      attacker,
                                                      defenders_left_neighbor,
                                                      defenders_right_neighbor,
                                                      owner_flag)
                   for owner_flag in SituationFlag)

    @staticmethod
    def _any_traits_blocks_attacks(defender: 'Species',
                                   attacker: 'Carnivore',
                                   defenders_left_neighbor: OptSpecies = NoSpecies,
                                   defenders_right_neighbor: OptSpecies = NoSpecies,
                                   owner_flag: SituationFlag = SituationFlag.DEFENDER) -> bool:
        """ Are attacks from the given attacker blocked by the traits of flagged owner
        :param defender:                 The defending Species
        :param attacker:                 The attacking Carnivore
        :param defenders_left_neighbor:  The defender's left neighbor
        :param defenders_right_neighbor: The defender's right neighbor
        :param owner_flag:               The flag which tells you whose traits are being looked at for blocking
        :return: True if the defender is unattackable by the attacker given the flagged owner's traits, False otherwise
        """
        owner_opt_species = Species.get_owner_species(defender,
                                                      attacker,
                                                      defenders_left_neighbor,
                                                      defenders_right_neighbor,
                                                      owner_flag)

        if owner_opt_species == NoSpecies:
            return False
        else:
            owner_species = cast(Species, owner_opt_species)
            sit_defender = SituationSpecies(defender, SituationFlag.DEFENDER)
            sit_attacker = SituationSpecies(attacker, SituationFlag.ATTACKER)
            sit_dfn_left_neighbor = make_opt_sit_species(defenders_left_neighbor, SituationFlag.DEFENDER_L_NEIGHBOR)
            sit_dfn_right_neighbor = make_opt_sit_species(defenders_right_neighbor, SituationFlag.DEFENDER_R_NEIGHBOR)
            
            return any(trait.blocks_attack(sit_defender, sit_attacker, sit_dfn_left_neighbor, sit_dfn_right_neighbor,
                                           owner_flag)
                       for trait in owner_species.trait_cards)

    def attack(self,
               owner_player:   'IPlayer',
               index_of_self:   Index,
               target_player:  'IPlayer',
               index_of_target: Index,
               deck: Deck) -> None:
        """ Have this Carnivore attack the Species at the given index within the target PlayerState
        Effect: Modifies the target species's attributes or its own attributes if the target has horns
        :param owner_player: owner of this species
        :param index_of_self: where this species is in its external_players's species list
        :param target_player: target species's owner
        :param index_of_target: where the target species is in its owner's list
        :param deck: The deck of cards the dealers holds
        """
        if self.is_vegetarian:
            raise ValueError("attack: Only Carnivores may Attack")

        target_species = target_player.species_list[index_of_target]

        target_species.reduce_population(DEFAULT_DAMAGE, target_player, index_of_target, deck)

        if target_species.has_trait(HornCard):
            self.reduce_population(DEFAULT_DAMAGE, owner_player, index_of_self, deck)

    def reduce_population(self,
                          damage:               NaturalPlus,
                          owner:                IPlayer,
                          index_of_self:        Index,
                          deck:                 Deck,
                          species_list:         OptList['Species'] = NoList) -> None:
        """ Reduces this species population by given amount of damage.
            If this species goes extinct from the damage,
                then the species is removed from its Player State's species_list and Player State draws cards
        Effect: Modifies this species by reducing it population by the given amount,
                 and the number of food tokens this species holds to be no greater than the population
                If this species goes extinct,
                    then its Player State is Modified by removing this Species from its species_list
                     and the deck is Modified by removing cards to put in the Player State's hand
        :param damage: Amount of damage received
        :param owner: The owner PlayerState of this species
        :param index_of_self: The index of this species in its owning Player's species_list
        :param deck: The deck of cards the dealers holds
        :param species_list: The Species OptList being iterated over
        """
        self.population -= damage

        if self.is_extinct:
            if species_list == NoList:
                owner.remove_species_at_index(index_of_self, deck)
            else:
                owner.remove_species_at_index(index_of_self, deck, species_list)

    def reduce_by_unfed_population(self,
                                   owner:                IPlayer,
                                   index_of_self:        Index,
                                   deck:                 Deck,
                                   species_list:         IList['Species']) -> None:
        """ Reduces this species population to match its number of food tokens.
            If this species goes extinct from the damage,
                then the species is removed from its Player State's species_list and Player State draws cards
        Effect: Modifies this species by reducing it population by the given amount
                If this species goes extinct,
                    then its Player State is Modified by removing this Species from its species_list
                     and the deck is Modified by removing cards to put in the Player State's hand
        :param owner: The owner PlayerState of this species
        :param index_of_self: The index of this species in its owning Player's species_list
        :param deck: The deck of cards the dealers holds
        :param species_list: The Species List being iterated over
        """
        self.reduce_population(self.unfed_population, owner, index_of_self, deck, species_list)

    def trigger_fertile(self) -> None:
        """ Trigger the Fertile trait of any Species with the Trait
        Effect: Add population to this Species
        """
        if self.has_trait(FertileCard) and self.population < SPECIES_MAX_POP:
            self.population += FERTILE_POP_INCREASE

    def trigger_long_neck(self, index_of_self: Index, player_state: 'IPlayer',
                          watering_hole: WateringHole) -> None:
        """ Trigger Long Neck by feeding this Species which is at the given index within the given PlayerState
            and feed any in this Species's Cooperation Chain.
        Effect: Modifies this Species and any other species that are affected by its feeding
        :param index_of_self: The index of this Species
        :param player_state: The Player State
        :param watering_hole: The Watering Hole
        """
        if self.has_trait(LongNeckCard):
            self.feed(index_of_self, player_state, watering_hole)

    @staticmethod
    def get_owner_species(defender: 'Species',
                          attacker: 'Carnivore',
                          defenders_left_neighbor: OptSpecies = NoSpecies,
                          defenders_right_neighbor: OptSpecies = NoSpecies,
                          owner_flag: SituationFlag = None) -> OptSpecies:
        """ Get the owner corresponding to the owner_flag given all participants
        :param defender:                 The defending Species
        :param attacker:                 The attacking Carnivore
        :param defenders_left_neighbor:  The defender's left neighbor
        :param defenders_right_neighbor: The defender's right neighbor
        :param owner_flag:               The flag which tells you whose traits are being looked at for blocking
        :return: The owner Species or None if no valid owner
        """
        if owner_flag is SituationFlag.ATTACKER:
            return attacker
        elif owner_flag is SituationFlag.DEFENDER:
            return defender
        elif owner_flag is SituationFlag.DEFENDER_L_NEIGHBOR:
            return defenders_left_neighbor
        elif owner_flag is SituationFlag.DEFENDER_R_NEIGHBOR:
            return defenders_right_neighbor
        else:
            return NoSpecies

    @staticmethod
    def is_extant_species(value: Any) -> bool:
        """ Is the given value a valid extant Species
        :param value: The value being checked
        :return: True if the value is a valid and extant, False otherwise
        """
        return isinstance(value, Species) and cast(Species, value).is_extant

    @staticmethod
    def is_extant_carnivore(value: Any) -> bool:
        """ Is the given value a valid extant Carnivore
        :param value: The value being checked
        :return: True if the value is a valid and extant, False otherwise
        """
        return Species.is_extant_species(value) and cast(Species, value).is_carnivore

    @staticmethod
    def is_opt_extant_species(value: Any) -> bool:
        """ Is the given value a valid extant Optional Species
        :param value: The value being checked
        :return: True if the value is a valid and extant, False otherwise
        """
        return (value == NoSpecies) or Species.is_extant_species(value)

    def __eq__(self, other):
        return isinstance(other, Species) and \
               self.fed_food == cast(Species, other).fed_food and \
               self.population == cast(Species, other).population and \
               self.body_size == cast(Species, other).body_size and \
               self.trait_cards == cast(Species, other).trait_cards

    def __repr__(self):
        return "Species(fed={},body={},pop={},traits={})".format(self.fed_food, self.body_size,
                                                                 self.population, self.trait_cards)
