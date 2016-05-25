from evo_json.convert_py_json.convert_player_fields import *
from evolution.external_players.silly.silly_player import *

"""----------- PyJSON SimplePlayer <-> PlayerState -----------"""

PJ_Player = List[PyJSON]  # [PJ_ID, PJ_LOS, PJ_Bag]


def is_pj_player(value: Any) -> bool:
    """ Is the given value a PJ_Player?
    :param value: The value being checked
    :return: True if the given value is a PJ_Player, False otherwise
    """
    return is_list(value, length=PJ_PLAYER_LEN)


def convert_from_pj_player(pj_player: PJ_Player) -> Player:
    """ Convert the given PJ_Player to a PlayerState
    :param pj_player: The PJ_Player
    :return: The PlayerState
    """
    if not is_pj_player(pj_player):
        raise ValueError("convert_from_pj_player: Invalid PyJSON SimplePlayer, got: {}".format(pj_player))
    player_id = convert_from_id(pj_player[0])
    player = Player(player_id=player_id,
                    species_list=convert_from_pj_player_species(pj_player[1]),
                    food_bag=convert_from_bag(pj_player[2]))

    player.external_player = SillyPlayer(player_id, player.player_configuration)
    return player


def convert_to_pj_player(player_state: Player) -> PJ_Player:
    """ Convert the given PlayerState to a PJ_Player
    :param player_state: The PlayerState
    :return: The PJ_Player
    """
    if not isinstance(player_state, Player):
        raise ValueError("convert_to_pj_player: Invalid PlayerState, got: {}".format(player_state))

    return [convert_to_pj_id(player_state.player_id),
            convert_to_pj_player_species(player_state.species_list),
            convert_to_pj_bag(player_state.food_bag)]


"""----------- PyJSON LOP <-> Listof[PlayerState] -----------"""

PJ_LOP = List[PJ_Player]


def is_pj_lop(value: Any):
    """ Is the given value a PJ_LOP
    :param value: The value being checked
    :return: True if the value is a PJ_LOP, False otherwise
    """
    return isinstance(value, list)


def convert_from_pj_lop(pj_lop: PJ_LOP) -> List[Player]:
    """ Convert the given PJ_LOP to a Listof[PlayerState]
    :param pj_lop: The PJ_LOP
    :return: The Listof[PlayerState]
    """
    if not is_pj_lop(pj_lop):
        raise ValueError("convert_from_pj_lop: Invalid PyJSON LOP, got: {}".format(pj_lop))

    return [convert_from_pj_player(pj_player) for pj_player in pj_lop]


def convert_to_pj_lop(player_states: List[Player]) -> PJ_LOP:
    """ Convert the given Listof[PlayerState] to a PJ_LOP
    :param player_states: The Listof[PlayerState]
    :return: The PJ_LOP
    """
    if not isinstance(player_states, list):
        raise ValueError("convert_species_plus_list: Invalid PyJSON LOS, got: {}".format(player_states))

    return [convert_to_pj_player(player_state) for player_state in player_states]


"""----------- PyJSON Player+ <-> Player -----------"""


def is_pj_player_plus(value: Any):
    """ Is the given value a PyJSON Player+?
    :param value: The value being checked
    :return: True if the given value is a PyJSON Player+, False otherwise
    """
    return is_list(value, with_len=PJ_PLAYER_PLUS_LEN)


def convert_from_pj_player_plus(pj_player: PyJSON) -> Player:
    """ Convert the given PyJSON Player+ to a Player
    :param pj_player: The PyJSON Player+ being converted
    :return: The Player

    Player+ = [id, species, bag, cards]
    """
    if is_list(pj_player, length=PJ_PLAYER_LEN):  # Is Normal Player
        return convert_from_pj_player(pj_player)
    elif not is_list(pj_player, length=PJ_PLAYER_PLUS_LEN):
        raise ValueError("convert_from_pj_player_plus: Invalid PyJSON Player+, got: {}".format(pj_player))

    player_id = convert_from_id(pj_player[0])
    player = Player(player_id=player_id,
                    species_list=convert_from_pj_player_species(pj_player[1]),
                    food_bag=convert_from_bag(pj_player[2]),
                    hand=convert_from_pj_cards(pj_player[3]))

    player.external_player = SillyPlayer(player_id, player.player_configuration)
    return player


def convert_to_pj_player_plus(player: Player) -> PyJSON:
    """ Convert the given Player to a PyJSON Player+
    :param player: The Player being converted
    :return: The PyJSON Player+


    Player+ = [id, species, bag, cards]
    """

    base_player = convert_to_pj_player(player)

    if not player.is_hand_empty:
        base_player.append(convert_to_pj_cards(player.hand))

    return base_player


"""----------- PyJSON LOP+ <-> Listof[PlayerState] -----------"""


def is_pj_lopp(value: Any):
    """ Is the given value a PyJSON Listof Player+?
    :param value: The value being checked
    :return: True if the given value is a PyJSON Listof Player+
    """
    return isinstance(value, list)


def convert_from_pj_lopp(py_lopp: PyJSON) -> List[Species]:
    """ Convert PyJSON LOS into a List of PlayerState
    :param py_lopp: The  PyJSON LOP+ being converted
    :return: The resulting List of Species
    """
    if not is_pj_lopp(py_lopp):
        raise ValueError("convert_from_pj_lopp: Invalid PyJSON LOP+, got: {}".format(py_lopp))

    return [convert_from_pj_player_plus(py_player_plus) for py_player_plus in py_lopp]


def convert_to_pj_lopp(player_plus_list: List[Player]) -> PyJSON:
    """ Convert List of Species into a PyJSON LOP+
    :param player_plus_list: The  List of PlayerState being converted
    :return: The resulting PyJSON PyJSON LOP+
    """
    if not is_list(player_plus_list, Player):
        raise ValueError("convert_to_pj_lopp: Invalid Listof[PlayerState], got: {}".format(player_plus_list))

    return [convert_to_pj_player_plus(player_plus) for player_plus in player_plus_list]
