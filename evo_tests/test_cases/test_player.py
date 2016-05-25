import unittest

from evo_tests.examples.all_examples import *


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.ex_player_states = ExamplePlayer()
        self.ex_species = ExampleSpecies()
        self.default_state = Player(1)

    def test_player_id(self):
        self.assertEqual(self.default_state.player_id, 1)


        self.default_state.player_id = 1
        self.default_state.player_id = 100

        self.default_state._player_id = Unset
        with self.assertRaises(UnsetValueError):
            player_id = self.default_state.player_id

    def test_species_list(self):
        self.assertEqual(self.default_state.species_list, [])

        with self.assertRaises(ValueError):
            self.default_state.species_list = [Unset]

        self.default_state._species_list = Unset
        with self.assertRaises(UnsetValueError):
            species_list = self.default_state.species_list

    def test_food_bag(self):
        self.assertEqual(self.default_state.food_bag, 0)

        with self.assertRaises(ValueError):
            self.default_state.food_bag = -1

        self.default_state.food_bag = 0
        self.default_state.food_bag = 100

        self.default_state._food_bag = Unset
        with self.assertRaises(UnsetValueError):
            food_bag = self.default_state.food_bag

    def test_hand(self):
        self.assertEqual(self.default_state.hand, [])

        with self.assertRaises(ValueError):
            self.default_state.hand = [Unset]

        self.default_state._hand = Unset
        with self.assertRaises(UnsetValueError):
            hand = self.default_state.hand

    def test_any_hungry_species(self):
        self.assertTrue(self.ex_player_states.carn.any_hungry_species)

        self.assertTrue(self.ex_player_states.carn_coop_and_fat_and_fat.any_hungry_species)

        self.assertFalse(self.ex_player_states.burr_veg.any_hungry_species)

        self.assertFalse(Player(1).any_hungry_species)

    def test_any_extinct_species(self):
        self.assertFalse(self.ex_player_states.carn.any_extinct_species)

        self.assertFalse(self.ex_player_states.carn_coop_and_fat_and_fat.any_extinct_species)

        self.assertFalse(self.ex_player_states.burr_veg.any_extinct_species)

        self.assertFalse(Player(1).any_extinct_species)

        self.assertTrue(Player(2, [Species(population=SPECIES_EXTINCTION_POP)]).any_extinct_species)

    def test_give_food_to_species(self):
        norm_player = Player(1, [self.ex_species.norm_default])
        player1 = Player(2, [self.ex_species.fat5_fed1_b6, self.ex_species.norm_fed3_p4])
        species0 = player1.species_list[0]
        species1 = player1.species_list[1]

        self.assertRaises(ValueError, norm_player.give_food_to_species, 0, 2)

        self.assertEqual(1, species0.fed_food)

        player1.give_food_to_species(0, 2)
        self.assertEqual(3, species0.fed_food)
        self.assertEqual(3, species1.fed_food)

        player1.give_food_to_species(1, 1)
        self.assertEqual(3, species0.fed_food)
        self.assertEqual(4, species1.fed_food)

    def test_can_feed_or_store_any_species(self):
        fat_player = Player(3, [self.ex_species.fat3_bd4_pop4_food1])
        self.assertTrue(fat_player.can_any_species_feed_or_store([]))

        full_fat = Player(4, [self.ex_species.fat_max])
        self.assertTrue(full_fat.can_any_species_feed_or_store([]))

        full_fat.get_species_at_index(0).fed_food = full_fat.get_species_at_index(0).population
        self.assertFalse(full_fat.can_any_species_feed_or_store([]))

        veg = Player(5, [self.ex_species.norm_bmax])
        self.assertTrue(veg.can_any_species_feed_or_store([]))

        carn0 = Player(6, [self.ex_species.carn_default])
        self.assertFalse(carn0.can_any_species_feed_or_store([]))

        self.assertFalse(carn0.can_any_species_feed_or_store([carn0]))

        self.assertTrue(carn0.can_any_species_feed_or_store([self.ex_player_states.carn_coop_and_fat_and_fat]))
        self.assertFalse(carn0.can_any_species_feed_or_store([self.ex_player_states.burr_veg]))

    def test_can_feed_as_carn_or_store_any_species(self):
        fat_player = Player(3, [self.ex_species.fat3_bd4_pop4_food1])
        self.assertTrue(fat_player.can_any_species_attack_or_store([]))

        full_fat = Player(4, [self.ex_species.fat_max])
        self.assertFalse(full_fat.can_any_species_attack_or_store([]))

        full_fat.get_species_at_index(0).fed_food = full_fat.get_species_at_index(0).population
        self.assertFalse(full_fat.can_any_species_attack_or_store([]))

        veg = Player(5, [self.ex_species.norm_bmax])
        self.assertFalse(veg.can_any_species_attack_or_store([]))

        carn0 = Player(6, [self.ex_species.carn_default])
        self.assertFalse(carn0.can_any_species_attack_or_store([]))

        self.assertFalse(carn0.can_any_species_attack_or_store([carn0]))

        self.assertTrue(carn0.can_any_species_attack_or_store([self.ex_player_states.carn_coop_and_fat_and_fat]))
        self.assertFalse(carn0.can_any_species_attack_or_store([self.ex_player_states.burr_veg]))

    # TODO: Change tests
    def _test_get_automated_feeding_choice(self):
        veg = Player(5, [self.ex_species.norm_bmax])
        self.assertTrue(veg.choose_feeding(Dealer(PlayerSequence([veg])), FeedVegetarianChoice(0)))

        self.assertEqual(self.ex_player_states.carn_and_coop_veg.choose_feeding([], 10),
                         FeedVegetarianChoice(1))

        carn = self.ex_player_states.carn
        carn.external_player = SillyPlayer(carn.player_id, carn.player_configuration)
        self.assertEqual(carn.choose_feeding(PlayerSequence([carn]), 10), InvalidFeedingChoice)

        fat_max = self.ex_player_states.fat_max
        fat_max.external_player = SillyPlayer(fat_max.player_id, fat_max.player_configuration)
        self.assertEqual(fat_max.choose_feeding(PlayerSequence([fat_max]), 10), FeedVegetarianChoice(0))

        fat_min = self.ex_player_states.fat_min
        fat_min.external_player = SillyPlayer(fat_min.player_id, fat_min.player_configuration)
        self.assertEqual(fat_min.choose_feeding(PlayerSequence([fat_min]), 10), StoreFatChoice(0, 4))

    def test_remove_extinct_species(self):
        pass


if __name__ == '__main__':
    unittest.main()
