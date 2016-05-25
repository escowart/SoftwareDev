from evolution.species.species_interface import *


class OptSituationSpecies(metaclass=ABCMeta):
    """ An OptSituationSpecies is one of:
        - ISituationSpecies
        - OptSituationSpecies.NoSituationSpeciesClass
    """


class NoSituationSpeciesClass(OptSituationSpecies):
    """ A class representing a No Situation Species """
    def __eq__(self, other):
        return isinstance(other, NoSituationSpeciesClass)

NoSituationSpecies = NoSituationSpeciesClass()


class ISituationSpecies(OptSituationSpecies, metaclass=ABCMeta):
    """ An interface for Situation Species """

    @property
    def is_sit_species(self) -> bool:
        """ Is this a Situation Species? """
        return True

    @property
    @abstractmethod
    def num_food_tokens(self) -> Natural:
        """ Get the number of food tokens """
        raise NotImplementedError("num_food_tokens")

    @property
    @abstractmethod
    def population(self) -> Natural:
        """ Get the population of this Species """
        raise NotImplementedError("population")

    @property
    @abstractmethod
    def body_size(self) -> Natural:
        """ Get the body size of this Species """
        raise NotImplementedError("body_size")

    @property
    @abstractmethod
    def played_cards(self) -> List[PlayedCard]:
        """ Get the played cards on this Species """
        raise NotImplementedError("played_cards")

    @property
    @abstractmethod
    def trait_cards(self) -> List[ITraitCard]:
        """ Get the currently active traits of this Species """
        raise NotImplementedError("cards")

    @abstractmethod
    def has_trait(self, trait_type: type(ITraitCard)) -> bool:
        """ Does this ISpecies have the a Trait Card of the given type?
        :param trait_type: The Trait Card type
        :return: True if this has a Trait Card of the given type, False otherwise
        """
        raise NotImplementedError("has_trait")

    @property
    @abstractmethod
    def situation_position(self) -> SituationFlag:
        """ Get this Species' position in the Situation """
        raise NotImplementedError("situation_position")

    @situation_position.setter
    @abstractmethod
    def situation_position(self, situation_position: SituationFlag) -> None:
        """ Set this Species' position in the Situation """
        raise NotImplementedError("situation_position")

    @property
    @abstractmethod
    def is_sit_attacker(self) -> bool:
        """ Is this a Situation Attacker? """
        raise NotImplementedError("is_sit_attacker")

    @property
    @abstractmethod
    def is_sit_defender(self) -> bool:
        """ Is this a Situation Defender? """
        raise NotImplementedError("is_sit_defender")

    @property
    @abstractmethod
    def is_sit_defender_left_neighbor(self) -> bool:
        """ Is this a Situation Defender's Left Neighbor? """
        raise NotImplementedError("is_sit_defender_left_neighbor")

    @property
    @abstractmethod
    def is_sit_defender_right_neighbor(self) -> bool:
        """ Is this a Situation Defender's Right Neighbor? """
        raise NotImplementedError("is_sit_defender_right_neighbor")

