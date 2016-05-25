from evolution.cards.trait_card import *


class AmbushCard(TraitCard):
    def __init__(self, food_card_tokens: FoodCardTokens = NoFoodCardTokens) -> None:
        """
        :param food_card_tokens: The food tokens associated with this AmbushCard
        """
        TraitCard.__init__(self, food_card_tokens, "AmbushCard overcomes a Warning Call during an evolution.")

    @property
    def name(self) -> str:
        """ Get the name of this TraitCard """
        return "Ambush"

    def __eq__(self, other):
        return isinstance(other, AmbushCard) and TraitCard.__eq__(self, other)

    def __repr__(self):
        return "AmbushCard({})".format(self.food_card_tokens)


class WarningCallCard(TraitCard):
    def __init__(self, food_card_tokens: FoodCardTokens = NoFoodCardTokens) -> None:
        """
        :param food_card_tokens: The food tokens associated with this WarningCallCard
        """
        TraitCard.__init__(self, food_card_tokens,
                           "Warning Call prevents an attack from a Carnivore on both "
                           "neighboring species unless the attacker has the AmbushCard "
                           "property.")

    def blocks_attack(self,
                      defender:                 ISituationSpecies,
                      attacker:                 ISituationSpecies,
                      defenders_left_neighbor:  OptSituationSpecies = NoSituationSpecies,
                      defenders_right_neighbor: OptSituationSpecies = NoSituationSpecies,
                      owner_flag:               OptSituationFlag = NoSituationFlag) -> bool:
        """ Does this TraitCard block attacks from a given attacker and the defenders neighbors
        :param defender:                 The defending Species
        :param attacker:                 The attacking Carnivore
        :param defenders_left_neighbor:  The defender's left neighbor,
        :param defenders_right_neighbor: The defender's right neighbor
        :param owner_flag:               The owner of this Trait
        :return:                         True if this blocks attacks from the given attacker, False otherwise

        Invariants:
        owner_flag = DEFENDER_RIGHT_NEIGHBOR_FLAG => defenders_right_neighbor is not None
        owner_flag = DEFENDER_LEFT_NEIGHBOR_FLAG  => defenders_left_neighbor  is not None
        """
        return SituationFlag.is_defender_neighbor(owner_flag) and not attacker.has_trait(AmbushCard)

    @property
    def name(self) -> str:
        """ Get the name of this TraitCard """
        return "Warning Call"

    def __eq__(self, other):
        return isinstance(other, WarningCallCard) and TraitCard.__eq__(self, other)

    def __repr__(self):
        return "WarningCallCard({})".format(self.food_card_tokens)
