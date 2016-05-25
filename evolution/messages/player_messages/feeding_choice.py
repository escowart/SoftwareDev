from evolution.messages.player_messages.feeding import *
from evolution.messages.player_messages.player_response import *

OptValidFeedingChoice = Union['InvalidFeedingChoiceClass', 'FeedingChoice']


class InvalidFeedingChoiceClass(NoValue):
    """ The No-type for FeedingChoice """

InvalidFeedingChoice = InvalidFeedingChoiceClass()


class FeedingChoice(PlayerResponse, metaclass=ABCMeta):
    """ Represents the Feeding Choice being made by the SimplePlayer
    A FeedingChoice is one of:
        - ForgoChoice
        - FeedVegetarianChoice
        - StoreFatChoice
        - AttackWithCarnivoreChoice
    """

    @abstractmethod
    def is_valid(self, player_sequence: IPlayerSequence, player_state: IPlayer) -> bool:
        """ Is this Choice valid given the dealers and the State of the Player who gave the dealers this?
        :param player_sequence: The PlayerSequence
        :param player_state: The Player's State
        :return True if valid, False otherwise
        """
        raise NotImplementedError("is_valid")

    @abstractmethod
    def apply(self, dealer: IDealer, player: IPlayer) -> None:
        """ Apply this Choice to given the dealers and the State of the Player who gave the dealers this?
        Effect: Modifies the Player and Dealer according to this Choice
        :param dealer: The dealers
        :param player: The Player
        """
        raise NotImplementedError("apply")

    @abstractmethod
    def to_data(self, feeding: Feeding) -> DataFeedingChoice:
        """ Convert this Feeding Choice into a Data Feeding Choice
        :feeding: The Feeding
        :param feeding: The Feeding
        :return: this as a Data Feeding Choice
        """
        raise NotImplementedError("to_data")

    @staticmethod
    def can_deserialize(py_json: PyJSON) -> bool:
        """ Can this Serializers deserialize the given PyJSON value?
        :param py_json: A PyJSON value
        :return: True if this can deserialize the given value, False otherwise
        """
        return any(choice_type.can_deserialize(py_json) for choice_type in FeedingChoice.all_feeding_choices_types())

    @staticmethod
    def deserialize(py_json: PyJSON) -> 'FeedingChoice':
        """ Deserialize the given value into a instance of this Serializer?
        :param py_json: A PyJSON value
        :return: An instance of this Deserialized
        """
        for choice_type in FeedingChoice.all_feeding_choices_types():
            if choice_type.can_deserialize(py_json):
                return choice_type.deserialize(py_json)

        raise Exception("deserialize: Feeding Choice cannot deserialize {}".format(py_json))

    @staticmethod
    def all_feeding_choices_types() -> List[type('FeedingChoice')]:
        """ Get all Feeding Choices types """
        return [ForgoChoice, FeedVegetarianChoice, StoreFatChoice, AttackWithCarnivoreChoice]


class ForgoChoice(FeedingChoice):
    """ Forgo a Feeding Choice """
    def is_valid(self, dealer: IDealer, player: IPlayer) -> bool:
        """ Is this Forgo Choice from the given player valid?
        :param dealer: The Dealer of the Game
        :param player: The Player whose response is being validated
        """
        return player.can_any_species_attack_or_store(dealer.player_sequence)

    def apply(self, dealer: IDealer, player: IPlayer) -> None:
        """ Apply this Choice to given the dealers and the State of the Player who gave the dealers this?
        Effect: Modifies the Player and Dealer according to this Choice
        :param dealer: The dealers
        :param player: The Player
        """
        player.has_forgon_this_turn = HAS_FORGON

    def to_data(self, feeding: Feeding) -> DataFeedingChoice:
        """ Convert this Feeding Choice into a Data Feeding Choice
        :param feeding: The Feeding
        :return: this as a Data Feeding Choice
        """
        return DataForgoChoice()

    def serialize(self) -> PyJSON:
        """ Serialize this value into a its PyJSON equivalent?
        :return: The serialized JSON
        """
        return False

    @staticmethod
    def can_deserialize(py_json: PyJSON) -> bool:
        """ Can this Serializers deserialize the given PyJSON value?
        :param py_json: A PyJSON value
        :return: True if this can deserialize the given value, False otherwise
        """
        return is_instance(py_json, bool) and (py_json == False)

    @staticmethod
    def deserialize(py_json: PyJSON) -> 'ForgoChoice':
        """ Deserialize the given value into a instance of this Serializer?
        :param py_json: A PyJSON value
        :return: An instance of this Deserialized
        """
        return ForgoChoice()

    def __repr__(self):
        return "{}()".format(name_of_class(self))

    def __eq__(self, other):
        return isinstance(other, ForgoChoice)


class FeedVegetarianChoice(FeedingChoice):
    """ A Feeding Vegetarian Choice """
    def __init__(self, vegetarian_index: Index) -> None:
        """ Construct a Feed Vegetarian Choice
        :param vegetarian_index: The vegitarian index
        """
        self._vegetarian_index = Unset  # type: Index

        self.vegetarian_index = vegetarian_index

    def is_valid(self, dealer: IDealer, player: IPlayer) -> bool:
        """ Is this Feed Vegetarian Choice from the given player valid?
        :param dealer: The Dealer of the Game
        :param player: The Player whose response is being validated
        """
        species = player.species_list[self.vegetarian_index]
        return species.is_hungry and species.is_vegetarian

    def apply(self, dealer: IDealer, player: IPlayer) -> None:
        """ Apply this Choice to given the dealers and the State of the Player who gave the dealers this?
        Effect: Modifies the Player and Dealer according to this Choice
        :param dealer: The dealers
        :param player: The Player's State
        """
        dealer.feed_species(self.vegetarian_index, player)

    def to_data(self, feeding: Feeding) -> DataFeedingChoice:
        """ Convert this Feeding Choice into a Data Feeding Choice
        :param feeding: The Feeding
        :return: this as a Data Feeding Choice
        """
        veg_index = self.vegetarian_index
        vegetarian = feeding.player.get_species_at_index(veg_index)
        return DataFeedVegetarian(vegetarian)

    def serialize(self) -> PyJSON:
        """ Serialize this value into a its PyJSON equivalent?
        :return: The serialized JSON
        """
        return self.vegetarian_index

    @staticmethod
    def can_deserialize(py_json: PyJSON) -> bool:
        """ Can this Serializers deserialize the given PyJSON value?
        :param py_json: A PyJSON value
        :return: True if this can deserialize the given value, False otherwise
        """
        return is_index(py_json)

    @staticmethod
    def deserialize(py_json: PyJSON) -> 'FeedVegetarianChoice':
        """ Deserialize the given value into a instance of this Serializer?
        :param py_json: A PyJSON value
        :return: An instance of this Deserializedb
        """
        return FeedVegetarianChoice(cast(Index, py_json))

    def __eq__(self, other):
        return isinstance(other, FeedVegetarianChoice) and \
               self.vegetarian_index == cast(FeedVegetarianChoice, other).vegetarian_index

    def __repr__(self):
        return "{}({})".format(name_of_class(self), self.vegetarian_index)

    @property
    def vegetarian_index(self) -> Index:
        """ The vegetarian index """
        return assert_set(self._vegetarian_index)

    @vegetarian_index.setter
    def vegetarian_index(self, vegetarian_index: Index) -> None:
        """ The vegetarian index """
        assert_type(vegetarian_index, of_type=Index, func_name="vegetarian_index")
        self._vegetarian_index = vegetarian_index


class StoreFatChoice(FeedingChoice):
    """ A Store Fat Choice """
    def __init__(self, species_index: Index, num_food_to_store: NaturalPlus) -> None:
        """ Store a number of food tokens as Fat for the Species at the given index
        :param species_index: The index of the Species
        :param num_food_to_store: The amount of food being stored
        """
        self._species_index = Unset      # type: Index
        self._num_food_to_store = Unset  # type: NaturalPlus

        self.species_index = species_index
        self.num_food_to_store = num_food_to_store

    def is_valid(self, dealer: IDealer, player: IPlayer) -> bool:
        """ Is this Store Fat Choice from the given player valid?
        :param dealer: The Dealer of the Game
        :param player: The Player whose response is being validated
        """
        species = player.species_list[self.species_index]
        return species.can_store(self.num_food_to_store)

    def apply(self, dealer: IDealer, player: IPlayer) -> None:
        """ Apply this Choice to given the dealers and the State of the Player who gave the dealers this?
        Effect: Modifies the Player and Dealer according to this Choice
        :param dealer: The dealers
        :param player: The Player's State
        """
        species = player.species_list[self.species_index]

        fat_to_store = 0
        for i in range(self.num_food_to_store):
            fat_to_store += dealer.grab_food_token_from_watering_hole()

        species.store_fat(fat_to_store)

    def to_data(self, feeding: Feeding) -> DataFeedingChoice:
        """ Convert this Feeding Choice into a Data Feeding Choice
        :param feeding: The Feeding
        :return: this as a Data Feeding Choice
        """
        fat_species = feeding.player.get_species_at_index(self.species_index)

        return DataStoreFat(fat_species, self.num_food_to_store)

    def serialize(self) -> PyJSON:
        """ Serialize this value into a its PyJSON equivalent?
        :return: The serialized JSON
        """
        return [self.species_index, self.num_food_to_store]

    @staticmethod
    def can_deserialize(py_json: PyJSON) -> bool:
        """ Can this Serializers deserialize the given PyJSON value?
        :param py_json: A PyJSON value
        :return: True if this can deserialize the given value, False otherwise
        """
        return is_list(py_json) and is_index(py_json[0]) and is_natural_plus(py_json[1])

    @staticmethod
    def deserialize(py_json: PyJSON) -> 'StoreFatChoice':
        """ Deserialize the given value into a instance of this Serializer?
        :param py_json: A PyJSON value
        :return: An instance of this Deserialized
        """
        return StoreFatChoice(*py_json)

    def __repr__(self):
        return "{}({}, {})".format(name_of_class(self), self.species_index, self.num_food_to_store)

    def __eq__(self, other):
        if not isinstance(other, StoreFatChoice):
            return False
        other_sf = cast(StoreFatChoice, other)
        return (self.species_index == other_sf.species_index and
                self.num_food_to_store == other_sf.num_food_to_store)

    @property
    def species_index(self) -> Index:
        """ The species index """
        return assert_set(self._species_index)

    @species_index.setter
    def species_index(self, species_index: Index) -> None:
        """ The species index """
        assert_type(species_index, of_type=Index, func_name="species_index")
        self._species_index = species_index

    @property
    def num_food_to_store(self) -> NaturalPlus:
        """ Get the number of food to store """
        return assert_set(self._num_food_to_store)

    @num_food_to_store.setter
    def num_food_to_store(self, num_food_to_store: NaturalPlus) -> None:
        """ Set the number of food to store """
        assert_type(num_food_to_store, of_type=NaturalPlus, func_name="num_food_to_store")
        self._num_food_to_store = num_food_to_store


class AttackWithCarnivoreChoice(FeedingChoice):
    """ An Attack with Carnivore Choice """
    def __init__(self, carnivore_index: Index, target_player_index: Index, target_species_index: Index) -> None:
        """ Construct an Attack with Carnivore to feed that Carnivore
        :param carnivore_index: The Index of your Carnivore
        :param target_player_index: The target external_players's id
        :param target_species_index: The target Species of the target external_players
        """
        self._carnivore_index = Unset       # type: Index
        self._target_player_index = Unset   # type: Index
        self._target_species_index = Unset  # type: Index

        self.carnivore_index = carnivore_index
        self.target_player_index = target_player_index
        self.target_species_index = target_species_index

    def is_valid(self, dealer: IDealer, player: IPlayer) -> bool:
        """ Is this Attack With Carnivore Choice from the given player valid?
        :param dealer: The Dealer of the Game
        :param player: The Player whose response is being validated
        """
        carnivore = player.species_list[self.carnivore_index]
        player_list = dealer.get_player_list_with_player_at_end(player)
        target_player = player_list[self.target_player_index]

        return carnivore.is_hungry and target_player.can_be_attacked_by(carnivore, self.target_species_index)

    def apply(self, dealer: IDealer, player: IPlayer) -> None:
        """ Apply this Choice to given the dealers and the State of the Player who gave the dealers this?
        Effect: Modifies the Player and Dealer according to this Choice
        :param dealer: The dealers
        :param player: The Player's State
        """
        carnivore = player.species_list[self.carnivore_index]
        player_list = dealer.get_player_list_with_player_at_end(player)
        target_player = player_list[self.target_player_index]

        carnivore.attack(player, self.carnivore_index, target_player, self.target_species_index, dealer.deck)
        if carnivore.is_extant:
            dealer.feed_species(self.carnivore_index, player)
            dealer.feed_scavengers()

    def to_data(self, feeding: Feeding) -> DataFeedingChoice:
        """ Convert this Feeding Choice into a Data Feeding Choice
        :param feeding: The Feeding
        :return: this as a Data Feeding Choice
        """
        carn_index = self.carnivore_index
        target_player_idx = self.target_player_index
        target_species_idx = self.target_species_index

        carnivore = feeding.player.get_species_at_index(carn_index)
        target_player = feeding.other_players[target_player_idx]
        target_species = target_player.get_species_at_index(target_species_idx)

        return DataAttackWithCarnivore(carnivore, target_player, target_species)

    def serialize(self) -> PyJSON:
        """ Serialize this value into a its PyJSON equivalent?
        :return: The serialized JSON
        """
        return [self.carnivore_index, self.target_player_index, self.target_species_index]

    @staticmethod
    def can_deserialize(py_json: PyJSON) -> bool:
        """ Can this Serializers deserialize the given PyJSON value?
        :param py_json: A PyJSON value
        :return: True if this can deserialize the given value, False otherwise
        """
        return is_list(py_json, of_type=Index, length=3)

    @staticmethod
    def deserialize(py_json: PyJSON) -> 'AttackWithCarnivoreChoice':
        """ Deserialize the given value into a instance of this Serializer?
        :param py_json: A PyJSON value
        :return: An instance of this Deserialized
        """
        return AttackWithCarnivoreChoice(*py_json)

    def __repr__(self):
        return "{}({},{},{})".format(name_of_class(self),
                                     self.carnivore_index,
                                     self.target_player_index,
                                     self.target_species_index)

    def __eq__(self, other):
        if not isinstance(other, AttackWithCarnivoreChoice):
            return False
        other_awc = cast(AttackWithCarnivoreChoice, other)
        return (self.carnivore_index == other_awc.carnivore_index and
                self.target_player_index == other_awc.target_player_index and
                self.target_species_index == other_awc.target_species_index)

    @property
    def carnivore_index(self) -> Index:
        """ The carnivore index """
        return assert_set(self._carnivore_index)

    @carnivore_index.setter
    def carnivore_index(self, carnivore_index: Index) -> None:
        """ The carnivore index """
        assert_type(carnivore_index, of_type=Index, func_name="carnivore_index")
        self._carnivore_index = carnivore_index

    @property
    def target_player_index(self) -> Index:
        """ Get the target player index """
        return assert_set(self._target_player_index)

    @target_player_index.setter
    def target_player_index(self, target_player_index: Index) -> None:
        """ Set the target player index """
        assert_type(target_player_index, of_type=Index, func_name="target_player_index")
        self._target_player_index = target_player_index

    @property
    def target_species_index(self) -> Index:
        """ Get the target species index """
        return assert_set(self._target_species_index)

    @target_species_index.setter
    def target_species_index(self, target_species_index: Index) -> None:
        """ Set the target species index """
        assert_type(target_species_index, of_type=Index, func_name="target_species_index")
        self._target_species_index = target_species_index
