from evo_json.convert_py_json.convert_player import *
from evolution.dealers.player_sequence import *

def is_pj_config(py_json: PyJSON) -> bool:
    """ Is the given PyJSON a Configuration?
    :param py_json: The PyJSON
    :return: True if the given PyJSON is a Configuration, False otherwise
    """
    return is_list(py_json, length=PJ_CONFIG_LEN)


def convert_from_pj_config(py_config: PyJSON) -> Configuration:
    """ Convert the given PyJSON Configuration into a evo Configuration
    :param py_config: The PyJSON Configuration
    :return: The Configuration
    """
    if not is_pj_config(py_config):
        raise ValueError("convert_from_pj_config: Invalid PyJSON Configuration, got: {}".format(py_config))

    return Configuration(PlayerSequence(convert_from_pj_lopp(py_config[0])),
                         WateringHole(py_config[1], []),
                         Deck(convert_from_pj_loc(py_config[2])))


def convert_to_pj_config(config: Configuration) -> PyJSON:
    """ Convert the given Configuration into a PyJSON Configuration
    :param config: The Configuration
    :return: The PyJSON Configuration
    """
    if not is_configuration(config):
        raise ValueError("convert_to_pj_config: Invalid Configuration, got: {}".format(config))

    return [convert_to_pj_lopp(config.player_sequence.player_list),
            config.watering_hole.num_food_tokens,
            convert_to_pj_loc(config.deck.cards)]

