from evolution.cards.trait_cards.attack_blockers import *
from evolution.cards.trait_cards.body_actors import *
from evolution.cards.trait_cards.carnivore import *
from evolution.cards.trait_cards.defence_actors import *
from evolution.cards.trait_cards.fat_tissue import *
from evolution.cards.trait_cards.feed_actors import *
from evolution.cards.trait_cards.pop_actors import *
from evolution.cards.trait_cards.warning_ambush import *

CARNIVORE_TYPE = CarnivoreCard
AMBUSH_TYPE = AmbushCard
BURROWING_TYPE = BurrowingCard
CLIMBING_TYPE = ClimbingCard
COOPERATION_TYPE = CooperationCard
FAT_TISSUE_TYPE = FatTissueCard
FERTILE_TYPE = FertileCard
FORAGING_TYPE = ForagingCard
HARD_SHELL_TYPE = HardShellCard
HERDING_TYPE = HerdingCard
HORNS_TYPE = HornCard
LONG_NECK_TYPE = LongNeckCard
PACK_HUNTING_TYPE = PackHuntingCard
SCAVENGER_TYPE = ScavengerCard
SYMBIOSIS_TYPE = SymbiosisCard
WARNING_CALL_TYPE = WarningCallCard

trait_dictionary = {
    CARNIVORE_STR: CARNIVORE_TYPE,
    AMBUSH_STR: AMBUSH_TYPE,
    BURROWING_STR: BURROWING_TYPE,
    CLIMBING_STR: CLIMBING_TYPE,
    COOPERATION_STR: COOPERATION_TYPE,
    FAT_TISSUE_STR: FAT_TISSUE_TYPE,
    FERTILE_STR: FERTILE_TYPE,
    FORAGING_STR: FORAGING_TYPE,
    HARD_SHELL_STR: HARD_SHELL_TYPE,
    HERDING_STR: HERDING_TYPE,
    HORNS_STR: HORNS_TYPE,
    LONG_NECK_STR: LONG_NECK_TYPE,
    PACK_HUNTING_STR: PACK_HUNTING_TYPE,
    SCAVENGER_STR: SCAVENGER_TYPE,
    SYMBIOSIS_STR: SYMBIOSIS_TYPE,
    WARNING_CALL_STR: WARNING_CALL_TYPE
}   #  type: Dict[PJ_Trait, Callable[[], type(TraitCard)]]