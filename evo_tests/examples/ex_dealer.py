from evo_tests.examples.ex_simple_player import *


class ExampleDealers:

    def __init__(self) -> None:
        self.ex_player_states = ExamplePlayer()

        self.seq0 = PlayerSequence(List([self.ex_player_states.carn_coop_a_veg_a_fat, self.ex_player_states.carn,
                                         self.ex_player_states.fora]))
        self.config0 = Configuration(self.seq0, WateringHole(50), Deck())
        self.dealer0 = Dealer(*self.config0)

        self.seq1 = PlayerSequence(List(
            [self.ex_player_states.carn, self.ex_player_states.carn_and_coop_veg, self.ex_player_states.fora]))
        self.config1 = Configuration(self.seq1, WateringHole(49), Deck())
        self.dealer1 = Dealer(*self.config1)

        self.seq2 = PlayerSequence(List([self.ex_player_states.carn_and_scav,
                                         self.ex_player_states.burr_veg,
                                         self.ex_player_states.carn_and_scav2]))
        self.config2 = Configuration(self.seq2, WateringHole(30), Deck())
        self.dealer2 = Dealer(*self.config2)

        self.seq3 = PlayerSequence(List(
            [self.ex_player_states.carn, self.ex_player_states.burr_veg, self.ex_player_states.climb]))
        self.config3 = Configuration(self.seq3, WateringHole(50), Deck())
        self.dealer3 = Dealer(*self.config3)

        self.seq4 = PlayerSequence(List([self.ex_player_states.player_fora_coop_3,
                                         self.ex_player_states.default,
                                         self.ex_player_states.default]))
        self.config4 = Configuration(self.seq4, WateringHole(50), Deck())
        self.dealer4 = Dealer(*self.config4)

        self.seq5 = PlayerSequence(List([self.ex_player_states.player_carn_w_cards,
                                         self.ex_player_states.fat3_w_cards,
                                         self.ex_player_states.coop_w_cards,
                                         self.ex_player_states.carn_fat_coop_w_cards,
                                         self.ex_player_states.fert_long_w_cards]))
        self.deck1 = Deck([CarnivoreCard(3), AmbushCard(1), BurrowingCard(3), ClimbingCard(2), FatTissueCard(-2)])
        self.config5 = Configuration(self.seq5, WateringHole(25), self.deck1)
        self.dealer5 = Dealer(*self.config5)
