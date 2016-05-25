from evo_json.convert_py_json.convert_species import *
from evo_json.serializers.py_json_serializers import *


def serialize_player_config(player_config: PlayerConfiguration) -> PyJSON:
    """ Serialize the given PlayerConfigurations into PyJSON
    :param player_config: The Player Configurations
    :return: The serialized PyJSON
    """
    species_boards = SpeciesBoards.from_player_configuration(player_config)
    return species_boards.serialize()


def serialize_player_config_list(player_configs: List[PlayerConfiguration]) -> PyJSON:
    """ Serialize the given list of PlayerConfigurations into PyJSON
    :param player_configs: The list of Player Configurations
    :return: The serialized PyJSON
    """
    return [serialize_player_config(player_config) for player_config in player_configs]


def deserialize_to_player_config(py_json: PyJSON) -> PlayerConfiguration:
    """ Deserialize the given PyJSON into a PlayerConfiguration
    :param py_json: The PyJSON
    :return: The Player Configuration
    """
    species_boards = SpeciesBoards.deserialize(py_json)
    return species_boards.to_player_configuration()


def deserialize_to_player_config_list(py_json: PyJSON) -> List[PlayerConfiguration]:
    """ Deserialize the given PyJSON into a PlayerConfiguration
    :param py_json: The PyJSON
    :return: The Player Configuration
    """
    return [deserialize_to_player_config(pj_boards) for pj_boards in py_json]


def player_configs_to_species_boards_list(player_configs: List[PlayerConfiguration]) -> List['SpeciesBoards']:
    """ Convert the Player Configurations to a List of SpeciesBoards
    :param player_configs: The player Configurations
    :return: The SpeciesBoards list
    """
    return [SpeciesBoards.from_player_configuration(player_config) for player_config in player_configs]


def species_boards_list_to_player_configs(species_boards_list: List['SpeciesBoards']) -> List[PlayerConfiguration]:
    """ Convert the List of SpeciesBoards to Player Configurations
    :param species_boards_list: The SpeciesBoards list
    :return: The player Configurations
    """
    return [species_boards.to_player_configuration() for species_boards in species_boards_list]


class SpeciesBoards(Serializer):
    """ A class representing a Species Board in the Remote Protocol """

    def __init__(self, species_list: List[Species]):
        """ Construct a Species Boards
        :param species_list: The List of Species
        """
        self._species_list = Unset  # type: List[Species]

        self.species_list = species_list

    @staticmethod
    def can_deserialize(py_json_val: PyJSON) -> bool:
        """ Can this Serializers deserialize the given PyJSON value?
        :param py_json_val: A PyJSON value
        :return: True if this can deserialize the given value, False otherwise
        """
        try:
            [convert_from_pj_species_plus(pj_species) for pj_species in py_json_val]
            return True
        except ValueError:
            return False

    def serialize(self) -> PyJSON:
        """ Serialize this value into a its PyJSON equivalent?
        :return: The serialized JSON
        """
        return [convert_to_pj_species_plus(species) for species in self.species_list]

    @staticmethod
    def deserialize(py_json_val: PyJSON) -> 'SpeciesBoards':
        """ Deserialize the given value into a instance of this Serializer?
        :param py_json_val: A PyJSON value
        :return: An instance of this Deserialized
        """
        return SpeciesBoards([convert_from_pj_species_plus(pj_species) for pj_species in py_json_val])

    def to_player_configuration(self) -> PlayerConfiguration:
        """ Convert these Boards into a Player Configuration """
        return PlayerConfiguration(NO_ID, self.species_list, 0, [])

    @staticmethod
    def from_player_configuration(player_config: PlayerConfiguration) -> 'SpeciesBoards':
        """ Convert the given Player Configuration into a Species Board
        :param player_config: The Player Configuration
        :return: The resulting Species Boards
        """
        return SpeciesBoards(player_config.species_list)

    @property
    def species_list(self) -> List[Species]:
        """ Get the list of Species """
        return assert_set(self._species_list)

    @species_list.setter
    def species_list(self, species_list: List[Species]) -> None:
        """ Set the list of Species """
        assert_type(species_list, list, of_type=Species, func_name="species_list")
        self._species_list = species_list

    def __repr__(self) -> str:
        return "{}(species_list={})".format(name_of_class(self), self.species_list)

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, SpeciesBoards) and
                (self.species_list == cast(SpeciesBoards, other).species_list))