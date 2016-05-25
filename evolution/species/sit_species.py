from evolution.species.neighbor_iter import *


class SituationSpecies(ISituationSpecies):
    """ A class representing a Situation Species which is what a Species is when it is being check whether a Species
        is attackable """
    def __init__(self, species: ISpecies, situation_position: OptSituationFlag=NoSituationFlag) -> None:
        """ Construct a Situation Species
        :param species: The Species
        :param situation_position: The position in the situation
        """
        self._species = Unset             # type: ISpecies
        self._situation_position = Unset  # type: OptSituationFlag

        self.species = species
        self.situation_position = situation_position

    @property
    def species(self) -> ISpecies:
        """ Get this Species in the Situation """
        return assert_set(self._species)

    @species.setter
    def species(self, species: ISpecies) -> None:
        """ Set this Species in the Situation """
        assert_type(species, of_type=ISpecies, func_name="species")
        self._species = species

    @property
    def situation_position(self) -> SituationFlag:
        """ Get this Species' position in the Situation """
        return assert_set(self._situation_position)

    @situation_position.setter
    def situation_position(self, situation_position: OptSituationFlag) -> None:
        """ Set this Species' position in the Situation """
        if situation_position != NoSituationFlag:
            assert_type(situation_position, of_type=SituationFlag, func_name="situation_position")

        self._situation_position = situation_position

    @property
    def num_food_tokens(self) -> Natural:
        """ Get the number of food tokens """
        return self.species.fed_food

    @property
    def population(self) -> Natural:
        """ Get the population of this Species """
        return self.species.population

    @property
    def body_size(self) -> Natural:
        """ Get the body size of this Species """
        if self.is_sit_attacker and self.has_trait(PackHuntingCard):
            return self.population + self.species.body_size
        else:
            return self.species.body_size

    @property
    def played_cards(self) -> List[PlayedCard]:
        """ Get the played cards on this Species """
        return self.species.played_cards

    @property
    def trait_cards(self) -> List[ITraitCard]:
        """ Get the currently active traits of this Species """
        return self.species.trait_cards

    def has_trait(self, trait_type: type(ITraitCard)) -> bool:
        """ Does this ISpecies have the a Trait Card of the given type?
        :param trait_type: The Trait Card type
        :return: True if this has a Trait Card of the given type, False otherwise
        """
        return self.species.has_trait(trait_type)

    def __repr__(self):
        return "SituationSpecies({})".format(self.species, self.situation_position)

    def __eq__(self, other):
        return isinstance(other, SituationSpecies) and \
               self.species == cast(SituationSpecies, other).species and \
               self.situation_position == cast(SituationSpecies, other).situation_position

    @property
    def is_sit_attacker(self) -> bool:
        """ Is this a Situation Attacker? """
        return self.situation_position is SituationFlag.ATTACKER

    @property
    def is_sit_defender(self) -> bool:
        """ Is this a Situation Defender? """
        return self.situation_position is SituationFlag.DEFENDER

    @property
    def is_sit_defender_left_neighbor(self) -> bool:
        """ Is this a Situation Defender's Left Neighbor? """
        return self.situation_position is SituationFlag.DEFENDER_L_NEIGHBOR

    @property
    def is_sit_defender_right_neighbor(self) -> bool:
        """ Is this a Situation Defender's Right Neighbor? """
        return self.situation_position is SituationFlag.DEFENDER_R_NEIGHBOR

