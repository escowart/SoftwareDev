import unittest
from evolution.messages.player_messages.all_player_messages import *
from evo_tests.examples.ex_dealer import *


class TestFeedingChoice(unittest.TestCase):
    """ Test Feeding Choice """
    def setUp(self):
        self.ex_dealers = ExampleDealers()
        self.dealer0 = self.ex_dealers.dealer0
        self.dealer1 = self.ex_dealers.dealer1
        self.dealer3 = self.ex_dealers.dealer3

        self.player0 = self.dealer0.player_sequence[0]
        self.player1 = self.dealer1.player_sequence[0]
        self.player3 = self.dealer3.player_sequence[0]

        self.player0sp0 = self.dealer0.player_sequence[0].species_list[0]
        self.player0sp1 = self.dealer0.player_sequence[0].species_list[1]
        self.player0sp2 = self.dealer0.player_sequence[0].species_list[2]
        self.player1sp0 = self.dealer0.player_sequence[1].species_list[0]


class TestForgoChoice(TestFeedingChoice):
    """ Test Forgo Choice """
    def test_is_valid(self):
        self.assertTrue(ForgoChoice().is_valid(self.dealer0, self.player0))
        self.assertTrue(ForgoChoice().is_valid(self.dealer1, self.player1))
        self.assertFalse(ForgoChoice().is_valid(self.dealer3, self.player3))


class TestFeedVegetarianChoice(TestFeedingChoice):
    """ Test Feed Vegetarian Choice """
    def test_is_valid(self):
        self.assertFalse(FeedVegetarianChoice(0).is_valid(self.dealer0, self.player0))
        self.assertTrue(FeedVegetarianChoice(1).is_valid(self.dealer0, self.player0))
        self.assertTrue(FeedVegetarianChoice(2).is_valid(self.dealer0, self.player0))

    def test_apply(self):
        self.assertEqual(self.player0sp0.fed_food, 0)
        self.assertEqual(self.player0sp1.fed_food, 0)
        self.assertEqual(self.player0sp2.fed_food, 1)

        FeedVegetarianChoice(1).apply(self.dealer0, self.dealer0.player_sequence[0])

        self.assertEqual(self.player0sp0.fed_food, 0)
        self.assertEqual(self.player0sp1.fed_food, 1)
        self.assertEqual(self.player0sp2.fed_food, 1)


class TestStoreFatChoice(TestFeedingChoice):
    """ Test Store Fat Choice """
    def test_is_valid(self):
        self.assertFalse(StoreFatChoice(0, 1).is_valid(self.dealer0, self.player0))
        self.assertFalse(StoreFatChoice(1, 1).is_valid(self.dealer0, self.player0))
        self.assertTrue(StoreFatChoice(2, 1).is_valid(self.dealer0, self.player0))
        self.assertFalse(StoreFatChoice(2, 2).is_valid(self.dealer0, self.player0))

    def test_apply(self):
        self.assertEqual(self.player0sp0.can_store_more_fat, False)
        self.assertEqual(self.player0sp1.can_store_more_fat, False)
        self.assertEqual(self.player0sp2.stored_fat_food, 3)

        StoreFatChoice(2, 1).apply(self.dealer0, self.dealer0.player_sequence[0])

        self.assertEqual(self.player0sp2.stored_fat_food, 4)


class TestAttackWithCarnivoreChoice(TestFeedingChoice):
    """ Test Attack with Carnivore Choice """
    def test_is_valid(self):
        self.assertFalse(AttackWithCarnivoreChoice(0, 2, 0).is_valid(self.dealer0, self.player0))
        self.assertFalse(AttackWithCarnivoreChoice(1, 2, 0).is_valid(self.dealer0, self.player0))
        self.assertFalse(AttackWithCarnivoreChoice(2, 2, 0).is_valid(self.dealer0, self.player0))
        self.assertTrue(AttackWithCarnivoreChoice(0, 2, 1).is_valid(self.dealer0, self.player0))
        self.assertFalse(AttackWithCarnivoreChoice(1, 2, 1).is_valid(self.dealer0, self.player0))
        self.assertFalse(AttackWithCarnivoreChoice(2, 2, 1).is_valid(self.dealer0, self.player0))
        self.assertFalse(AttackWithCarnivoreChoice(0, 2, 2).is_valid(self.dealer0, self.player0))
        self.assertFalse(AttackWithCarnivoreChoice(1, 2, 2).is_valid(self.dealer0, self.player0))
        self.assertFalse(AttackWithCarnivoreChoice(2, 2, 2).is_valid(self.dealer0, self.player0))
        self.assertTrue(AttackWithCarnivoreChoice(0, 0, 0).is_valid(self.dealer0, self.player0))
        self.assertFalse(AttackWithCarnivoreChoice(1, 0, 0).is_valid(self.dealer0, self.player0))
        self.assertFalse(AttackWithCarnivoreChoice(2, 0, 0).is_valid(self.dealer0, self.player0))

    def test_apply(self):
        self.assertEqual(self.player1sp0.population, 1)
        self.assertEqual(self.player0sp0.fed_food, 0)

        AttackWithCarnivoreChoice(0, 1, 0).apply(self.dealer0, self.dealer0.player_sequence[0])

        self.assertEqual(self.player0sp0.fed_food, 1)

