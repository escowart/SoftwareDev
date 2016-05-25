from evo_tests.util import *


class ExamplePJTraits:
    def __init__(self):
        self.carnivore = CARNIVORE_STR
        self.ambush = AMBUSH_STR
        self.burrowing = BURROWING_STR
        self.climbing = CLIMBING_STR
        self.cooperation = COOPERATION_STR
        self.fat_tissue = FAT_TISSUE_STR
        self.fertile = FERTILE_STR
        self.foraging = FORAGING_STR
        self.hard_shell = HARD_SHELL_STR
        self.herding = HERDING_STR
        self.horns = HORNS_STR
        self.long_neck = LONG_NECK_STR
        self.pack_hunting = PACK_HUNTING_STR
        self.scavenger = SCAVENGER_STR
        self.symbiosis = SYMBIOSIS_STR
        self.warning_call = WARNING_CALL_STR


class ExamplePJLOT:
    def __init__(self):
        self.ex_traits = ExampleTraits()
        self.ex_pj_traits = ExamplePJTraits()

        self.lot0 = []
        self.lot1 = [self.ex_pj_traits.carnivore]
        self.lot2 = [self.ex_pj_traits.carnivore, self.ex_pj_traits.ambush]
        self.lot3 = [self.ex_pj_traits.carnivore, self.ex_pj_traits.ambush, self.ex_pj_traits.burrowing]
        self.lot4 = [self.ex_pj_traits.carnivore, self.ex_pj_traits.ambush,
                     self.ex_pj_traits.burrowing, self.ex_pj_traits.climbing]
        self.lot_dup = [self.ex_pj_traits.carnivore, self.ex_pj_traits.ambush, self.ex_pj_traits.carnivore]


class ExampleTraitTypes:
    def __init__(self):
        self.horn_type = HornCard
        self.carn_type = CarnivoreCard
        self.amb_type = AmbushCard
        self.burr_type = BurrowingCard
        self.climb_type = ClimbingCard
        self.shell_type = HardShellCard
        self.herd_type = HerdingCard
        self.symb_type = SymbiosisCard
        self.warn_type = WarningCallCard
        self.coop_type = CooperationCard
        self.fat_type = FatTissueCard
        self.fert_type = FertileCard
        self.fora_type = ForagingCard
        self.long_type = LongNeckCard
        self.pack_type = PackHuntingCard
        self.scav_type = ScavengerCard

        self.all_trait_types = [self.horn_type,
                                self.carn_type,
                                self.amb_type,
                                self.burr_type,
                                self.climb_type,
                                self.shell_type,
                                self.herd_type,
                                self.symb_type,
                                self.warn_type,
                                self.coop_type,
                                self.fat_type,
                                self.fert_type,
                                self.fora_type,
                                self.long_type,
                                self.pack_type,
                                self.scav_type]


class ExampleTraits:
    def __init__(self):
        self.ex_trait_types = ExampleTraitTypes()

        """ Creates a new set of example TraitCards
        """
        self.horn = self.ex_trait_types.horn_type()
        self.carn = self.ex_trait_types.carn_type()
        self.amb = self.ex_trait_types.amb_type()
        self.burr = self.ex_trait_types.burr_type()
        self.climb = self.ex_trait_types.climb_type()
        self.shell = self.ex_trait_types.shell_type()
        self.herd = self.ex_trait_types.herd_type()
        self.symb = self.ex_trait_types.symb_type()
        self.warn = self.ex_trait_types.warn_type()
        self.coop = self.ex_trait_types.coop_type()
        self.fat = self.ex_trait_types.fat_type()
        self.fat_min = self.ex_trait_types.fat_type(stored_food=SPECIES_MIN_BODY_SIZE)
        self.fat3 = self.ex_trait_types.fat_type(stored_food=3)
        self.fat5 = self.ex_trait_types.fat_type(stored_food=5)
        self.fat_max = self.ex_trait_types.fat_type(stored_food=SPECIES_MAX_BODY_SIZE)
        self.fert = self.ex_trait_types.fert_type()
        self.fora = self.ex_trait_types.fora_type()
        self.long = self.ex_trait_types.long_type()
        self.pack = self.ex_trait_types.pack_type()
        self.scav = self.ex_trait_types.scav_type()

        self.all_trait_classes = [CarnivoreCard, AmbushCard, BurrowingCard, ClimbingCard,
                                  HardShellCard, HerdingCard,
                                  SymbiosisCard, WarningCallCard, CooperationCard, FatTissueCard,
                                  FertileCard,
                                  ForagingCard, LongNeckCard, PackHuntingCard, ScavengerCard]
        self.classes_with_default_food_points = [x for x in self.all_trait_classes if
                                                 x != CarnivoreCard]
        self.classes_with_generic_atk_body_size = [x for x in self.all_trait_classes if
                                                   x != PackHuntingCard]
        self.classes_block_attacks = [BurrowingCard, ClimbingCard, HardShellCard, HerdingCard,
                                      SymbiosisCard,
                                      WarningCallCard]
        self.classes_cant_block_attacks = [x for x in self.all_trait_classes if
                                           x not in self.classes_block_attacks]


class ExampleTraitList:
    def __init__(self):
        self.ex_traits = ExampleTraits()

        self.lot0 = []
        self.lot1 = [self.ex_traits.carn]
        self.lot2 = [self.ex_traits.carn, self.ex_traits.amb]
        self.lot3 = [self.ex_traits.carn, self.ex_traits.amb, self.ex_traits.burr]
        self.lot4 = [self.ex_traits.carn, self.ex_traits.amb, self.ex_traits.burr, self.ex_traits.climb]