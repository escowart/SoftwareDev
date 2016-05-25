from evo_json.convert_py_json.convert_species import *
from evolution.messages.player_messages.situation import *

"""----------- PyJSON Situation <-> Situation -----------"""


PJ_Situation = List[PyJSON]  # of format [PJ_Species, PJ_Species, PJ_OptSpecies, PJ_OptSpecies]


def is_pj_situation(value: Any) -> bool:
    """ Is the given value a PyJSON Situation
    :param value: The value being checked
    :return: True if the given value is a PyJSON Situation
    """
    return is_list(value, length=PJ_SIT_LEN)


def convert_from_py_situation(situation: PJ_Situation) -> Situation:
    """ Convert the given PyJSON Situation to a Situation
    :param situation: The given PyJSON Situation
    :return: The resulting Situation
    """
    if not is_pj_situation(situation):
        raise ValueError("convert_situation: Invalid PyJSON Situation, got: {}".format(situation))

    return Situation(defender=convert_from_pj_species(situation[0]),
                     attacker=convert_from_pj_species(situation[1]),
                     defender_left_neighbor=convert_from_pj_opt_species(situation[2]),
                     defender_right_neighbor=convert_from_pj_opt_species(situation[3]))


def convert_to_py_situation(situation: Situation) -> PyJSON:
    """ Convert the given Situation to a PyJSON Situation
    :param situation: The given Situation
    :return: The resulting PyJSON Situation

    Situation = [Species, Species, OptSpecies, OptSpecies]
    """
    if not isinstance(situation, Situation):
        raise ValueError("convert_situation: Invalid Situation, got: {}".format(situation))

    return [convert_to_pj_species(situation.attacker),
            convert_to_pj_species(situation.defender),
            convert_to_pj_opt_species(situation.defender_left_neighbor),
            convert_t0_pj_opt_species(situation.defender_right_neighbor)]
