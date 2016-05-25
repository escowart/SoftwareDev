from evolution.messages.message import *
from evo_json.serializers.species_boards import *


class ChooseActionServerMessage(Message):
    """ A Server Choose Action """

    def __init__(self, before_boards: List[SpeciesBoards], after_boards: List[SpeciesBoards]) -> None:
        """ Construct a Server Choose Action
        :param before_boards: The before player species boards
        :param after_boards: The after player species boards
        """
        self._before_boards = Unset  # type: List[SpeciesBoards]
        self._after_boards = Unset   # type: List[SpeciesBoards]

        self.before_boards = before_boards
        self.after_boards = after_boards

    def serialize(self) -> PyJSON:
        """ Serialize this value into a its PyJSON equivalent?
        :return: The serialized JSON
        """
        return [serialize_list(self.before_boards), serialize_list(self.after_boards)]

    @staticmethod
    def can_deserialize(py_json: PyJSON) -> bool:
        """ Can this Serializers deserialize the given PyJSON value?
        :param py_json: A PyJSON value
        :return: True if this can deserialize the given value, False otherwise
        """
        return (len(py_json) == SERVER_CHOOSE_ACTION_LEN) and \
            all(can_deserialize_list(SpeciesBoards, boards_list) for boards_list in py_json)

    @staticmethod
    def deserialize(py_json: PyJSON) -> 'ChooseActionServerMessage':
        """ Deserialize the given value into a instance of this Serializer?
        :param py_json: A PyJSON value
        :return: An instance of this Deserialized
        """
        return ChooseActionServerMessage(*[deserialize_list(SpeciesBoards, boards_list) for boards_list in py_json])

    @property
    def player_before_after_config_lists(self) -> Tuple[List[PlayerConfiguration], List[PlayerConfiguration]]:
        """ Get the before and after Player Configuration lists """
        return [species_boards_list_to_player_configs(self.before_boards),
                species_boards_list_to_player_configs(self.after_boards)]

    @staticmethod
    def make_from_player_configs(before_configs: List[PlayerConfiguration],
                                 after_configs: List[PlayerConfiguration]) -> 'ChooseActionServerMessage':
        """ Make a server choose action from player configuration
        :param before_configs: The before player configurations
        :param after_configs: The after player configurations
        :return: The ServerChooseAction
        """
        return ChooseActionServerMessage(player_configs_to_species_boards_list(before_configs),
                                         player_configs_to_species_boards_list(after_configs))

    @property
    def before_boards(self) -> List[SpeciesBoards]:
        """ Get the Before Boards """
        return assert_set(self._before_boards)

    @before_boards.setter
    def before_boards(self, before_boards: List[SpeciesBoards]) -> None:
        """ Set the Before Boards """
        assert_type(before_boards, list, of_type=SpeciesBoards, func_name="before_boards")
        self._before_boards = before_boards

    @property
    def before_player_configs(self) -> List[PlayerConfiguration]:
        """ Get the before player configurations """
        return species_boards_list_to_player_configs(self.before_boards)

    @before_player_configs.setter
    def before_player_configs(self, before_player_configs: List[PlayerConfiguration]) -> None:
        """ Set the before player configurations """
        assert_type(before_player_configs, list, of_type=PlayerConfiguration, func_name="before_player_configs")
        self.before_boards = player_configs_to_species_boards_list(before_player_configs)

    @property
    def after_boards(self) -> List[SpeciesBoards]:
        """ Get the After Boards """
        return assert_set(self._after_boards)

    @after_boards.setter
    def after_boards(self, after_boards: List[SpeciesBoards]) -> None:
        """ Set the After Boards """
        assert_type(after_boards, list, of_type=SpeciesBoards, func_name="after_boards")
        self._after_boards = after_boards

    @property
    def after_player_configs(self) -> List[PlayerConfiguration]:
        """ Get the after player configurations """
        return species_boards_list_to_player_configs(self.after_boards)

    @after_player_configs.setter
    def after_player_configs(self, after_player_configs: List[PlayerConfiguration]) -> None:
        """ Set the after player configurations """
        assert_type(after_player_configs, list, of_type=PlayerConfiguration, func_name="after_player_configs")
        self.after_boards = player_configs_to_species_boards_list(after_player_configs)

    def __repr__(self) -> str:
        return "{}(before={}, after={})".format(name_of_class(self), self.before_boards, self.after_boards)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, ChooseActionServerMessage) and \
               (self.before_boards == cast(ChooseActionServerMessage, other).before_boards) and \
               (self.after_boards == cast(ChooseActionServerMessage, other).after_boards)
