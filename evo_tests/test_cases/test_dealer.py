import unittest

from evo_tests.examples.ex_dealer import ExampleDealers
from evolution.all_evo import *


class TestDealer(unittest.TestCase):

    def setUp(self):
        self.ex_dealers = ExampleDealers()

    def test_properties(self):
        self.assertEqual(self.ex_dealers.dealer0.is_watering_hole_empty, False)
        self.assertEqual(self.ex_dealers.dealer0.player_sequence, self.ex_dealers.seq0)
        self.assertEqual(self.ex_dealers.dealer0.configuration, self.ex_dealers.config0)
        self.assertEqual(self.ex_dealers.dealer0.food_on_watering_hole, 50)

    def test_choose_feeding_message_store_fat_choice(self):
        choose_feeding_msg = ChooseFeedingServerMessage(food_bag=cast(Natural, 3),
                                                        species_list=[Species(0, 1, 2, [FertileCard(3)]),
                                                                      Species(0, 1, 2, [FatTissueCard(-2, 1)])],
                                                        hand=cast(List[TraitCard],
                                                                  [ForagingCard(-2), ForagingCard(-3), LongNeckCard(-1),
                                                                   LongNeckCard(-2),
                                                                   ScavengerCard(1), ScavengerCard(0)]),
                                                        food_on_watering_hole=cast(Natural, 1),
                                                        other_player_boards=cast(List[SpeciesBoards],[]))

        dealer0 = self.ex_dealers.dealer0
        dealer0.watering_hole = WateringHole(100)
        player1 = Player(*choose_feeding_msg.to_player_configuration())

        species1 = player1.species_list[1]

        self.assertEqual(species1.body_size, 1)
        self.assertEqual(species1.stored_fat_food, 1)
        self.assertFalse(species1.can_store_more_fat)

        stored_fat_choice = StoreFatChoice(1, 1)
        self.assertFalse(stored_fat_choice.is_valid(dealer0, player1))

    def test_feed_species(self):
        dealer0 = self.ex_dealers.dealer0
        player0 = dealer0.player_sequence[0]
        species0 = player0.species_list[0]
        species1 = player0.species_list[1]
        species2 = player0.species_list[2]
        player1species0 = dealer0.player_sequence[1].species_list[0]

        self.assertEqual(species0.fed_food, 0)
        self.assertEqual(species0.population, 1)

        self.assertEqual(species1.fed_food, 0)
        self.assertEqual(species1.population, 1)

        self.assertEqual(species2.fed_food, 1)
        self.assertEqual(species2.population, 4)

        self.assertEqual(player1species0.fed_food, 0)
        self.assertEqual(player1species0.population, 1)

        dealer0.feed_species(0, player0)

        self.assertEqual(species0.fed_food, 1)
        self.assertEqual(species0.population, 1)

        self.assertEqual(species1.fed_food, 1)
        self.assertEqual(species1.population, 1)

        self.assertEqual(species2.fed_food, 1)
        self.assertEqual(species2.population, 4)

    def grab_food_from_watering_hole(self):
        dealer0 = self.ex_dealers.dealer0

        self.assertEqual(dealer0.grab_food_token_from_watering_hole(10), 10)
        self.assertEqual(dealer0.food_on_watering_hole, 40)

    def remove_extinct_species(self):
        dealer0 = self.ex_dealers.dealer0
        player0 = dealer0.player_sequence[0]
        extinct_species = player0.species_list[0]
        extinct_species.population = 0
        dealer0.remove_extinct_species()

        self.assertNotEqual(player0.species_list[0], extinct_species)

    def test_feed_scavengers(self):
        dealer2 = self.ex_dealers.dealer2
        player0 = dealer2.player_sequence[0]
        carn0 = player0.species_list[0]
        scav1 = player0.species_list[1]

        player2 = dealer2.player_sequence[2]
        scav2 = player2.species_list[1]

        self.assertEqual(carn0.fed_food, 0)
        self.assertEqual(scav1.fed_food, 0)
        self.assertEqual(scav2.fed_food, 0)

        dealer2.feed_scavengers()

        self.assertEqual(carn0.fed_food, 0)
        self.assertEqual(scav1.fed_food, 1)
        self.assertEqual(scav2.fed_food, 1)

    def test_feed1(self):
        # Vegetarian Foraging Cooperation Chain Example
        dealer4 = self.ex_dealers.dealer4
        player0 = dealer4.player_sequence[0]
        species0 = player0.species_list[0]
        species1 = player0.species_list[1]
        species2 = player0.species_list[2]

        self.assertEqual(species0.fed_food, 0)
        self.assertEqual(species0.population, 7)

        self.assertEqual(species1.fed_food, 0)
        self.assertEqual(species1.population, 7)

        self.assertEqual(species2.fed_food, 0)
        self.assertEqual(species2.population, 1)

        player0.external_player = SillyPlayer(player0.player_id, player0.player_configuration)
        dealer4.feed1(player0, player0.choose_feeding(dealer4))

        self.assertEqual(species0.fed_food, 2)
        self.assertEqual(species0.population, 7)

        self.assertEqual(species1.fed_food, 4)
        self.assertEqual(species1.population, 7)

        self.assertEqual(species2.fed_food, 1)
        self.assertEqual(species2.population, 1)

    def test_deal(self):
        deck = Deck.create_deck()
        player1 = Player(1)
        player2 = Player(2)
        player3 = Player(3)

        dealer_new = Dealer(PlayerSequence([player1, player2, player3]), deck=deck)

        self.assertEqual(4, player1.num_cards_wanted)
        self.assertEqual(4, player2.num_cards_wanted)
        self.assertEqual(4, player3.num_cards_wanted)

        dealer_new.deal()

        self.assertEqual(4, len(player1.all_cards))
        self.assertEqual(4, len(player2.all_cards))
        self.assertEqual(4, len(player3.all_cards))

    def test_split_configuration_sequence(self) -> None:
        player1 = Player(1)
        player2 = Player(2)
        player3 = Player(3)
        dealer_1 = Dealer(PlayerSequence([player1]))
        dealer_2 = Dealer(PlayerSequence([player1, player2]))
        dealer_3 = Dealer(PlayerSequence([player1, player2, player3]))

        self._test_split_configuration(dealer_1, player1)
        self._test_split_configuration(dealer_2, player1)
        self._test_split_configuration(dealer_2, player2)
        self._test_split_configuration(dealer_3, player1)
        self._test_split_configuration(dealer_3, player2)
        self._test_split_configuration(dealer_3, player3)

    def _test_split_configuration(self, dealer: Dealer, player: Player) -> None:
        first_half, second_half = dealer.split_configuration_sequence(player)

        expected_config_list = [player.player_configuration for player in dealer.player_sequence]
        actual_config_list = first_half + [player.player_configuration] + second_half
        #print("Actual:   {}\nExpected: {}\n".format(actual_config_list, expected_config_list))
        self.assertEqual(actual_config_list, expected_config_list)


if __name__ == '__main__':
    unittest.main()
