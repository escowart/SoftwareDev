from evo_json.convert_py_json.convert_step4 import *

Choice = namedtuple('Choice', ['player_id', 'player_configuration', 'before_players', 'after_players'])

def is_pj_choice(py_json: PyJSON) -> bool:
    """ Is the given PyJSON a Choice?
    :param py_json: The PyJSON
    :return: True if the given PyJSON is an Action4, False otherwise
    """
    return is_list(py_json, length=PJ_CHOICE_LEN)


def convert_from_pj_choice(pj_choice: PyJSON) -> Choice:
    """ Convert the given PyJSON Choice into a Choice
    :param choice: The PyJSON Choice
    :return: The Choice
    """
    if not is_pj_choice(pj_choice):
        raise ValueError("convert_from_pj_action4: Invalid PyJSON Choice, got: {}".format(pj_choice))

    player = convert_from_pj_player_plus(pj_choice[0])
    return Choice(player.player_id,
                  player.player_configuration,
                  [convert_from_pj_los_to_player_config(pj_los) for pj_los in pj_choice[1]],
                  [convert_from_pj_los_to_player_config(pj_los) for pj_los in pj_choice[2]])

NO_ID = 0

def convert_from_pj_los_to_player_config(pj_species_list: PyJSON):
    """ Convert the given List of PyJSON Species+ into a PlayerConfiguration
    :param pj_species_list: The PyJSON List of Species+
    :return: The Player Configuration
    """
    return PlayerConfiguration(NO_ID, convert_from_pj_los(pj_species_list), NO_FOOD_TOKENS, [])