from evolution.species.all_species import *


class Situation(object):
    """ A class representing a Situation where the Attacking Carnivore is attempting to attack the Defender
    """

    def __init__(self,
                 defender:                Species,
                 attacker:                Carnivore,
                 defender_left_neighbor:  OptSpecies=NoSpecies,
                 defender_right_neighbor: OptSpecies=NoSpecies) -> None:
        """ Construct a Situation
        :param defender: The defender in the Situation
        :param attacker: The attacker in the Situation
        :param defender_left_neighbor: The left neighbor of the defender
        :param defender_right_neighbor: The right neighbor of the defender
        """

        if not Species.is_extant_species(defender):
            raise ValueError("Situation: Invalid Extant Species as defender, got: {}".format(defender))
        elif not Species.is_extant_carnivore(attacker):
            raise ValueError("Situation: Invalid Extant Carnivore as attacker, got: {}".format(attacker))
        elif not Species.is_opt_extant_species(defender_left_neighbor):
            raise ValueError("Situation: Invalid Optional Extant Species as defender_left_neighbor, got: {}"
                             .format(defender_left_neighbor))
        elif not Species.is_opt_extant_species(defender_right_neighbor):
            raise ValueError("Situation: Invalid Optional Extant Species as defender_right_neighbor, got: {}"
                             .format(defender_right_neighbor))

        self.defender = defender                                # type: Species
        self.attacker = attacker                                # type: Carnivore
        self.defender_left_neighbor = defender_left_neighbor    # type: Optional[Species]
        self.defender_right_neighbor = defender_right_neighbor  # type: Optional[Species]

    def is_defender_attackable(self) -> bool:
        """ Is the Situation defender attackable by attacker given the defender's neighbors?
        :return: True if the defender is attackable, False otherwise
        """
        return self.defender.is_attackable(self.attacker, self.defender_left_neighbor, self.defender_right_neighbor)

    def __repr__(self):
        return "Situation({}, {}, {}, {})".format(self.defender,
                                                  self.attacker,
                                                  self.defender_left_neighbor,
                                                  self.defender_right_neighbor)

    def __eq__(self, other):
        return isinstance(other, Situation) and \
               self.defender == cast(Situation, other).defender and \
               self.attacker == cast(Situation, other).attacker and \
               self.defender_left_neighbor == cast(Situation, other).defender_left_neighbor and \
               self.defender_right_neighbor == cast(Situation, other).defender_right_neighbor