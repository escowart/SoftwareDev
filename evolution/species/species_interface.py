from evolution.card_holders.watering_hole_interface import *
from evolution.card_holders.deck_interface import *


class NoSpeciesClass(NoValue):
    """ The No-Species Type """

NoSpecies = NoSpeciesClass()


OptSpecies = Union['ISpecies', NoSpeciesClass]


class SpeciesAttribute(object, metaclass=ABCMeta):
    """ A Species Attribute """

    def can_add_to_attribute(self, species: 'ISpecies', amount_to_add: Natural) -> bool:
        """ Can this Species Attribute add the given amount to the given species's?
        :param species: The Species
        :param amount_to_add: The amount being added
        :return: True if the amount can be added, False otherwise
        """
        return (self.species_attribute_value(species) + amount_to_add) <= self.max_value

    @abstractmethod
    def species_attribute_value(self, species: 'ISpecies') -> Natural:
        """ Get the value of the attribute for the given species
        :param species: The species
        :return: The value of that attribute
        """
        raise NotImplementedError("species_value")

    @property
    @abstractmethod
    def max_value(self) -> Natural:
        """ The maximum value this Attribute can be"""
        raise NotImplementedError("max_value")

    def add_to_attribute(self, species: 'ISpecies', amount_to_add: Natural) -> None:
        """ Add the given amount to this Attribute within the Species
        Effect: Modifies the attribute within the Species
        :param species: The Species
        :param amount_to_add: The amount being added
        """
        raise NotImplementedError("add_to_attribute")


class SpeciesPopulation(SpeciesAttribute):
    """ A class representing the Population of a Species """
    def species_attribute_value(self, species: 'ISpecies') -> Natural:
        """ Get the value of the attribute for the given species
        :param species: The species
        :return: The value of that attribute
        """
        return species.population

    @property
    def max_value(self) -> Natural:
        """ The maximum value this Attribute can be"""
        return SPECIES_MAX_POP

    def add_to_attribute(self, species: 'ISpecies', amount_to_add: Natural) -> None:
        """ Add the given amount to this Attribute within the Species
        Effect: Modifies the attribute within the Species
        :param species: The Species
        :param amount_to_add: The amount being added
        """
        species.population += amount_to_add


class SpeciesBodySize(SpeciesAttribute):
    """ A class representing the Body Size of a Species """
    def species_attribute_value(self, species: 'ISpecies') -> Natural:
        """ Get the value of the attribute for the given species
        :param species: The species
        :return: The value of that attribute
        """
        return species.body_size

    @property
    def max_value(self) -> Natural:
        """ The maximum value this Attribute can be"""
        return SPECIES_MAX_BODY_SIZE

    def add_to_attribute(self, species: 'ISpecies', amount_to_add: Natural) -> None:
        """ Add the given amount to this Attribute within the Species
        Effect: Modifies the attribute within the Species
        :param species: The Species
        :param amount_to_add: The amount being added
        """
        species.body_size += amount_to_add


class ISpecies(object, metaclass=ABCMeta):
    """ A Species Interface for all the TraitCard"""

    @property
    @abstractmethod
    def fed_food(self) -> Natural:
        """ Get the number of food tokens fed """
        raise NotImplementedError("num_food_tokens")

    @fed_food.setter
    @abstractmethod
    def fed_food(self, num_food_tokens: Natural) -> None:
        """ Set the number of food tokens fed """
        raise NotImplementedError("num_food_tokens")

    @property
    @abstractmethod
    def population(self) -> Natural:
        """ Get the population of this Species """
        raise NotImplementedError("population")

    @population.setter
    @abstractmethod
    def population(self, population: Natural) -> None:
        """ Set the population of this Species
        Effect: Modifies the num_food_tokens to population if it exceeds the new population
        """
        raise NotImplementedError("population")

    @property
    @abstractmethod
    def body_size(self) -> Natural:
        """ Get the body size of this Species """
        raise NotImplementedError("body_size")

    @body_size.setter
    @abstractmethod
    def body_size(self, body_size: Natural) -> None:
        """ Set the body_size of this Species """
        raise NotImplementedError("body_size")

    @property
    @abstractmethod
    def played_cards(self) -> List[PlayedCard]:
        """ Get the played cards on this Species """
        raise NotImplementedError("played_cards")

    @played_cards.setter
    @abstractmethod
    def played_cards(self, played_cards: OptList[PlayedCard] = NoList) -> None:
        """ Set the played cards on this Species """
        raise NotImplementedError("played_cards")

    @property
    @abstractmethod
    def trait_cards(self) -> List[ITraitCard]:
        """ Get the currently active traits of this Species """
        raise NotImplementedError("trait_cards")

    @abstractmethod
    def has_trait(self, trait_type: type(ITraitCard)) -> bool:
        """ Does this ISpecies have the a Trait Card of the given type?
        :param trait_type: The Trait Card type
        :return: True if this has a Trait Card of the given type, False otherwise
        """
        raise NotImplementedError("has_trait")

    @property
    @abstractmethod
    def is_hungry(self) -> bool:
        """ Is this Species hungry? """
        raise NotImplementedError("is_hungry")

    @abstractmethod
    def can_store(self, fat_to_store: Natural) -> bool:
        """ Can the given amount of food be stored as Fat Tissue?
        :param fat_to_store: The fat to store
        :return: True if this Species can store the given amount of food, False otherwise
        """
        raise NotImplementedError("can_store")

    @abstractmethod
    def store_fat(self, fat_to_store: Natural) -> None:
        """ Store the given amount of Fat in your Fat Tissue
        :param fat_to_store: The Fat to Store
        """
        raise NotImplementedError("store_fat")

    @abstractmethod
    def is_attackable(self,
                      attacker: 'ISpecies',
                      defenders_left_neighbor:  OptSpecies = NoSpecies,
                      defenders_right_neighbor: OptSpecies = NoSpecies) -> bool:
        """ Can the given attacker attack the given defender given the defender's left and right neighbors?
        :param attacker:                 The attacking Carnivore
        :param defenders_left_neighbor:  The defender's left neighbor
        :param defenders_right_neighbor: The defender's right neighbor
        :return: True if the defender is attackable by the attacker, False otherwise
        """
        raise NotImplementedError("is_hungry")

    @abstractmethod
    def feed(self, species_index: Index, player_state, watering_hole: IWateringHole) -> None:
        """ Feed the Species at the given index within the given Player State and feed any in the Cooperation Chain
        Effect: Modifies the Species and any other species that are affected by its feeding
        :param species_index: The index of the Species
        :param player_state: The Player State
        :param watering_hole: The Watering Hole
        """
        raise NotImplementedError("feed")

    @abstractmethod
    def attack(self,
               owner_player,
               index_of_self: Index,
               target_player,
               index_of_target: Index,
               deck: IDeck) -> None:
        """ Have this Carnivore attack the Species at the given index within the target PlayerState
        Effect: Modifies the target species's attributes or its own attributes if the target has horns
        :param owner_player: owner of this species
        :param index_of_self: where this species is in its external_players's species list
        :param target_player: target species's owner
        :param index_of_target: where the target species is in its owner's list
        :param deck: The deck of cards the dealers holds
        """
        raise NotImplementedError("attack")

    @abstractmethod
    def reduce_population(self,
                          damage:               NaturalPlus,
                          owner,
                          index_of_self:        Index,
                          deck:                 IDeck,
                          species_list:         OptList['ISpecies'] = NoList) -> None:
        """ Reduces this species population by given amount of damage.
            If this species goes extinct from the damage,
                then the species is removed from its Player State's species_list and Player State draws cards
        Effect: Modifies this species by reducing it population by the given amount,
                 and the number of food tokens this species holds to be no greater than the population
                If this species goes extinct,
                    then its Player State is Modified by removing this Species from its species_list
                     and the deck is Modified by removing cards to put in the Player State's hand
        :param damage: Amount of damage received
        :param owner: The owner PlayerState of this species
        :param index_of_self: The index of this species in its owning Player's species_list
        :param deck: The deck of cards the dealers holds
        :param species_list: The Species OptList being iterated over
        """
        raise NotImplementedError("reduce_population")

    @abstractmethod
    def reduce_by_unfed_population(self,
                                   owner,
                                   index_of_self:        Index,
                                   deck:                 IDeck,
                                   species_list:         IList['ISpecies']) -> None:
        """ Reduces this species population to match its number of food tokens.
            If this species goes extinct from the damage,
                then the species is removed from its Player State's species_list and Player State draws cards
        Effect: Modifies this species by reducing it population by the given amount
                If this species goes extinct,
                    then its Player State is Modified by removing this Species from its species_list
                     and the deck is Modified by removing cards to put in the Player State's hand
        :param owner: The owner PlayerState of this species
        :param index_of_self: The index of this species in its owning Player's species_list
        :param deck: The deck of cards the dealers holds
        :param species_list: The Species List being iterated over
        """
        raise NotImplementedError("reduce_by_unfed_population")

    @property
    @abstractmethod
    def is_vegetarian(self) -> bool:
        """ Is this Species a Vegetarian? """
        raise NotImplementedError("is_vegetarian")

    @property
    @abstractmethod
    def is_extant(self) -> bool:
        """ Is this Species extant? """
        raise NotImplementedError("is_extant")

