from evo_tests.examples.ex_trait_cards import *


class ExamplePJSpecies:
    def __init__(self):
        self.ex_pj_traits = ExamplePJTraits()
        self.ex_pj_lot = ExamplePJLOT()

        self.food_n1 = [FOOD_STR, -1]
        self.food_0 = [FOOD_STR, 0]
        self.food_1 = [FOOD_STR, 1]
        self.food_max = [FOOD_STR, SPECIES_MAX_POP]
        self.food_max_p1 = [FOOD_STR, SPECIES_MAX_POP + 1]
        self.food_10 = [FOOD_STR, 10]

        self.body_n1 = [BODY_STR, -1]
        self.body_0 = [BODY_STR, 0]
        self.body_1 = [BODY_STR, 1]
        self.body_max = [BODY_STR, SPECIES_MAX_BODY_SIZE]
        self.body_max_p1 = [BODY_STR, SPECIES_MAX_BODY_SIZE + 1]
        self.body_10 = [BODY_STR, 10]

        self.pop_n1 = [POP_STR, -1]
        self.pop_0 = [POP_STR, 0]
        self.pop_1 = [POP_STR, 1]
        self.pop_max = [POP_STR, SPECIES_MAX_POP]
        self.pop_max_p1 = [POP_STR, SPECIES_MAX_POP + 1]
        self.pop_10 = [POP_STR, 10]

        self.traits0 = [TRAITS_STR, self.ex_pj_lot.lot0]
        self.traits1 = [TRAITS_STR, self.ex_pj_lot.lot1]
        self.traits2 = [TRAITS_STR, self.ex_pj_lot.lot2]
        self.traits3 = [TRAITS_STR, self.ex_pj_lot.lot3]
        self.traits4 = [TRAITS_STR, self.ex_pj_lot.lot4]
        self.traits_dup = [TRAITS_STR, self.ex_pj_lot.lot_dup]

        self.fat_food_n1 = [FAT_FOOD_STR, -1]
        self.fat_food_0 = [FAT_FOOD_STR, 0]
        self.fat_food_1 = [FAT_FOOD_STR, 1]
        self.fat_food_max = [FAT_FOOD_STR, SPECIES_MAX_POP]
        self.fat_food_max_p1 = [FAT_FOOD_STR, SPECIES_MAX_POP + 1]
        self.fat_food_10 = [FAT_FOOD_STR, 10]

        self.spe_0 = [self.food_0, self.body_0, self.pop_0, self.traits0]
        self.spe_1 = [self.food_1, self.body_1, self.pop_1, self.traits1]
        self.spe_max = [self.food_max, self.body_max, self.pop_max, self.traits3]
        self.spe_max_f1 = [self.food_max_p1, self.body_max, self.pop_max, self.traits3]
        self.spe_max_b1 = [self.food_max, self.body_max_p1, self.pop_max, self.traits3]
        self.spe_max_p1 = [self.food_max, self.body_max, self.pop_max_p1, self.traits3]
        self.spe_dup = [self.food_0, self.body_0, self.pop_0, self.traits_dup]
        self.spe_t4 = [self.food_0, self.body_0, self.pop_0, self.traits4]


class ExampleSpecies:
    def __init__(self):
        """ Creates a new ExampleSpecies with all of the example species initialized
        """
        self.ex_traits = ExampleTraits()

        self.spe_0 = Species(0, 0, 0, [])
        self.spe_1 = Species(1, 1, 1, [CarnivoreCard()])
        self.spe_max = Species(7, 7, 7, [CarnivoreCard(), AmbushCard(), BurrowingCard()])

        # Normal (trait-less) species
        self.norm_default = Species()
        self.norm_bstart3 = Species(body_size=(3 + SPECIES_START_BODY_SIZE))
        self.norm_bstart4 = Species(body_size=(4 + SPECIES_START_BODY_SIZE))
        self.norm_bstartshell = Species(body_size=(HARD_SHELL_OFFSET + SPECIES_START_BODY_SIZE))
        self.norm_bmax = Species(body_size=SPECIES_MAX_BODY_SIZE)
        self.norm_pstart2 = Species(population=(2 + SPECIES_START_POP))
        self.norm_bstart3_pstart2 = Species(body_size=(3 + SPECIES_START_BODY_SIZE),
                                            population=(2 + SPECIES_START_POP))
        self.norm_fed1_p2 = Species(fed_food=1, population=2)
        self.norm_fed3_p4 = Species(fed_food=3, population=4)

        # Carnivore species
        self.carn_default = Species(played_cards=[self.ex_traits.carn])
        self.carn_pstart1 = Species(population=1 + SPECIES_START_POP,
                                    played_cards=[self.ex_traits.carn])
        self.carn_pstart1_bstart3 = Species(population=1 + SPECIES_START_POP,
                                            body_size=3 + SPECIES_START_BODY_SIZE,
                                            played_cards=[self.ex_traits.carn])
        self.carnamb_default = Species(played_cards=[self.ex_traits.carn, self.ex_traits.amb])
        self.carnamb_pstart2 = Species(population=2 + SPECIES_START_POP,
                                       played_cards=[self.ex_traits.carn, self.ex_traits.amb])

        # Burrowing species
        self.burr_fstart_pstart = Species(fed_food=SPECIES_START_FOOD,
                                          population=SPECIES_START_POP,
                                          played_cards=[self.ex_traits.burr])
        self.burr_fstart1_pstart = Species(fed_food=1 + SPECIES_START_FOOD,
                                           population=SPECIES_START_POP,
                                           played_cards=[self.ex_traits.burr])
        self.burr_fstart2_pstart2 = Species(fed_food=2 + SPECIES_START_FOOD,
                                            population=2 + SPECIES_START_POP,
                                            played_cards=[self.ex_traits.burr])
        self.burr_fstart3_pstart2 = Species(fed_food=3 + SPECIES_START_FOOD,
                                            population=2 + SPECIES_START_POP,
                                            played_cards=[self.ex_traits.burr])

        # Climbing species
        self.climb_default = Species(played_cards=[self.ex_traits.climb])
        self.climb_default_2 = Species(played_cards=[self.ex_traits.climb])

        # Cooperation Species
        self.coop_default = Species(played_cards=[self.ex_traits.coop])
        self.carn_coop_default = Species(played_cards=[self.ex_traits.carn, self.ex_traits.coop])
        self.fora_coop_default = Species(fed_food=SPECIES_START_FOOD,
                                         population= SPECIES_MAX_POP,
                                         played_cards=[self.ex_traits.fora, self.ex_traits.coop])

        # Fat Tissue Species
        self.fat_default = Species(played_cards=[self.ex_traits.fat])
        self.fat_min = Species(body_size=4, played_cards=[self.ex_traits.fat_min])
        self.fat3 = Species(body_size=3, played_cards=[self.ex_traits.fat3])
        self.fat5 = Species(body_size=6, played_cards=[self.ex_traits.fat5])
        self.fat_max = Species(body_size=SPECIES_MAX_BODY_SIZE, played_cards=[self.ex_traits.fat_max])
        self.carn_fat_default = Species(played_cards=[self.ex_traits.carn, self.ex_traits.fat])
        self.carn_fat_coop_default = Species(
            played_cards=[self.ex_traits.carn, self.ex_traits.fat, self.ex_traits.coop])

        # Fef Fat Tissue Species
        self.fat5_fed1_b6 = Species(body_size=6, population=SPECIES_MAX_POP, played_cards=[self.ex_traits.fat5],
                                    fed_food=1)
        self.fat3_fed2_b5 = Species(body_size=5, population=SPECIES_MAX_POP, played_cards=[self.ex_traits.fat3],
                                    fed_food=2)
        self.fat_min_fedmax_bmax = Species(body_size=SPECIES_MAX_BODY_SIZE, population=SPECIES_MAX_POP,
                                           played_cards=[self.ex_traits.fat_min],
                                           fed_food=SPECIES_MAX_BODY_SIZE)
        self.fat_max_fed0_bmax = Species(body_size=SPECIES_MAX_BODY_SIZE,
                                         population=SPECIES_MAX_POP, played_cards=[self.ex_traits.fat_max],
                                         fed_food=SPECIES_MAX_BODY_SIZE)

        # Fat Species with the same Body - Fat already store
        self.fat5_bd6_popmax_food1 = Species(body_size=6,
                                             population=SPECIES_MAX_POP,
                                             played_cards=[self.ex_traits.fat5],
                                             fed_food=1)
        self.fat3_bd4_popmax_food1 = Species(body_size=4,
                                             population=SPECIES_MAX_POP,
                                             played_cards=[self.ex_traits.fat3],
                                             fed_food=1)
        self.fat3_bd4_pop4_food1 = Species(body_size=4,
                                           population=4,
                                           played_cards=[self.ex_traits.fat3],
                                           fed_food=1)
        self.fat3_bd4_pop4_food3 = Species(body_size=4,
                                           population=4,
                                           played_cards=[self.ex_traits.fat3],
                                           fed_food=3)

        # Foraging Species
        self.fora_default = Species(played_cards=[self.ex_traits.fora])
        self.carn_fora_default = Species(played_cards=[self.ex_traits.carn, self.ex_traits.fora])

        # Hard Shell species
        self.shell_default = Species(played_cards=[self.ex_traits.shell])
        self.shell_bstart3 = Species(body_size=3 + SPECIES_START_BODY_SIZE,
                                     played_cards=[self.ex_traits.shell])

        # Herding species
        self.herd_default = Species(played_cards=[self.ex_traits.herd])
        self.herd_pstart1 = Species(population=1 + SPECIES_START_POP,
                                    played_cards=[self.ex_traits.herd])
        self.herd_pstart2 = Species(population=2 + SPECIES_START_POP,
                                    played_cards=[self.ex_traits.herd])

        # Symbiosis species
        self.symb_default = Species(played_cards=[self.ex_traits.symb])
        self.symb_bstart3 = Species(body_size=3 + SPECIES_START_BODY_SIZE,
                                    played_cards=[self.ex_traits.symb])

        # Warning call
        self.warn_default = Species(played_cards=[self.ex_traits.warn])
        self.warn_default2 = Species(played_cards=[self.ex_traits.warn])

        # Pack Hunting species
        self.pack_bstart_pstart = Species(body_size=SPECIES_START_BODY_SIZE,
                                          population=SPECIES_START_POP,
                                          played_cards=[self.ex_traits.pack])
        self.pack_bstart_pstart2 = Species(body_size=SPECIES_START_BODY_SIZE,
                                           population=SPECIES_START_POP + 2,
                                           played_cards=[self.ex_traits.pack])
        self.pack_bstart3_pstart2 = Species(body_size=SPECIES_START_BODY_SIZE + 3,
                                            population=SPECIES_START_POP + 2,
                                            played_cards=[self.ex_traits.pack])

        # Scavenger Species
        self.scav_default = Species(played_cards=[self.ex_traits.scav])
        self.carn_scav_default = Species(played_cards=[self.ex_traits.scav, self.ex_traits.coop])

        # Horn Species
        self.horn_default = Species(played_cards=[self.ex_traits.horn])
        self.horn_pstart2 = Species(population=2 + SPECIES_START_POP,
                                    played_cards=[self.ex_traits.horn])

        # Fertile Species
        self.fertile_default = Species(played_cards=[self.ex_traits.fert])

        # Long Neck Species
        self.long_neck_default = Species(played_cards=[self.ex_traits.long])
