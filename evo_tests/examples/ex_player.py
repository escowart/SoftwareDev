from evo_tests.examples.ex_species import *


class ExamplePlayer:
    def __init__(self):
        self.ex_species = ExampleSpecies()

        self.default = Player(1)
        self.burr_veg = Player(2, List([self.ex_species.burr_fstart1_pstart]))
        self.carn = Player(3, List([self.ex_species.carn_default]))
        self.coop = Player(4, List([self.ex_species.coop_default]))
        self.carn_coop = Player(5, List([self.ex_species.carn_coop_default]))
        self.fat_default = Player(6, List([self.ex_species.fat_default]))
        self.fat_min = Player(7, List([self.ex_species.fat_min]))
        self.fat3 = Player(8, List([self.ex_species.fat3]))
        self.fat5 = Player(9, List([self.ex_species.fat5]))
        self.fat_max = Player(10, List([self.ex_species.fat_max]))
        self.carn_fat = Player(11, List([self.ex_species.carn_fat_default]))
        self.carn_fat_coop = Player(12, List([self.ex_species.carn_fat_coop_default]))
        self.fora = Player(13, List([self.ex_species.fora_default]))
        self.carn_fora = Player(14, List([self.ex_species.carn_fora_default]))
        self.climb = Player(26, List([self.ex_species.climb_default]))
        self.fat_and_burr_veg = Player(15,
                                       List(
                                                [self.ex_species.burr_fstart1_pstart, self.ex_species.fat5_fed1_b6]))
        self.fat_and_carn_coop = Player(16,
                                        List(
                                                 [self.ex_species.carn_coop_default, self.ex_species.fat3_fed2_b5]))
        self.carn_coop_and_fat_and_fat = Player(17, List([self.ex_species.carn_coop_default,
                                                          self.ex_species.fat_max_fed0_bmax,
                                                          self.ex_species.fat_min_fedmax_bmax]))
        self.fat_and_carn_and_shell_veg = Player(18, List([self.ex_species.carn_coop_default,
                                                           self.ex_species.fat_min_fedmax_bmax,
                                                           self.ex_species.norm_bstartshell]))
        self.carn_and_coop_veg = Player(19,
                                        List(
                                                 [self.ex_species.carn_coop_default, self.ex_species.warn_default]))

        self.fat_fat = Player(20)

        self.player_state_with_4 = Player(21,
                                          List([self.ex_species.carn_default,
                                                     self.ex_species.norm_bstart3,
                                                     self.ex_species.norm_bstart4,
                                                     self.ex_species.norm_fed3_p4]))

        self.carn_coop_a_veg_a_fat = Player(22, List([self.ex_species.carn_coop_default,
                                                      self.ex_species.warn_default,
                                                      self.ex_species.fat3_bd4_pop4_food1]))

        self.carn_and_scav = Player(23,
                                    List([self.ex_species.carn_default, self.ex_species.scav_default]))
        self.carn_and_scav2 = Player(123,
                                     List([self.ex_species.carn_default, self.ex_species.scav_default]))

        self.player_gui_four = Player(24, List(
            [self.ex_species.carn_default, self.ex_species.burr_fstart1_pstart,
             self.ex_species.norm_default, self.ex_species.carn_coop_default]), 10,
                                      List([CarnivoreCard(2), BurrowingCard(2), ForagingCard(-2)]))
        self.player_gui_eight = Player(25, List(
            [self.ex_species.carn_coop_default, self.ex_species.burr_fstart1_pstart,
             self.ex_species.burr_fstart3_pstart2, self.ex_species.carn_default,
             self.ex_species.carn_fat_default, self.ex_species.fat5_fed1_b6,
             self.ex_species.carnamb_default, self.ex_species.climb_default_2]),
                                       30, List(
                [CarnivoreCard(8), AmbushCard(3), BurrowingCard(0), ClimbingCard(3),
                 CooperationCard(3), FatTissueCard(-2), FertileCard(1),
                 ForagingCard(-1), HardShellCard(2), HerdingCard(1), HornCard(-3),
                 LongNeckCard(-3), PackHuntingCard(0), ScavengerCard(1),
                 SymbiosisCard(3), WarningCallCard(2)]))
        self.player_horns_default = Player(27, List(
            [self.ex_species.horn_default, self.ex_species.norm_fed1_p2]))
        self.player_fora_coop_3 = Player(28, List([self.ex_species.fora_coop_default,
                                                   deepcopy(self.ex_species.fora_coop_default),
                                                   self.ex_species.norm_default]))
        self.player_carn_w_cards = Player(29, List([self.ex_species.carn_default]), 0, [CarnivoreCard(1),
                                                                                        WarningCallCard(
                                                                                                          2),
                                                                                        HardShellCard(1),
                                                                                        FatTissueCard(1)
                                                                                        ])
        self.fat3_w_cards = Player(30, List([self.ex_species.fat3]), 0,
                                   [CarnivoreCard(2), PackHuntingCard(1), ClimbingCard(-3)])
        self.coop_w_cards = Player(31, List([self.ex_species.coop_default]), 0,
                                   [AmbushCard(-1), FertileCard(-2), HornCard(0)])
        self.carn_fat_coop_w_cards = Player(32, List([self.ex_species.carn_fat_coop_default]), 0,
                                            [CooperationCard(3),
                                                  AmbushCard(-2),
                                                  FertileCard(1)])
        self.fert_long_w_cards = Player(33,
                                        List(
                                                 [self.ex_species.fertile_default, self.ex_species.long_neck_default]),
                                        0,
                                        [AmbushCard(-2), ClimbingCard(2), HerdingCard(0)])
