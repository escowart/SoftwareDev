import unittest

from evo_tests.examples.ex_species import ExampleSpecies
from evolution.all_evo import *


class TestTraitCards(unittest.TestCase):
    def setUp(self):
        self.all_trait_classes = [CarnivoreCard, AmbushCard, BurrowingCard, ClimbingCard,
                                  HardShellCard, HerdingCard, SymbiosisCard, WarningCallCard,
                                  CooperationCard, FatTissueCard, FertileCard, ForagingCard,
                                  LongNeckCard, PackHuntingCard, ScavengerCard]
        self.classes_with_default_food_points = [x for x in self.all_trait_classes if
                                                 x != CarnivoreCard]
        self.classes_with_generic_atk_body_size = [x for x in self.all_trait_classes if
                                                   x != PackHuntingCard]
        self.classes_block_attacks = [BurrowingCard, ClimbingCard, HardShellCard, HerdingCard,
                                      SymbiosisCard,
                                      WarningCallCard]
        self.classes_cant_block_attacks = [x for x in self.all_trait_classes if
                                           x not in self.classes_block_attacks]

        self.ex_species = ExampleSpecies()

    def test_carnivore_constructor(self):
        for food_tokens in range(CARNIVORE_MIN_FOOD_TOKENS, CARNIVORE_MAX_FOOD_TOKENS + 1):
            carnivore = CarnivoreCard(food_tokens)
            self.assertEqual(carnivore.food_card_tokens, food_tokens,
                             "Carnivore " + str(food_tokens) + ": constructor-food_tokens")
            self.assertEqual(carnivore.description,
                             "CarnivoreCard must attack to eat during the evolution stage.")

    def test_rest_trait_card_constructors(self):
        for trait_class in self.classes_with_default_food_points:
            self._test_generic_trait_card_constructor(trait_class)

    def _test_generic_trait_card_constructor(self, trait_class):
        for food_tokens in range(TRAIT_CARD_MIN_FOOD_TOKENS, TRAIT_CARD_MAX_FOOD_TOKENS + 1):
            card = trait_class(cast(FoodCardTokens, food_tokens))  # type: TraitCard
            self.assertEqual(card.food_card_tokens, food_tokens)

        self.assertRaises(ValueError, trait_class, TRAIT_CARD_MAX_FOOD_TOKENS + 1)
        self.assertRaises(ValueError, trait_class, TRAIT_CARD_MIN_FOOD_TOKENS - 1)

    def _test_default_blocks_attacks(self):
        # TODO: FIX ALL THE SITUATIONSPECIES EXAMPLES
        for trait_class in self.classes_cant_block_attacks:
            trait_card1 = trait_class()  # type: TraitCard
            attacker = evolution.species.Species(played_cards=[CarnivoreCard(0)])
            defender = evolution.species.Species(played_cards=[trait_card1])
            self.assertEqual(trait_card1.blocks_attack(defender, attacker,
                                                       owner_flag=SituationFlag.DEFENDER), False)

    def _test_burrowing_blocks_attacks(self):
        # TODO: FIX ALL THE SITUATIONSPECIES EXAMPLES
        b_card = BurrowingCard(0)
        attacker = evolution.species.Species(played_cards=[CarnivoreCard(0)])
        defender_1 = evolution.species.Species(num_food_tokens=0, population=1, played_cards=[b_card])
        defender_2 = evolution.species.Species(num_food_tokens=1, population=1, played_cards=[b_card])
        defender_3 = evolution.species.Species(num_food_tokens=2, population=3, played_cards=[b_card])
        defender_4 = evolution.species.Species(num_food_tokens=3, population=3, played_cards=[b_card])

        self.assertEqual(b_card.blocks_attack(self.ex_species.burr_fstart_pstart, attacker,
                                              owner_flag=SituationFlag.DEFENDER),
                         SPECIES_START_FOOD == SPECIES_START_POP)
        self.assertEqual(b_card.blocks_attack(self.ex_species.burr_fstart1_pstart, attacker,
                                              owner_flag=SituationFlag.DEFENDER),
                         1 + SPECIES_START_FOOD == SPECIES_START_POP)
        self.assertEqual(b_card.blocks_attack(self.ex_species.burr_fstart2_pstart2, attacker,
                                              owner_flag=SituationFlag.DEFENDER),
                         2 + SPECIES_START_FOOD == 2 + SPECIES_START_POP)
        self.assertEqual(b_card.blocks_attack(self.ex_species.burr_fstart3_pstart2, attacker,
                                              owner_flag=SituationFlag.DEFENDER),
                         3 + SPECIES_START_FOOD == 2 + SPECIES_START_POP)

    def _test_climbing_blocks_attacks(self):
        # TODO: FIX ALL THE SITUATIONSPECIES EXAMPLES
        c_card0 = ClimbingCard(0)
        c_card1 = ClimbingCard(1)

        self.assertEqual(c_card1.blocks_attack(self.ex_species.climb_default,
                                               self.ex_species.climb_default_2,
                                               owner_flag=SituationFlag.DEFENDER),
                         False)
        self.assertEqual(c_card1.blocks_attack(self.ex_species.climb_default,
                                               self.ex_species.norm_default,
                                               owner_flag=SituationFlag.DEFENDER),
                         True)

    def test_hard_shell_blocks_attacks(self):
        hs_card = HardShellCard(0)
        attacker_0 = Species(body_size=0, played_cards=[CarnivoreCard(0)])
        attacker_3 = Species(body_size=3, played_cards=[CarnivoreCard(0)])
        attacker_4 = Species(body_size=4, played_cards=[CarnivoreCard(0)])
        attacker_7 = Species(body_size=7, played_cards=[CarnivoreCard(0)])
        defender_0 = Species(body_size=0, played_cards=[hs_card])
        defender_4 = Species(body_size=4, played_cards=[hs_card])

        self.assertEqual(hs_card.blocks_attack(self.ex_species.shell_default,
                                               self.ex_species.norm_default,
                                               owner_flag=SituationFlag.DEFENDER), True)
        # MAGIC CONSTANT TEST
        self.assertEqual(hs_card.blocks_attack(self.ex_species.shell_default,
                                               self.ex_species.norm_bstart3,
                                               owner_flag=SituationFlag.DEFENDER), True)

        self.assertEqual(hs_card.blocks_attack(self.ex_species.shell_default,
                                               self.ex_species.norm_bstartshell,
                                               owner_flag=SituationFlag.DEFENDER), False)

        self.assertEqual(hs_card.blocks_attack(self.ex_species.shell_default,
                                               self.ex_species.norm_bmax,
                                               owner_flag=SituationFlag.DEFENDER),
                         HARD_SHELL_OFFSET > SPECIES_MAX_POP - SPECIES_START_POP)

        self.assertEqual(hs_card.blocks_attack(self.ex_species.shell_bstart3,
                                               self.ex_species.norm_default,
                                               owner_flag=SituationFlag.DEFENDER), True)

    def test_herding_blocks_attacks(self):
        h_card = HerdingCard(0)
        self.assertEqual(h_card.blocks_attack(self.ex_species.herd_default,
                                              self.ex_species.carn_default,
                                              owner_flag=SituationFlag.DEFENDER), True)
        self.assertEqual(h_card.blocks_attack(self.ex_species.herd_default,
                                              self.ex_species.carn_pstart1,
                                              owner_flag=SituationFlag.DEFENDER), False)
        self.assertEqual(h_card.blocks_attack(self.ex_species.herd_pstart1,
                                              self.ex_species.carn_pstart1,
                                              owner_flag=SituationFlag.DEFENDER), True)
        self.assertEqual(h_card.blocks_attack(self.ex_species.herd_pstart2,
                                              self.ex_species.carn_pstart1,
                                              owner_flag=SituationFlag.DEFENDER), True)

    def test_symbiosis_blocks_attacks(self):
        card = SymbiosisCard(0)
        self.assertEqual(card.blocks_attack(self.ex_species.symb_default,
                                            self.ex_species.carn_default,
                                            NoSituationSpecies, self.ex_species.norm_default,
                                            owner_flag=SituationFlag.DEFENDER),
                         False)
        self.assertEqual(card.blocks_attack(self.ex_species.symb_default,
                                            self.ex_species.carn_default,
                                            NoSituationSpecies, self.ex_species.norm_bstart3,
                                            owner_flag=SituationFlag.DEFENDER),
                         True)
        self.assertEqual(card.blocks_attack(self.ex_species.symb_bstart3,
                                            self.ex_species.carn_default,
                                            NoSituationSpecies, self.ex_species.norm_bstart3,
                                            owner_flag=SituationFlag.DEFENDER),
                         False)
        self.assertEqual(card.blocks_attack(self.ex_species.symb_bstart3,
                                            self.ex_species.carn_default,
                                            NoSituationSpecies, self.ex_species.norm_bstart4,
                                            owner_flag=SituationFlag.DEFENDER),
                         True)
        self.assertEqual(card.blocks_attack(self.ex_species.symb_bstart3,
                                            self.ex_species.carn_default,
                                            NoSituationSpecies, self.ex_species.norm_default,
                                            owner_flag=SituationFlag.DEFENDER),
                         False)
        self.assertEqual(card.blocks_attack(self.ex_species.symb_bstart3,
                                            self.ex_species.carn_default,
                                            self.ex_species.norm_bstart4, NoSituationSpecies,
                                            owner_flag=SituationFlag.DEFENDER),
                         False)
        self.assertEqual(card.blocks_attack(self.ex_species.symb_bstart3,
                                            self.ex_species.carn_default,
                                            self.ex_species.norm_default, NoSituationSpecies,
                                            owner_flag=SituationFlag.DEFENDER),
                         False)

    def test_warning_call_blocks_attacks(self):
        warn_card = WarningCallCard()

        # Warn doesn't protect defender
        self.assertEqual(warn_card.blocks_attack(self.ex_species.warn_default,
                                                 self.ex_species.carn_default,
                                                 owner_flag=SituationFlag.DEFENDER), False)
        # Left defense
        self.assertEqual(warn_card.blocks_attack(self.ex_species.norm_default,
                                                 self.ex_species.carn_default,
                                                 self.ex_species.warn_default, NoSituationSpecies,
                                                 SituationFlag.DEFENDER_L_NEIGHBOR),
                         True)
        # Right defense
        self.assertEqual(warn_card.blocks_attack(self.ex_species.norm_default,
                                                 self.ex_species.carn_default,
                                                 NoSituationSpecies, self.ex_species.warn_default,
                                                 SituationFlag.DEFENDER_R_NEIGHBOR),
                         True)
        # Left defense ambushed
        self.assertEqual(warn_card.blocks_attack(self.ex_species.norm_default,
                                                 self.ex_species.carnamb_default,
                                                 self.ex_species.warn_default, NoSituationSpecies,
                                                 SituationFlag.DEFENDER_L_NEIGHBOR),
                         False)
        # Right defense ambushed
        self.assertEqual(warn_card.blocks_attack(self.ex_species.norm_default,
                                                 self.ex_species.carnamb_default,
                                                 NoSituationSpecies, self.ex_species.warn_default,
                                                 SituationFlag.DEFENDER_R_NEIGHBOR),
                         False)


if __name__ == '__main__':
    unittest.main()
