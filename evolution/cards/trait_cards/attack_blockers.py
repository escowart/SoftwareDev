from evolution.cards.trait_card import *


class BurrowingCard(TraitCard):
    def __init__(self, food_card_tokens: FoodCardTokens = NoFoodCardTokens) -> None:
        """
        :param food_card_tokens: The food tokens associated with this BurrowingCard
        """
        TraitCard.__init__(self, food_card_tokens, "BurrowingCard deflects an attack when its species has a food"
                                                   " supply equal to its population size.")

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
        return (owner_flag is SituationFlag.DEFENDER) and (defender.num_food_tokens == defender.population)

    @property
    def name(self) -> str:
        """ Get the name of this TraitCard """
        return "Burrowing"

    def __eq__(self, other):
        return isinstance(other, BurrowingCard) and TraitCard.__eq__(self, other)

    def __repr__(self):
        return "BurrowingCard({})".format(self.food_card_tokens)


class ClimbingCard(TraitCard):
    def __init__(self, food_card_tokens: FoodCardTokens = NoFoodCardTokens) -> None:
        """
        :param food_card_tokens: The food tokens associated with this ClimbingCard
        """
        TraitCard.__init__(self, food_card_tokens,
                           "ClimbingCard prevents an attack unless the Carnivore"
                           " also has the ClimbingCard attribute.")

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
        return owner_flag is SituationFlag.DEFENDER and not attacker.has_trait(ClimbingCard)

    @property
    def name(self) -> str:
        """ Get the name of this TraitCard """
        return "Climbing"

    def __eq__(self, other):
        return isinstance(other, ClimbingCard) and TraitCard.__eq__(self, other)

    def __repr__(self):
        return "ClimbingCard({})".format(self.food_card_tokens)


class HardShellCard(TraitCard):
    def __init__(self, food_card_tokens: FoodCardTokens = NoFoodCardTokens) -> None:
        """
        :param food_card_tokens: The food tokens associated with this HardShellCard
        """
        TraitCard.__init__(self, food_card_tokens,
                           "Hard Shell prevents an attack unless the attacker is "
                           "at least 4 units larger than this species in body size.")

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
        attacker_body_size = attacker.body_size
        defender_body_size = defender.body_size
        return owner_flag is SituationFlag.DEFENDER and ((attacker_body_size - defender_body_size) < HARD_SHELL_OFFSET)

    @property
    def name(self) -> str:
        """ Get the name of this TraitCard """
        return "Hard Shell"

    def __eq__(self, other):
        return isinstance(other, HardShellCard) and TraitCard.__eq__(self, other)

    def __repr__(self):
        return "HardShellCard({})".format(self.food_card_tokens)


class HerdingCard(TraitCard):
    def __init__(self, food_card_tokens: FoodCardTokens = NoFoodCardTokens) -> None:
        """
        :param food_card_tokens: The food tokens associated with this HerdingCard
        """
        TraitCard.__init__(self, food_card_tokens,
                           "Herding stops attacks from Carnivore species whose populations "
                           "are smaller or equal in size to this species population.")

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
        return (owner_flag is SituationFlag.DEFENDER) and (attacker.population <= defender.population)

    @property
    def name(self) -> str:
        """ Get the name of this TraitCard """
        return "Herding"

    def __eq__(self, other):
        return isinstance(other, HerdingCard) and TraitCard.__eq__(self, other)

    def __repr__(self):
        return "HerdingCard({})".format(self.food_card_tokens)


class SymbiosisCard(TraitCard):
    def __init__(self, food_card_tokens: FoodCardTokens = NoFoodCardTokens) -> None:
        """
        :param food_card_tokens: The food tokens associated with this SymbiosisCard
        """
        TraitCard.__init__(self, food_card_tokens,
                           "Symbiosis prevents an attack if this species has a neighbor to "
                           "the right whose body size is larger than this ones.")

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
        owner_flag = DEFENDER_RIGHT_NEIGHBOR_FLAG => defenders_right_neighbor.is_sit_species
        owner_flag = DEFENDER_LEFT_NEIGHBOR_FLAG  => defenders_left_neighbor.is_sit_species
        """
        if not (owner_flag is SituationFlag.DEFENDER) or (defenders_right_neighbor == NoSituationSpecies):
            return False

        right_neighbor = cast(ISituationSpecies, defenders_right_neighbor)
        return defender.body_size < right_neighbor.body_size

    @property
    def name(self) -> str:
        """ Get the name of this TraitCard """
        return "Symbiosis"

    def __eq__(self, other):
        return isinstance(other, SymbiosisCard) and TraitCard.__eq__(self, other)

    def __repr__(self):
        return "SymbiosisCard({})".format(self.food_card_tokens)
