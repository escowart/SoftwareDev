import unittest

from evo_tests.examples.all_examples import *


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.ex_players = ExampleSillyPlayers()
        self.ex_client_players = ExamplePlayer()
        self.ex_species = ExampleSpecies()

    def test_choose_fat_veg_carn(self):
        # Choosing Fat Species before Vegetarian
        player_fat_veg = self.ex_players.fat_and_burr_veg

        self.assertEqual(player_fat_veg.choose_feeding(1, List([self.ex_client_players.burr_veg.player_configuration,
                                                                self.ex_client_players.carn_fat.player_configuration,
                                                                self.ex_client_players.fora.player_configuration])),
                         StoreFatChoice(1, 1))

        # Choosing Fat Species before Carnivore
        player_fat_carn = self.ex_players.fat_and_carn_coop
        self.assertEqual(player_fat_carn.choose_feeding(2, List([self.ex_client_players.burr_veg.player_configuration,
                                                                 self.ex_client_players.carn_fat.player_configuration,
                                                                 self.ex_client_players.fora.player_configuration])),
                         StoreFatChoice(1, 2))

        # Choosing Fat Species before Carnivore and before Full Fat
        player_carn_fat_fat = self.ex_players.carn_coop_and_fat_and_fat
        self.assertEqual(
            player_carn_fat_fat.choose_feeding(10, List([self.ex_client_players.burr_veg.player_configuration,
                                                         self.ex_client_players.carn_fat.player_configuration,
                                                         self.ex_client_players.fora.player_configuration])),
            StoreFatChoice(2, SPECIES_MAX_BODY_SIZE))

        # Choosing Fat Species before Carnivore and Vegetarian
        player_fat_carn_veg = self.ex_players.fat_and_carn_and_shell_veg
        self.assertEqual(
            player_fat_carn_veg.choose_feeding(10, List([self.ex_client_players.burr_veg.player_configuration,
                                                         self.ex_client_players.carn_fat.player_configuration,
                                                         self.ex_client_players.fora.player_configuration])),
            StoreFatChoice(1, SPECIES_MAX_BODY_SIZE))

        # Choosing Vegetarian before Carnivore
        player_carn_veg = self.ex_players.carn_and_coop_veg
        self.assertEqual(player_carn_veg.choose_feeding(6, List([self.ex_client_players.burr_veg.player_configuration,
                                                                 self.ex_client_players.carn_fat.player_configuration,
                                                                 self.ex_client_players.fora.player_configuration])),
                         FeedVegetarianChoice(1))

    def test_fat_ordering(self):
        # Test that the species with more fat tissue space is picked  5 - 3 > 6 - 5
        player_diff_fat_space = SillyPlayer.from_species([self.ex_species.fat5_fed1_b6,
                                                          self.ex_species.fat3_fed2_b5])
        self.assertEqual(
            player_diff_fat_space.choose_feeding(3, List([self.ex_client_players.carn.player_configuration])),
            StoreFatChoice(1, 2))

        # Choose the Fat Species with the greater Population
        player_diff_fat_pop = SillyPlayer.from_species([self.ex_species.fat3_bd4_popmax_food1,
                                                        self.ex_species.fat3_bd4_pop4_food1])
        self.assertEqual(
            player_diff_fat_pop.choose_feeding(1, List([self.ex_client_players.burr_veg.player_configuration,
                                                        self.ex_client_players.carn_fat.player_configuration,
                                                        self.ex_client_players.fora.player_configuration])),
            StoreFatChoice(0, 1))

        # Choose the Fat Species with the greater food already fed
        player_diff_fat_pop = SillyPlayer.from_species([self.ex_species.fat3_bd4_pop4_food1,
                                                        self.ex_species.fat3_bd4_pop4_food3])
        self.assertEqual(
            player_diff_fat_pop.choose_feeding(1, List([self.ex_client_players.burr_veg.player_configuration,
                                                        self.ex_client_players.carn_fat.player_configuration,
                                                        self.ex_client_players.fora.player_configuration])),
            StoreFatChoice(1, 1))

        # Choose the Fat Species with the greater body size
        player_diff_fat_pop = SillyPlayer.from_species([self.ex_species.fat5_bd6_popmax_food1,
                                                        self.ex_species.fat3_bd4_popmax_food1])
        self.assertEqual(
            player_diff_fat_pop.choose_feeding(1, List([self.ex_client_players.burr_veg.player_configuration,
                                                        self.ex_client_players.carn_fat.player_configuration,
                                                        self.ex_client_players.fora.player_configuration])),
            StoreFatChoice(0, 1))

        # If species are identical, choose the first one
        player_fat_identical = SillyPlayer.from_species([self.ex_species.fat3_fed2_b5,
                                                         self.ex_species.fat3_fed2_b5])
        self.assertEqual(
            player_fat_identical.choose_feeding(2, List([self.ex_client_players.default.player_configuration])),
            StoreFatChoice(0, 2))

    def test_choose_veg(self):
        # Choose the vegetarian with the largest population
        player_veg_diff_pop = SillyPlayer.from_species(
            [self.ex_species.norm_pstart2, self.ex_species.norm_bstart3])
        self.assertEqual(
            player_veg_diff_pop.choose_feeding(2, List([self.ex_client_players.default.player_configuration])),
            FeedVegetarianChoice(0))

        # With same population, choose the vegetarian with the largest number of food tokens
        player_veg_diff_food = SillyPlayer.from_species([self.ex_species.norm_fed1_p2,
                                                         self.ex_species.norm_fed3_p4])
        self.assertEqual(
            player_veg_diff_food.choose_feeding(2, List([self.ex_client_players.default.player_configuration])),
            FeedVegetarianChoice(1))

        # With same population and food tokens, choose the vegetarian with the largest body size
        player_veg_diff_body_size = SillyPlayer.from_species([self.ex_species.norm_bstart3,
                                                              self.ex_species.norm_bstart4])
        self.assertEqual(
            player_veg_diff_body_size.choose_feeding(2, List([self.ex_client_players.default.player_configuration])),
            FeedVegetarianChoice(1))
        # With identical vegetarians, choose the first one
        player_veg_identical = SillyPlayer.from_species([self.ex_species.norm_default,
                                                         self.ex_species.norm_default])
        self.assertEqual(
            player_veg_identical.choose_feeding(2, List([self.ex_client_players.default.player_configuration])),
            FeedVegetarianChoice(0))

    def test_choose_carn(self):
        # If all carnivores can attack, largest is picked to attack only target (id = 1)
        player_card_order_varied = SillyPlayer.from_species([self.ex_species.carn_pstart1,
                                                             self.ex_species.carn_default,
                                                             self.ex_species.carn_pstart1_bstart3])
        self.assertEqual(
            player_card_order_varied.choose_feeding(3, List([self.ex_client_players.carn.player_configuration])),
            AttackWithCarnivoreChoice(2, 0, 0))

        # If 2 carnivores come in same place in order, pick first in list
        player_carn_order_match = SillyPlayer.from_species([self.ex_species.carn_pstart1,
                                                            self.ex_species.carn_default,
                                                            self.ex_species.carn_pstart1])
        self.assertEqual(
            player_carn_order_match.choose_feeding(3, List([self.ex_client_players.carn.player_configuration])),
            AttackWithCarnivoreChoice(0, 0, 0))

        # If some can't attack, pick largest that can attack
        player_carn_can_attack = SillyPlayer.from_species([self.ex_species.carn_pstart1_bstart3,
                                                           self.ex_species.carnamb_default,
                                                           self.ex_species.carnamb_pstart2])
        player_double_warn = SillyPlayer.from_species([self.ex_species.warn_default,
                                                       self.ex_species.warn_default2], player_id=12)
        self.assertEqual(player_carn_can_attack.choose_feeding(3, List([player_double_warn.player.player_configuration])),
                         AttackWithCarnivoreChoice(2, 0, 0))

        # Make sure the carnivore attacks the largest of the attackable species
        player_carn_basic = SillyPlayer.from_species([self.ex_species.carn_default])
        player_some_warned = SillyPlayer.from_species([self.ex_species.warn_default,
                                                       self.ex_species.norm_pstart2,
                                                       self.ex_species.norm_bstart3], player_id=12)
        self.assertEqual(player_carn_basic.choose_feeding(3, List([player_some_warned.player.player_configuration])),
                         AttackWithCarnivoreChoice(0, 0, 2))

        # If two species could equally be chosen, favor earlier external_players
        self.assertEqual(
            player_carn_basic.choose_feeding(3, List([self.ex_client_players.fat_default.player_configuration,
                                                      self.ex_client_players.carn.player_configuration])),
            AttackWithCarnivoreChoice(0, 0, 0))

        # Within external_players, with two equal species, attacks first
        player_equiv_defs = SillyPlayer.from_species([self.ex_species.norm_default,
                                                      self.ex_species.carn_default], player_id=12)
        self.assertEqual(player_carn_basic.choose_feeding(3, List([player_equiv_defs.player.player_configuration])),
                         AttackWithCarnivoreChoice(0, 0, 0))

        # Test the new index result instead of id
        player_equiv_defs = SillyPlayer.from_species([self.ex_species.carn_default], player_id=12)
        self.assertEqual(player_equiv_defs.choose_feeding(3, List([self.ex_client_players.burr_veg.player_configuration,
                                                                   self.ex_client_players.carn.player_configuration,
                                                                   self.ex_client_players.carn.player_configuration,
                                                                   self.ex_client_players.player_state_with_4.player_configuration])),
                         AttackWithCarnivoreChoice(0, 3, 3))

    def test_choose_action(self):
        simple_player_4_cards = self.ex_players.carn_w_cards
        simple_player_3_cards = self.ex_players.coop_w_cards

        action3 = Action(FoodCardChoice(0), [], [], [GainBoard(1, [2])], [])
        self.assertEqual(action3, simple_player_3_cards.choose_action([], []))

        action4 = Action(FoodCardChoice(0), [GainPopulation(1, 1)], [], [GainBoard(3, [2])], [])
        self.assertEqual(action4, simple_player_4_cards.choose_action([], []))

    def test_choose_action_complex(self):
        player1 = Player(1, [Species(0,0,1,[SymbiosisCard(2)])], 1,
                         [FatTissueCard(-3, 0), FertileCard(-2), ForagingCard(-1),
                          HardShellCard(0), LongNeckCard(-1), LongNeckCard(-2)])
        silly_player1 = SillyPlayer(player_id=1, player_configuration=player1.player_configuration)

        action1 = Action(FoodCardChoice(0), [GainPopulation(1, 3)], [GainBody(1, 5)], [GainBoard(1, [2])],
                         [ReplaceTrait(1, 0, 4)])

        self._test_lexo_card_keys(LongNeckCard(-2), LongNeckCard(-1))
        self._test_lexo_card_keys(HardShellCard(0), LongNeckCard(-1))
        self._test_lexo_card_keys(LongNeckCard(-2), LongNeckCard(0))

        action1_actual = silly_player1.choose_action([], [])
        self.assertEqual(action1_actual, action1)

    def _test_lexo_card_keys(self, smaller_card: TraitCard, larger_card: TraitCard):
        """ Test that the smaller card is less than the larger card """
        smaller_key = LexicographicCardKey(smaller_card)
        larger_key = LexicographicCardKey(larger_card)
        self.assertLess(smaller_key, larger_key)
        self.assertNotEqual(smaller_key, larger_key)


    if __name__ == '__main__':
        unittest.main()
