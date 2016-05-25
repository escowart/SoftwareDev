import json
import sys

from evo_json.all_converters import *
from evolution.dealers.dealer import *
from old_exe.exe_util import *


def main(n: int) -> None:
    """ Main function for running the Evolution Game
    :param n: Number of Players
    :return:
    """
    player_sequence = []     # type: List[Player]
    for i in range(n):
        player = Player(i + 1, external_player_type=SillyPlayer)
        player_sequence.append(player)

    dealer = Dealer(PlayerSequence(player_sequence),
           WateringHole(0, []),
           Deck.create_deck())

    dealer.run_evolution()



