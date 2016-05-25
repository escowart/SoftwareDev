import sys
import json
from typing import Optional
from evo_json.convert_py_json.convert_feeding import *
from evolution.all_evo import *


def main():
    process_json_feeding_7(sys.stdin, sys.stdout)


def process_json_feeding_6(file_in, file_out):
    """ Process evolution according to HW-6 Specs """
    py_json_in = json.load(file_in)
    try:
        feeding = convert_from_pj_feeding(py_json_in)  # type: Feeding
    except Exception as e:
        # Error converting the PyJSON to a evolution; ill formed
        return

    silly_player = SillyPlayer(feeding.player.player_id, feeding.player.player_configuration)
    other_players = [player.player_configuration for player in feeding.other_players]
    feeding_choice = silly_player.choose_feeding(feeding.watering_hole, other_players)
    data_feeding_choice = NoDataFeedingChoice if feeding_choice == InvalidFeedingChoice else feeding_choice.to_data(feeding)

    if data_feeding_choice != NoDataFeedingChoice:
        py_json_out = convert_feeding_choice_to_pj(data_feeding_choice)   # type: PyJSON
        json.dump(py_json_out, file_out)


def process_json_feeding_7(file_in, file_out):
    """ Process evolution according to HW-7 Specs """
    py_json_in = json.load(file_in)
    try:
        feeding = convert_from_pj_feeding(py_json_in)  # type: Feeding
    except Exception as e:
        # Error converting the PyJSON to a evolution; ill formed
        return

    player = SillyPlayer(feeding.player.player_id, feeding.player.player_configuration)
    other_players = [player.player_configuration for player in feeding.other_players]
    feeding_choice = player.choose_feeding(feeding.watering_hole, other_players)

    if feeding_choice != InvalidFeedingChoice:
        py_json_out = convert_player_feeding_choice_to_pj(feeding_choice)   # type: PyJSON
        json.dump(py_json_out, file_out)

if __name__ == "__main__":
    main()
