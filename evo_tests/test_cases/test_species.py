import unittest

from evo_tests.examples.all_examples import *
from evolution.species import *


class TestSpecies(unittest.TestCase):
    def setUp(self):
        self.ex_species = ExampleSpecies()
        self.ex_traits = ExampleTraits()
        self.ex_trait_types = ExampleTraitTypes()
        self.ex_player_states = ExamplePlayer()

    def test_get_population(self):
        self.assertEqual(self.ex_species.norm_default.population,
                         SPECIES_START_POP)
        self.assertEqual(self.ex_species.norm_pstart2.population,
                         2 + SPECIES_START_POP)
        self.assertEqual(self.ex_species.pack_bstart_pstart2.population,
                         2 + SPECIES_START_POP)

    def test_set_population(self):
        self.ex_species.norm_default.population = (SPECIES_EXTINCTION_POP)
        self.assertEqual(self.ex_species.norm_default.population, SPECIES_EXTINCTION_POP)
        self.ex_species.norm_default.population = (SPECIES_MAX_POP)
        self.assertEqual(self.ex_species.norm_default.population, SPECIES_MAX_POP)

        self.ex_species.shell_default.population = (2 + SPECIES_START_POP)
        self.assertEqual(self.ex_species.shell_default.population, 2 + SPECIES_START_POP)

        self.ex_species.norm_default.population = -1 + SPECIES_EXTINCTION_POP
        self.assertEqual(self.ex_species.norm_default.population, SPECIES_EXTINCTION_POP)

        with self.assertRaises(ValueError):
            self.ex_species.norm_default.population = 1 + SPECIES_MAX_POP

    def test_feed(self):
        player0 = self.ex_player_states.carn_coop_a_veg_a_fat
        player0sp0 = player0.species_list[0]
        player0sp1 = player0.species_list[1]
        player0sp2 = player0.species_list[2]
        watering_hole = WateringHole(50, [])

        self.assertEquals(player0sp0.fed_food, 0)
        self.assertEquals(player0sp1.fed_food, 0)
        self.assertEquals(player0sp2.fed_food, 1)

        player0sp0.feed(0, player0, watering_hole)

        self.assertEquals(player0sp0.fed_food, 1)
        self.assertEquals(player0sp1.fed_food, 1)
        self.assertEquals(player0sp2.fed_food, 1)

    def test_attack(self):
        player0 = self.ex_player_states.player_horns_default
        player1 = self.ex_player_states.player_state_with_4
        p2s0 = player1.species_list[0]
        deck = Deck([TraitCard(3)])

        self.assertEquals(player0.num_species, 2)
        self.assertEqual(player1.num_species, 4)
        self.assertEqual(player0.hand_size, 0)

        p2s0.attack(player1, 0, player0, 0, deck)

        self.assertEqual(player0.num_species, 1)
        self.assertEqual(player1.num_species, 3)
        self.assertEqual(len(deck.cards), 0)
        self.assertEqual(player0.hand_size, 1)

    def test_damage(self):
        player = self.ex_player_states.carn_and_coop_veg
        species0 = player.species_list[0]
        player2 = self.ex_player_states.player_state_with_4

        self.assertEquals(player.num_species, 2)
        species0.reduce_population(1, player, 1, Deck())
        self.assertEqual(player.num_species, 1)

        self.assertEqual(player2.species_list[3].population, 4)

        player2.species_list[3].reduce_population(1, player2, 3, Deck())

        self.assertEqual(player2.species_list[3].population, 3)

    def test_is_attackable(self):
        # Can't Attack Self
        self.assertEqual(self.ex_species.carn_default.is_attackable(self.ex_species.carn_default), False)
        self.assertEqual(self.ex_species.carn_default.is_attackable(self.ex_species.carn_default,
                                                                    self.ex_species.carn_default,
                                                                    self.ex_species.carn_default), False)
        # Can be attacked by random Carnivore
        self.assertEqual(self.ex_species.norm_default.is_attackable(self.ex_species.carn_default), True)
        self.assertEqual(self.ex_species.norm_default.is_attackable(self.ex_species.carn_default,
                                                                    self.ex_species.carn_default,
                                                                    self.ex_species.carn_default), True)
        # Burrowing defender
        self.assertEqual(self.ex_species.burr_fstart_pstart.is_attackable(self.ex_species.carn_default), True)
        self.assertEqual(self.ex_species.burr_fstart1_pstart.is_attackable(self.ex_species.carn_default), False)
        self.assertEqual(self.ex_species.burr_fstart2_pstart2.is_attackable(self.ex_species.carn_default), True)
        self.assertEqual(self.ex_species.burr_fstart3_pstart2.is_attackable(self.ex_species.carn_default), False)

    def test_get_owner_species(self):
        attacker = self.ex_species.carn_fat_default
        defender = self.ex_species.symb_default
        defender_left = self.ex_species.burr_fstart1_pstart
        defender_right = self.ex_species.carn_coop_default

        self.assertTrue(Species.get_owner_species(defender, attacker, defender_left, defender_right) == NoSpecies)
        self.assertTrue(Species.get_owner_species(defender, attacker, defender_left, defender_right,
                                                  SituationFlag.ATTACKER), attacker)
        self.assertTrue(Species.get_owner_species(defender, attacker, defender_left, defender_right,
                                                  SituationFlag.DEFENDER) is defender)
        self.assertTrue(Species.get_owner_species(defender, attacker, defender_left, defender_right,
                                                  SituationFlag.DEFENDER_L_NEIGHBOR) is defender_left)
        self.assertTrue(Species.get_owner_species(defender, attacker, defender_left, defender_right,
                                                  SituationFlag.DEFENDER_R_NEIGHBOR) is defender_right)

    def test_has_trait(self):
        self.assertTrue(self.ex_species.burr_fstart1_pstart.has_trait(self.ex_trait_types.burr_type))
        self.assertFalse(self.ex_species.burr_fstart1_pstart.has_trait(self.ex_trait_types.scav_type))

        self.assertTrue(self.ex_species.carn_fat_default.has_trait(self.ex_trait_types.carn_type))
        self.assertFalse(self.ex_species.carn_fat_default.has_trait(self.ex_trait_types.burr_type))

        trait_types = self.ex_trait_types.all_trait_types
        for index, trait_type in enumerate(trait_types):
            species = Species(played_cards=[trait_type()])
            self.assertTrue(species.has_trait(trait_type))
            if index + 1 >= len(trait_types):
                for other_trait in trait_types[index + 1:]:
                    self.assertFalse(species.has_trait(other_trait))

    def test_attack_body_size(self):
        norm_species = self.ex_species.norm_default
        norm_body_size = norm_species.body_size
        norm_sit_species = SituationSpecies(norm_species)

        self.assertEqual(norm_sit_species.body_size, norm_body_size)

        norm_sit_species.situation_position = SituationFlag.ATTACKER
        self.assertEqual(norm_sit_species.body_size, norm_body_size)

        norm_sit_species.situation_position = SituationFlag.DEFENDER
        self.assertEqual(norm_sit_species.body_size, norm_body_size)

        norm_sit_species.situation_position = SituationFlag.DEFENDER_L_NEIGHBOR
        self.assertEqual(norm_sit_species.body_size, norm_body_size)

        norm_sit_species.situation_position = SituationFlag.DEFENDER_R_NEIGHBOR
        self.assertEqual(norm_sit_species.body_size, norm_body_size)

        pack_species = self.ex_species.pack_bstart3_pstart2
        pack_body_size = pack_species.body_size
        pack_atk_body_size = pack_body_size + pack_species.population
        pack_sit_species = SituationSpecies(pack_species)

        self.assertEqual(pack_sit_species.body_size, pack_body_size)

        pack_sit_species.situation_position = SituationFlag.DEFENDER
        self.assertEqual(pack_sit_species.body_size, pack_body_size)

        pack_sit_species.situation_position = SituationFlag.ATTACKER
        self.assertEqual(pack_sit_species.body_size, pack_atk_body_size)
        self.assertEqual(pack_sit_species.body_size, pack_atk_body_size)
        self.assertEqual(pack_sit_species.body_size, pack_atk_body_size)
        self.assertEqual(pack_sit_species.body_size, pack_atk_body_size)

        pack_sit_species.situation_position = SituationFlag.DEFENDER_R_NEIGHBOR
        self.assertEqual(pack_sit_species.body_size, pack_body_size)

        pack_sit_species.situation_position = SituationFlag.DEFENDER_L_NEIGHBOR
        self.assertEqual(pack_sit_species.body_size, pack_body_size)
        self.assertEqual(pack_sit_species.body_size, pack_body_size)

    def test_properties(self):
        self.assertFalse(self.ex_species.norm_default.is_carnivore)
        self.assertTrue(self.ex_species.norm_default.is_vegetarian)
        self.assertTrue(self.ex_species.norm_default.is_hungry)

    def test_give_food(self):
        norm_species = self.ex_species.norm_default
        self.assertRaises(ValueError, norm_species.give_food, 2)

        pop3_species = self.ex_species.norm_pstart2
        pop3_species.give_food(2)
        self.assertEqual(pop3_species.fed_food, 2)
        pop3_species.give_food(1)
        self.assertEqual(pop3_species.fed_food, 3)

    def test_can_feed_or_store(self):

        fat_species = self.ex_species.fat3_bd4_pop4_food1
        self.assertTrue(fat_species.can_feed_or_store([]))

        full_fat = self.ex_species.fat_max
        self.assertTrue(full_fat.has_trait(FatTissueCard))
        self.assertEqual(full_fat.fat_tissue_need, 0)
        self.assertFalse(full_fat.can_store_more_fat)
        self.assertTrue(full_fat.can_feed_or_store([]))

        full_fat.fed_food = full_fat.population
        self.assertFalse(full_fat.can_feed_or_store([]))

        veg = self.ex_species.norm_bmax
        self.assertTrue(veg.can_feed_or_store([]))

        carn0 = self.ex_species.carn_default
        self.assertFalse(carn0.can_feed_or_store([]))


        self.assertTrue(carn0.can_feed_or_store([self.ex_player_states.carn_coop_and_fat_and_fat]))
        self.assertFalse(carn0.can_feed_or_store([self.ex_player_states.burr_veg]))

    def test_food_wanted(self):
        self.assertEqual(self.ex_species.carn_default.num_tokens_per_feed, NUM_TOKENS_FOR_NORMAL_FEED)
        self.assertEqual(self.ex_species.carn_fat_coop_default.num_tokens_per_feed, NUM_TOKENS_FOR_NORMAL_FEED)
        self.assertEqual(self.ex_species.burr_fstart1_pstart.num_tokens_per_feed, NUM_TOKENS_FOR_NORMAL_FEED)
        self.assertEqual(self.ex_species.burr_fstart_pstart.num_tokens_per_feed, NUM_TOKENS_FOR_NORMAL_FEED)
        self.assertEqual(self.ex_species.fora_default.num_tokens_per_feed, NUM_TOKENS_FOR_FORAGING_FEED)
        self.assertEqual(self.ex_species.carn_fora_default.num_tokens_per_feed, NUM_TOKENS_FOR_FORAGING_FEED)


if __name__ == '__main__':
    unittest.main()