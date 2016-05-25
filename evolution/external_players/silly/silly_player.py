from evolution.card_holders.lexicographic_card_key import *
from evolution.external_players.abs_external_player import *
from evolution.external_players.silly.silly_species_keys import *


class SillyPlayer(AbsExternalPlayer):
    """ A class representing the Silly Player which preforms a simple strategy """

    def choose_action(self,
                      before_players: List[PlayerConfiguration],
                      after_players: List[PlayerConfiguration]) -> OptValidAction:
        """ Choose an Action based off of the list of before and after players
        :param before_players: The list of players whose turns preceded this player
        :param after_players: The list of players whose turns are after this player
        :return: Optional Action that this player chose
        """
        self.validate_choose_action(before_players, after_players)
        ordered_hand = self.ordered_hand

        food_card_choice = self.get_food_card_choice(ordered_hand)
        gain_board_choice = self.get_gain_board_choice(ordered_hand)  # type: List[GainBoard]
        gain_pop_list, gain_body_list = self.get_grow_species_choice(ordered_hand)
        replace_trait_choices = []  # type: List[ReplaceTrait]
        
        if EMPTY_LIST_LEN < len(ordered_hand):
            replace_trait_choices.append(self.get_replace_trait_choice(ordered_hand))

        return Action(food_card_choice, gain_pop_list, gain_body_list, [gain_board_choice], replace_trait_choices)

    def get_food_card_choice(self, ordered_hand: List[TraitCard]) -> FoodCardChoice:
        """ Get the FoodCardChoice
        Effect: Pops off the first card in the ordered hand
        :param ordered_hand: This player's ordered hand
        :return: The FoodCardChoice
        """
        index = self.get_next_index_in_hand(ordered_hand)
        return FoodCardChoice(index)

    def get_gain_board_choice(self, ordered_hand: List[TraitCard]) -> GainBoard:
        """ Get a List of GainBoard
        Effect: Pops off cards in the ordered hand
        :param ordered_hand: This player's ordered hand
        :return: The GainBoard choice
        """
        board_index = self.get_next_index_in_hand(ordered_hand)
        trait_index = self.get_next_index_in_hand(ordered_hand)
        return GainBoard(board_index, [trait_index])

    @property
    def species_grow_list(self) -> List[GrowSpecies]:
        """ Get the Grow List for all species """
        grow_list = []
        species_index = len(self.own_species_list)
        grow_list.append(GrowSpecies(species_index, GainPopulation))
        grow_list.append(GrowSpecies(species_index, GainBody))

        return grow_list

    def get_grow_species_choice(self, ordered_hand: List[TraitCard]) -> Tuple[List[GainPopulation], List[GainBody]]:
        """ Get the List of GainPopulation and GainBody Choices
        Effect: Pops off cards in the ordered hand
        :param ordered_hand: This player's ordered hand
        :return: A tuple of the list of GainPopulation and list of GainBody Choices
        """
        gain_pop_list = []
        gain_body_list = []
        for grow_species in self.species_grow_list:
            if EMPTY_LIST_LEN == len(ordered_hand):
                break

            card_index = self.get_next_index_in_hand(ordered_hand)

            if grow_species.gain_type == GainPopulation:
                gain_pop_list.append(GainPopulation(grow_species.species_index, card_index))
            if grow_species.gain_type == GainBody:
                gain_body_list.append(GainBody(grow_species.species_index, card_index))

        return gain_pop_list, gain_body_list

    def get_replace_trait_choice(self, ordered_hand: List[TraitCard]) -> ReplaceTrait:
        """ Get ReplaceTrait choice
        Effect: Pops off cards in the ordered hand
        :param ordered_hand: This player's ordered hand
        :return: The ReplaceTrait Choice
        """
        trait = self.get_next_index_in_hand(ordered_hand)
        species_index = self.player.num_species
        return ReplaceTrait(species_index, DEFAULT_START_INDEX, trait)

    def validate_choose_action(self,
                               before_players: List[PlayerConfiguration],
                               after_players: List[PlayerConfiguration]) -> bool:
        """ Checks whether or not this player can choose an action
        :param before_players: The list of players whose turns preceded this player
        :param after_players: The list of players whose turns are after this player
        :return: True if this player can choose an action
        """
        if self.hand_size < MINIMUM_HAND_SIZE:
            raise ValueError("choose_action: This player doesn't have enough cards to choose an action")
        if not is_list(before_players, of_type=PlayerConfiguration):
            raise ValueError("choose_action: before_players isn't a list of PlayerConfiguration")
        if not is_list(after_players, of_type=PlayerConfiguration):
            raise ValueError("choose_action: after_players isn't a list of PlayerConfiguration")
        return

    def choose_feeding(self,
                       num_tokens_on_watering_hole: Natural,
                       other_players=List[PlayerConfiguration]) -> OptValidFeedingChoice:
        """ Choose the next species for this external_players to feed. Must have at least 2 choices for feedings.
        :param num_tokens_on_watering_hole: the number of tokens on the watering hole
        :param other_players: the states of the other players in the game
        :return: The Feeding Choice that this Silly Player
        """
        self.validate_choose_feeding(num_tokens_on_watering_hole, other_players)

        other_players = [Player(*player_config) for player_config in other_players]
        best_species_key = self.best_species_key(other_players)

        if best_species_key == NoOrderedKey:
            return InvalidFeedingChoice
        else:
            best_species_key = cast(SimpleSpeciesOrderedKey, best_species_key)

        best_species = best_species_key.species
        best_species_index = self.index_of_own_species(best_species)
        best_species_feed_type = best_species_key.feed_type

        if best_species_feed_type is SpeciesFeedType.STORE_FAT:
            return StoreFatChoice(best_species_index, min(best_species.fat_tissue_need, num_tokens_on_watering_hole))
        elif best_species_feed_type is SpeciesFeedType.FEEDABLE_VEG:
            return FeedVegetarianChoice(best_species_index)
        elif best_species_feed_type is SpeciesFeedType.FEEDABLE_CARN:
            return self.choose_target(best_species_index, other_players)
        elif best_species_feed_type is SpeciesFeedType.FORGO_ATTACK:
            return ForgoChoice()
        else:
            return InvalidFeedingChoice

    def validate_choose_feeding(self,
                                num_tokens_on_watering_hole: Natural,
                                other_players=List[PlayerConfiguration]) -> None:
        """ Validate the choose feeding arguments and raise an exception if they are bad
        :param num_tokens_on_watering_hole: The number of tokens on the watering hole
        :param other_players: The other players in the game
        :raises: ValueError if invalid data
        """
        assert_type(num_tokens_on_watering_hole, of_type=Natural, func_name="num_tokens_on_watering_hole")
        assert_type(other_players, list, of_type=PlayerConfiguration, func_name="other_players")

        if self.num_species < 1:
            raise ValueError("choose_feeding: Cannot make choice; this player has no species.")

        return

    def best_species_key(self, other_players: List[Player]) -> OptOrderedKey[Species]:
        """ Get the Best Species Key of this Player's Species given the other players in the game
        :param other_players: The other Players in the game
        :return: The best Species Key
        """
        return max([SimpleSpeciesOrderedKey(species, self.player, other_players) for species in self.own_species_list],
                   default=NoOrderedKey)

    def has_best_species_key(self, other_players: List[IPlayer]) -> bool:
        """ Does this Silly Player have a Best Species Key?
        :param other_players: The other players in the game
        :return: True if this has a best species key , False otherwise
        """
        return self.best_species_key(other_players) != NoOrderedKey

    def best_species(self, other_players: List[IPlayer]) -> OptSpecies:
        """ Get the Best Species given the other_players in the Game
        :param other_players: The other players
        :return: The Best Species or NoSpecies
        """
        if self.has_best_species_key(other_players):
            return cast(SimpleSpeciesOrderedKey, self.best_species_key(other_players))
        else:
            return NoSpecies

    def choose_target(self, carn_index: Index, player_states=List[IPlayer]) -> AttackWithCarnivoreChoice:
        """ Choose the target of this Silly Player's Carnivore at the given index in this Silly Player's species boards
        :param carn_index: The index of the attacking Carnivore in this Silly Player's species boards
        :param player_states: the other players in the game
        :return: The attack that the aforementioned Carnivore will execute
        """
        carn_species = self.own_species_list[carn_index]
        best_player_index = NoIndex      # type: Index
        best_species_index = NoIndex     # type: Index
        best_species_key = NoOrderedKey  # type: SimpleSpeciesOrderedKey

        for player_index, player_state in enumerate(player_states):
            player_best_order_key_index = carn_species.best_attack_on_player(player_state, species_order_key)
            if ((player_best_order_key_index != NoOrderedKeyWithIndex) and
                    ((best_species_key == NoOrderedKey) or (player_best_order_key_index.opt_key > best_species_key))):
                best_player_index = player_index
                best_species_index = player_best_order_key_index.index
                best_species_key = player_best_order_key_index.key

        if (best_player_index == NoIndex) or (best_species_index == NoIndex):
            raise UnsetValueError("choose_target: Given carnivore had no valid target among players.")

        return AttackWithCarnivoreChoice(carn_index, best_player_index, best_species_index)

    @staticmethod
    def from_species(species_list: List[Species], player_id: NaturalPlus = DEFAULT_ID) -> 'SillyPlayer':
        """ Create an example external_players from this given species
        :param species_list: The Species of the new Silly Player
        :param player_id: The id of the Player
        :return: A Silly Player with the given species
        """
        return SillyPlayer(player_id, PlayerConfiguration(player_id, species_list, NO_FOOD_TOKENS, []))

    def __repr__(self):
        return "SillyPlayer({})".format(self.player)

    def __eq__(self, other):
        return isinstance(other, SillyPlayer) and \
               self.player_state == cast(SillyPlayer, other).player