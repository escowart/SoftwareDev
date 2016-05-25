from evo_json.convert_py_json.convert_config import *
from evo_json.convert_py_json.convert_action_choices import *


def is_pj_config_and_step4(py_json: PyJSON) -> bool:
    """ Is the given PyJSON an Step4?
    :param py_json: The PyJSON
    :return: True if the given PyJSON is an Step4, False otherwise
    """
    return is_list(py_json, length=PJ_STEP4_CONFIG_LEN)


def convert_from_pj_config_and_step4(config_and_step4: PyJSON) -> Tuple[Configuration, List[Action]]:
    """ Convert the given PyJSON Step4 and Configuration to a tuple of List[Actions] and Configuration
    :param config_and_step4: The PyJSON Configuration and Step4
    :return: The Configuration and the List of Actions
    """
    if not is_pj_config_and_step4(config_and_step4):
        raise ValueError("convert_from_pj_step4: Invalid PyJSON Step4 and Configuration, got: {}"
                         .format(config_and_step4))

    return (convert_from_pj_config(config_and_step4[0]), convert_from_pj_step4(config_and_step4[1]))


def is_pj_step4(py_json: PyJSON) -> bool:
    """ Is the given PyJSON an Step4?
    :param py_json: The PyJSON
    :return: True if the given PyJSON is an Step4, False otherwise
    """
    return is_list(py_json)


def convert_from_pj_step4(step4: PyJSON) -> List[Action]:
    """ Convert the given PyJSON Step4 into a List of Actions
    :param step4: The PyJSON Configuration
    :return: The List of Actions
    """
    if not is_pj_step4(step4):
        raise ValueError("convert_from_pj_step4: Invalid PyJSON Step4, got: {}".format(step4))
    return [convert_from_pj_action4(action4) for action4 in step4]


def is_pj_action4(py_json: PyJSON) -> bool:
    """ Is the given PyJSON an Action4?
    :param py_json: The PyJSON
    :return: True if the given PyJSON is an Action4, False otherwise
    """
    return is_list(py_json, length=PJ_ACTION4_LEN)


def convert_from_pj_action4(action4: PyJSON) -> Action:
    """ Convert the given PyJSON Action4 into a Actions
    :param action4: The PyJSON Configuration
    :return: The Actions
    """
    if not is_pj_action4(action4):
        raise ValueError("convert_from_pj_action4: Invalid PyJSON Action4, got: {}".format(action4))

    return Action(convert_food_card_index(action4[0]),
                  [convert_from_pj_gp(gp) for gp in action4[1]],
                  [convert_from_pj_gb(gb) for gb in action4[2]],
                  [convert_from_pj_bt(bt) for bt in action4[3]],
                  [convert_from_pj_rt(rt) for rt in action4[4]])


def convert_to_pj_action4(action: Action) -> PyJSON:
    """ Convert the given PyJSON Action into a Action4
    :param action: The Action
    :return: The Action4
    """
    if not isinstance(action, Action):
        raise ValueError("convert_to_pj_action4: Invalid Action, got: {}".format(action))

    return [action.food_card_choice.card_index,
           [convert_to_pj_gp(gp) for gp in action.gain_population_list],
           [convert_to_pj_gb(gb) for gb in action.gain_body_list],
           [convert_to_pj_bt(bt) for bt in action.gain_board_list],
           [convert_to_pj_rt(rt) for rt in action.replace_trait_list]]

