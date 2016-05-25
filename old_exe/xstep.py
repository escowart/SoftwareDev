import json
import sys

from evo_json.convert_py_json.convert_config import *
from evolution.dealers.dealer import Dealer


def main():
    process_json_configuration(sys.stdin, sys.stdout)


def process_json_configuration(file_in, file_out,):
    """ Process evolution according to HW-8 Specs
    :param file_in: In file
    :param file_out: Out file
    """
    py_json_config = json.load(file_in)

    try:
        in_config = convert_from_pj_config(py_json_config)
        dealer = Dealer(*in_config)
    except Exception as e:
        raise e

    try:
        player = dealer.player_sequence[DEFAULT_START_INDEX]
        player.external_player = SillyPlayer(player.player_id, player.player_configuration)
        if (not dealer.is_watering_hole_empty) and dealer.can_player_feed_or_store(player):
            choice = player.choose_feeding(dealer)

            if choice != InvalidFeedingChoice:
                dealer.feed1(player, choice)

            out_config = dealer.configuration
        else:
            out_config = in_config

        pj_config = convert_to_pj_config(out_config)
        json.dump(pj_config, file_out)
    except Exception as e:
        raise e






