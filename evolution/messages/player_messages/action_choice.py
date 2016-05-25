from evo_json.serializers.py_json_serializers import *
from evolution.species.all_species import *


""" A GrowSpecies is a Tuple of the Species's index and the Gain Type it wants either GainPopulation or GainBody """
GrowSpecies = namedtuple('GrowSpecies', ['species_index', 'gain_type'])


class ActionChoice(Serializer, metaclass=ABCMeta):
    """ Represents the Action Choice being made by a Player
    An Action Choice is one of:
        - ChoiceFoodCard
        - GainPopulation
        - GainBody
        - GainBoard
        - ReplaceTrait
    """
    def __init__(self, card_index: Index):
        """ Construct an Action Choice
        :param card_index: The card index of this action choice"""
        self._card_index = Unset  # type: Index

        self.card_index = card_index

    def is_valid(self,
                 player:        IPlayer,
                 rem_hand:      RemovalList[ITraitCard],
                 watering_hole: IWateringHole) -> None:
        """ Is this Action Choice valid?
        :param player: The Player
        :param rem_hand: Hand with Removed Cards
        :param watering_hole: The Watering Hole
        """
        return rem_hand.has_unremoved_item_at_index(self.card_index)

    @abstractmethod
    def apply(self,
              player:        IPlayer,
              rem_hand:      RemovalList[ITraitCard],
              watering_hole: IWateringHole) -> None:
        """ Apply this Action Choice on the given Player State and its Hand with Removed Cards and the Watering Hole
        Effect: Changes the Player State according to this Choice
        :param player: The Player
        :param rem_hand: Hand with Removed Cards
        :param watering_hole: The Watering Hole
        """
        raise NotImplementedError("apply")

    @property
    def card_index(self) -> Index:
        """ Get the card index """
        return assert_set(self._card_index)

    @card_index.setter
    def card_index(self, card_index: Index) -> None:
        """ Set the card index """
        assert_type(card_index, of_type=Index, func_name="card_index")
        self._card_index = card_index


class FoodCardChoice(ActionChoice):
    """ Food Card Choice by the Player """

    def __repr__(self) -> str:
        return "FoodCardChoice({})".format(self.card_index)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, FoodCardChoice) and \
               self.card_index == cast(FoodCardChoice, other).card_index

    def apply(self,
              player:        IPlayer,
              rem_hand:      RemovalList[ITraitCard],
              watering_hole: IWateringHole) -> None:
        """ Apply this Action Choice on the given Player State and its Hand with Removed Cards and the Watering Hole
        Effect: Changes the Player State according to this Choice
        :param player: The Player
        :param rem_hand: Hand with Removed Cards
        :param watering_hole: The Watering Hole
        """
        food_card = rem_hand.pop(self.card_index)
        watering_hole.add_food_card_tokens(food_card)

    def serialize(self) -> PyJSON:
        """ Serialize this value into a its PyJSON equivalent?
        :return: The serialized JSON
        """
        return self.card_index

    @staticmethod
    def can_deserialize(py_json: PyJSON) -> bool:
        """ Can this Serializers deserialize the given PyJSON value?
        :param py_json: A PyJSON value
        :return: True if this can deserialize the given value, False otherwise
        """
        return is_index(py_json)

    @staticmethod
    def deserialize(py_json: PyJSON) -> 'FoodCardChoice':
        """ Deserialize the given value into a instance of this Serializer?
        :param py_json: A PyJSON value
        :return: An instance of this Deserialized
        """
        return FoodCardChoice(cast(int, py_json))


class GainSpeciesAttribute(ActionChoice, metaclass=ABCMeta):
    """ Gain a Species Attribute """
    def __init__(self, species_index: Index, card_index: Index, species_attribute: SpeciesAttribute) -> None:
        """ The action where you trade in a card for  population growth on a species
        :param species_index: the species that is being modified
        :param card_index: the card that is being traded
        :param species_attribute: The species attribute string
        """
        ActionChoice.__init__(self, card_index)
        self._species_index = Unset      # type: Index
        self._species_attribute = Unset  # type: SpeciesAttribute

        self.species_index = species_index
        self.species_attribute = species_attribute

    def serialize(self) -> PyJSON:
        """ Serialize this value into a its PyJSON equivalent?
        :return: The serialized JSON
        """
        return [self.species_index, self.card_index]

    @staticmethod
    def can_deserialize(py_json: PyJSON) -> bool:
        """ Can this Serializers deserialize the given PyJSON value?
        :param py_json: A PyJSON value
        :return: True if this can deserialize the given value, False otherwise
        """
        return is_list(py_json, of_type=Index, length=NEW_PJ_GP_AND_GB_LEN)

    def is_valid(self,
                 player: IPlayer,
                 rem_hand: RemovalList[ITraitCard],
                 watering_hole: IWateringHole) -> None:
        """ Is this Action Choice valid?
        :param player: The Player
        :param rem_hand: Hand with Removed Cards
        :param watering_hole: The Watering Hole
        """
        return ActionChoice.is_valid(self, player, rem_hand, watering_hole) and \
               player.has_species_at_index(self.species_index) and \
               player.can_add_to_attribute_of_species_at_index(GAIN_FOR_ATTRIBUTE,
                                                               self.species_attribute,
                                                               self.species_index)

    def apply(self,
              player: IPlayer,
              rem_hand: RemovalList[ITraitCard],
              watering_hole: IWateringHole) -> None:
        """ Apply this Action Choice on the given Player State and its Hand with Removed Cards and the Watering Hole
        Effect: Changes the Player State according to this Choice
        :param player: The Player
        :param rem_hand: Hand with Removed Cards
        :param watering_hole: The Watering Hole
        """
        rem_hand.pop(cast(int, self.card_index))
        species = player.species_list[self.species_index]
        self.species_attribute.add_to_attribute(species, GAIN_FOR_ATTRIBUTE)

    @property
    def species_index(self) -> Index:
        """ Get the species index """
        return assert_set(self._species_index)

    @species_index.setter
    def species_index(self, species_index: Index) -> None:
        """ Set the species index """
        assert_type(species_index, of_type=Index, func_name="species_index")
        self._species_index = species_index

    @property
    def species_attribute(self) -> SpeciesAttribute:
        """ Get the species attribute """
        return assert_set(self._species_attribute)

    @species_attribute.setter
    def species_attribute(self, species_attribute: SpeciesAttribute) -> None:
        """ Set the species attribute """
        assert_type(species_attribute, of_type=SpeciesAttribute, func_name="species_attribute")
        self._species_attribute = species_attribute

    def __repr__(self) -> str:
        return "{}({}, {})".format(name_of_class(self), self.species_index, self.card_index)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and \
               self.card_index == cast(self.__class__, other).card_index and \
               self.species_index == cast(self.__class__, other).species_index


class GainPopulation(GainSpeciesAttribute):
    """ A Gain Population Action Choice """
    def __init__(self, species_index: Index, card_index: Index) -> None:
        """ The action where you trade in a card for  population growth on a species
        :param species_index: the species that is being modified
        :param card_index: the card that is being traded
        """
        GainSpeciesAttribute.__init__(self, species_index, card_index, SpeciesPopulation())

    @staticmethod
    def deserialize(py_json: PyJSON) -> 'GainPopulation':
        """ Deserialize the given value into a instance of this Serializer?
        :param py_json: A PyJSON value
        :return: An instance of this Deserialized
        """
        return GainPopulation(py_json[0], py_json[1])


class GainBody(GainSpeciesAttribute):
    """ A Gain Body Action Choice """
    def __init__(self, species_index: Index, card_index: Index) -> None:
        """ The action where you trade in a card for  population growth on a species
        :param species_index: the species that is being modified
        :param card_index: the card that is being traded
        """
        GainSpeciesAttribute.__init__(self, species_index, card_index, SpeciesBodySize())

    @staticmethod
    def deserialize(py_json: PyJSON) -> 'GainBody':
        """ Deserialize the given value into a instance of this Serializer?
        :param py_json: A PyJSON value
        :return: An instance of this Deserialized
        """
        return GainBody(py_json[0], py_json[1])


class GainBoard(ActionChoice):
    def __init__(self, board_index: Index, trait_indices: List[Index]) -> None:
        """ Trade in a card for a species board
        :param board_index: The index of the card being traded in for a SpeciesBoard
        :param trait_indices: The Trait Card indices
        """
        ActionChoice.__init__(self, board_index)
        self._trait_indices = Unset  # type: List[Index]

        self.trait_indices = trait_indices

    def __repr__(self) -> str:
        return "GainBoard({}, {})".format(self.card_index, self.trait_indices)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, GainBoard) and \
               self.card_index == cast(GainBoard, other).card_index and \
               self.trait_indices == cast(GainBoard, other).trait_indices

    def is_valid(self,
                 player:        IPlayer,
                 rem_hand:      RemovalList[ITraitCard],
                 watering_hole: IWateringHole) -> None:
        """ Is this Action Choice valid?
        :param player: The Player
        :param rem_hand: Hand with Removed Cards
        :param watering_hole: The Watering Hole
        """
        return ActionChoice.is_valid(self, player, rem_hand, watering_hole) and \
            self.num_traits <= SPECIES_MAX_TRAITS_PER_SPECIES and \
            all(rem_hand.has_unremoved_item_at_index(trait_index) for trait_index in self.trait_indices) and \
            (not any_duplicates(self.trait_indices + [self.card_index]))

    @property
    def num_traits(self) -> Natural:
        """ Get the number of traits this New Species would possess """
        return len(self.trait_indices)

    def apply(self,
              player:        IPlayer,
              rem_hand:      RemovalList[ITraitCard],
              watering_hole: IWateringHole) -> None:
        """ Apply this Action Choice on the given Player State and its Hand with Removed Cards and the Watering Hole
        Effect: Changes the Player State according to this Choice
        :param player: The Player
        :param rem_hand: Hand with Removed Cards
        :param watering_hole: The Watering Hole
        """
        rem_hand.pop(self.card_index)
        new_species = Species(played_cards=self.get_traits(rem_hand))
        player.add_species(new_species)

    def get_traits(self, rem_hand: RemovalList[ITraitCard]) -> List[PlayedCard]:
        """ Get the traits of this Gain Boards given the hand
        Effect: Removed the traits from the hand
        :param rem_hand: The Hand of Removed cards
        :return: The list of Traits
        """
        return [rem_hand.pop(trait_index) for trait_index in self.trait_indices]

    def serialize(self) -> PyJSON:
        """ Serialize this value into a its PyJSON equivalent?
        :return: The serialized JSON
        """
        return [self.board_index] + self.trait_indices

    @staticmethod
    def can_deserialize(py_json: PyJSON) -> bool:
        """ Can this Serializers deserialize the given PyJSON value?
        :param py_json: A PyJSON value
        :return: True if this can deserialize the given value, False otherwise
        """
        return is_list(py_json, of_type=Index, min_len=MIN_PJ_BT_LEN, max_len=MAX_PJ_BT_LEN)

    @staticmethod
    def deserialize(py_json: PyJSON) -> 'GainBoard':
        """ Deserialize the given value into a instance of this Serializer?
        :param py_json: A PyJSON value
        :return: An instance of this Deserialized
        """
        return GainBoard(py_json[0], py_json[1:])

    @property
    def board_index(self) -> Index:
        """ Get the board index """
        return self.card_index

    @board_index.setter
    def board_index(self, board_index: Index) -> None:
        """ Set the board index """
        self.card_index = board_index

    @property
    def trait_indices(self) -> List[Index]:
        """ Get the trait indices """
        return assert_set(self._trait_indices)

    @trait_indices.setter
    def trait_indices(self, trait_indices: List[Index]) -> None:
        """ Set the trait indices """
        assert_type(trait_indices, list, of_type=Index, func_name="trait_indices")
        self._trait_indices = trait_indices


class ReplaceTrait(ActionChoice):
    def __init__(self,
                 species_index: Index,
                 trait_index:   Index,
                 card_index:    Index) -> None:
        """ Trade in a card for a species board
        :param species_index: the index of the species whose traits are going to be replaced
        :param trait_index: the index of the species trait being replaced
        :param card_index: the card being traded in for the replacement
        """
        ActionChoice.__init__(self, card_index)
        self._species_index = Unset  # Index
        self._trait_index = Unset    # Index

        self.species_index = species_index
        self.trait_index = trait_index

    def __repr__(self) -> str:
        return "ReplaceTrait({}, {}, {})".format(self.species_index, self.trait_index, self.card_index)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, ReplaceTrait) and \
               self.species_index == cast(ReplaceTrait, other).species_index and \
               self.trait_index == cast(ReplaceTrait, other).trait_index and \
               self.card_index == cast(ReplaceTrait, other).card_index

    def is_valid(self,
                 player:        IPlayer,
                 rem_hand:      RemovalList[ITraitCard],
                 watering_hole: IWateringHole) -> None:
        """ Is this Action Choice valid?
        :param player: The Player
        :param rem_hand: Hand with Removed Cards
        :param watering_hole: The Watering Hole
        """
        return ActionChoice.is_valid(self, player, rem_hand, watering_hole) and \
            player.has_species_at_index(self.species_index) and \
            player.species_at_index_has_trait_at_index(self.species_index, self.trait_index)

    def apply(self,
              player:        IPlayer,
              rem_hand:      RemovalList[ITraitCard],
              watering_hole: IWateringHole) -> None:
        """ Apply this Action Choice on the given Player State and its Hand with Removed Cards and the Watering Hole
        Effect: Changes the Player State according to this Choice
        :param player: The Player
        :param rem_hand: Hand with Removed Cards
        :param watering_hole: The Watering Hole
        """
        species = player.species_list[self.species_index]
        species.played_cards[self.trait_index] = rem_hand.pop(self.card_index)

    def serialize(self) -> PyJSON:
        """ Serialize this value into a its PyJSON equivalent?
        :return: The serialized JSON
        """
        return [self.species_index, self.trait_index, self.card_index]

    @staticmethod
    def can_deserialize(py_json: PyJSON) -> bool:
        """ Can this Serializers deserialize the given PyJSON value?
        :param py_json: A PyJSON value
        :return: True if this can deserialize the given value, False otherwise
        """
        return is_list(py_json, of_type=Index, length=PJ_RT_LEN)

    @staticmethod
    def deserialize(py_json: PyJSON) -> 'ReplaceTrait':
        """ Deserialize the given value into a instance of this Serializer?
        :param py_json: A PyJSON value
        :return: An instance of this Deserialized
        """
        return ReplaceTrait(*py_json)

    @property
    def species_index(self) -> Index:
        """ Get the species index """
        return assert_set(self._species_index)

    @species_index.setter
    def species_index(self, species_index: Index) -> None:
        """ Set the species index """
        assert_type(species_index, of_type=Index, func_name="species_index")
        self._species_index = species_index

    @property
    def trait_index(self) -> Index:
        """ Get the trait index """
        return assert_set(self._trait_index)

    @trait_index.setter
    def trait_index(self, trait_index: Index) -> None:
        """ Set the trait index """
        assert_type(trait_index, of_type=Index, func_name="trait_index")
        self._trait_index = trait_index