from evo_tests.examples.ex_messages import *
from client import *
import unittest

class TestMessages(unittest.TestCase):

    def _test_serializer(self,
                         serializer_type:    type(Serializer),
                         deserialized_value: Serializer,
                         serialized_value:   PyJSON) -> None:
        """ Test the given serializer type with a deserialized value and serialized value
        :param serializer_type: The type of Serializer being tested
        :param deserialized_value: The value Deserialized
        :param serialized_value: The value Serialized
        """
        self.assertEqual(deserialized_value.serialize(), serialized_value)
        self.assertTrue(serializer_type.can_deserialize(serialized_value))
        self.assertEqual(serializer_type.deserialize(serialized_value), deserialized_value)

    def setUp(self) -> None:
        self.ex_messages = ExampleMessages()

    def test_species_boards(self) -> None:
        self._test_serializer(SpeciesBoards,
                              self.ex_messages.species_boards_norm,
                              self.ex_messages.species_boards_norm_serial)

    def test_player_state(self) -> None:
        self._test_serializer(PlayerState,
                              self.ex_messages.player_state_norm,
                              self.ex_messages.player_state_norm_serial)

    def test_game_state(self) -> None:
        self._test_serializer(GameState,
                              self.ex_messages.game_state_norm,
                              self.ex_messages.game_state_norm_serial)

        py_json = self.ex_messages.game_state_norm_serial
        self.assertEqual(len(py_json), PJ_GAME_STATE_LEN)
        self.assertTrue(is_natural(py_json[3]))
        self.assertTrue(all(SpeciesBoards.can_deserialize(other_player_board) for other_player_board in py_json[4]))

    def test_action(self) -> None:
        action1_deserialized = Action(FoodCardChoice(0), [], [], [], [])
        action1_serialized = [0,[],[],[],[]]

        self._test_serializer(Action, action1_deserialized, action1_serialized)

    def test_boards(self) -> None:
        gain_board_min = GainBoard(1, [])
        gain_board_min_serial = [1]
        gain_board_max = GainBoard(1, [2, 3, 4])
        gain_board_max_serial = [1, 2, 3, 4]

        self._test_serializer(GainBoard, gain_board_min, gain_board_min_serial)
        self._test_serializer(GainBoard, gain_board_max, gain_board_max_serial)

    def test_full_action(self):
        action_d = Action(FoodCardChoice(3), [GainPopulation(1, 0)], [GainBody(1, 5)], [GainBoard(2, [1])],
                          [ReplaceTrait(1, 0, 4)])
        action_s = [3, [[1, 0]], [[1, 5]], [[2, 1]], [[1, 0, 4]]]
        self.assertTrue(is_list(action_s, length=PJ_ACTION4_LEN) )
        self.assertTrue(FoodCardChoice.can_deserialize(action_s[0]))
        self.assertTrue(GainPopulation.can_deserialize(action_s[1][0]))
        self.assertTrue(can_deserialize_list(GainPopulation, action_s[1]))
        self.assertTrue(can_deserialize_list(GainBody, action_s[2]))
        self.assertTrue(can_deserialize_list(GainBoard, action_s[3]))
        self.assertTrue(can_deserialize_list(ReplaceTrait, action_s[4]))
        self._test_serializer(Action, action_d, action_s)

    def test_store_fat(self):
        store_fat_s = [1, 1]
        store_fat_d = StoreFatChoice(1, 1)
        self._test_serializer(StoreFatChoice, store_fat_d, store_fat_s)


class TestSocketHolder(unittest.TestCase):

    def setUp(self):
        psuedo_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_holder = MessageSocket(psuedo_socket)

    def _test_stored_and_next_data(self, stored_data: str, next_py_json_sequence: List[PyJSON]) -> None:
        """ Test both collected data and the sequence of PyJSON
        :param stored_data: The added data to collected data
        :param next_py_json_sequence: The sequence of next py jsons
        """
        self.socket_holder.collected_data += stored_data

        for next_py_json in next_py_json_sequence:
            self.assertEqual(self.socket_holder.next_py_json(), next_py_json)

    def test_simple_next_py_json(self):
        stored_data = "5"
        next_py_json = 5

        self._test_stored_and_next_data(stored_data, [next_py_json, InvalidPyJSON])

    def test_complex_next_py_json(self):
        stored_data = "5[6, 45]"
        py_json_5 = 5
        py_json_hello = [6, 45]

        self._test_stored_and_next_data(stored_data, [py_json_5, py_json_hello, InvalidPyJSON])




