import json
import sys

from evo_json.all_converters import *
from evolution.dealers.dealer import Dealer


def main():
    process_json_silly_choice(sys.stdin, sys.stdout)


def process_json_silly_choice(file_in, file_out):
    """ Process evolution according to HW-12 Specs """
    try:
        py_json_in = json.load(file_in)
        choice = convert_from_pj_choice(py_json_in)
        silly_player = SillyPlayer(choice.player_id, choice.player_configuration)
        action = silly_player.choose_action(choice.before_players, choice.after_players)
        py_json_out = convert_to_pj_action4(action)
        json.dump(py_json_out, file_out)
    except Exception as e:
        return
        #raise e





