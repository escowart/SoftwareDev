import unittest
from evo_tests.examples.ex_dealer import ExampleDealers
from evolution.messages.player_messages.action import *
from evolution.messages.player_messages.action_choice import *


class TestStep4(unittest.TestCase):

    def setUp(self):
        self.ex_dealers = ExampleDealers()

    def test_apply_actions(self):
        dealer5 = self.ex_dealers.dealer5
        p0 = dealer5.player_sequence[0]
        p0species0 = p0.species_list[0]

        action1 = Action(FoodCardChoice(0), [GainPopulation(0, 1)], [], [], [])

        self.assertEqual(p0species0.population, 1)

        action1.apply(dealer5, p0)

        self.assertEqual(p0species0.population, 2)

        p1 = dealer5.player_sequence[1]
        p1species0 = p1.species_list[0]

        action2 = Action(FoodCardChoice(0), [], [GainBody(0, 1)], [], [])

        self.assertEqual(p1species0.body_size, 3)
        action2.apply(dealer5,p1)
        self.assertEqual(p1species0.body_size, 4)

        p2 = dealer5.player_sequence[2]

        action3 = Action(FoodCardChoice(0), [], [], [GainBoard(1, [2])], [])

        self.assertEqual(len(p2.species_list), 1)
        action3.apply(dealer5, p2)
        self.assertEqual(len(p2.species_list), 2)
        self.assertTrue(p2.species_list[1].has_trait(HornCard))

        p3 = dealer5.player_sequence[3]
        p3species0 = p3.species_list[0]

        self.assertTrue(p3species0.has_trait(CarnivoreCard))
        action3 = Action(FoodCardChoice(0), [], [], [], [ReplaceTrait(0, 0, 1)])
        action3.apply(dealer5, p3)
        self.assertFalse(p3species0.has_trait(CarnivoreCard))
        self.assertTrue(p3species0.has_trait(AmbushCard))

    def test_trigger_food_card_flip_traits(self):
        dealer5 = self.ex_dealers.dealer5
        p4 = dealer5.player_sequence[4]
        species0 = p4.species_list[0]
        species1 = p4.species_list[1]

        self.assertEqual(species0.population, 1)
        self.assertEqual(species1.fed_food, 0)

        dealer5.trigger_food_card_flip_traits()

        self.assertEqual(species0.population, 2)
        self.assertEqual(species1.fed_food, 1)

    def test_all_species_move_fat_food(self):
        dealer5 = self.ex_dealers.dealer5
        p1 = dealer5.player_sequence[1]
        p1species0 = p1.species_list[0]
        p1species0.stored_fat_food = 3

        self.assertEqual(p1species0.stored_fat_food, 3)
        dealer5.all_species_move_fat_food()
        self.assertEqual(p1species0.stored_fat_food, 2)

    def test_all_species_reduce_to_fed_population(self):
        dealer5 = self.ex_dealers.dealer5
        p1 = dealer5.player_sequence[1]
        p1species0 = p1.species_list[0]
        p1species0.population = 3
        p1species0.fed_food = 1

        self.assertEqual(p1species0.fed_food, 1)
        self.assertEqual(p1species0.population, 3)
        dealer5.all_species_reduce_to_fed_population()
        self.assertEqual(p1species0.fed_food, 1)
        self.assertEqual(p1species0.population, 1)

    def test_all_players_move_fed_food_to_food_bag(self):
        dealer5 = self.ex_dealers.dealer5
        p0 = dealer5.player_sequence[0]
        p0.species_list[0].population = 3
        p0.species_list[0].fed_food = 3

        p1 = dealer5.player_sequence[1]
        p1.species_list[0].fed_food = 1

        self.assertEqual(p0.food_bag, 0)
        self.assertEqual(p1.food_bag, 0)
        dealer5.all_players_move_fed_food_to_food_bag()
        self.assertEqual(p0.food_bag, 3)
        self.assertEqual(p1.food_bag, 1)