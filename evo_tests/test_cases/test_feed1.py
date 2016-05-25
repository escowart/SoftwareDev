import unittest

from evo_tests.examples.all_examples import *


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.species = Species(fed_food=0, population=7)
        self.player = Player(1,[self.species])
        self.player.external_player = SillyPlayer(1, self.player.player_configuration)
        self.dealer = Dealer(PlayerSequence([self.player]), WateringHole(100))

        self.choice = FeedVegetarianChoice(0)

    def test_dealer_feed_species(self):
        self.assertEqual(self.species.fed_food, 0)
        self.assertEqual(self.player.species_list[0], self.species)
        self.dealer.feed_species(0, self.player)
        self.assertEqual(self.species.fed_food, 1)

    def test_dealer_feed_species(self):
        self.assertEqual(self.species.fed_food, 0)
        self.dealer.feed_species(0, self.player)
        self.assertEqual(self.species.fed_food, 1)

    def test_apply(self):
        self.assertEqual(self.species.fed_food, 0)
        self.choice.apply(self.dealer, self.player)
        self.assertEqual(self.species.fed_food, 1)

    def test_feed1(self):
        self.assertEqual(self.species.fed_food, 0)
        self.dealer.feed1(self.player, self.choice)
        self.assertEqual(self.species.fed_food, 1)