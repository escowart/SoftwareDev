from evolution.messages.player_messages.action_choice import *


def is_pj_food_card_index(value: Any) -> bool:
    """ Is the given value a PJ Food Card index?"""
    return is_index(value)


def convert_food_card_index(food_card_index: Index) -> FoodCardChoice:
    """ Convert from a Food Card Index to a Choice Food Card """
    return FoodCardChoice(food_card_index)


def is_pj_gp(value: Any) -> bool:
    """ Is the given value a PJ Gain Population?"""
    return is_list(value, length=PJ_GP_AND_GB_LEN) and (value[0] == POP_STR) \
           and is_index(value[1]) and is_index(value[2])


def convert_from_pj_gp(pj_gp: PyJSON) -> GainPopulation:
    """ Convert from a PJ Gain Population to Gain Population """
    if not is_pj_gp(pj_gp):
        raise ValueError("convert_from_pj_gp: Must be PJ Gain Population, got: {}".format(pj_gp))

    return GainPopulation(pj_gp[1], pj_gp[2])


def convert_to_pj_gp(gain_pop: GainPopulation) -> PyJSON:
    """ Convert from a Gain Population to PJ Gain Population """
    if not isinstance(gain_pop, GainPopulation):
        raise ValueError("convert_to_pj_gp: Must be Gain Population, got: {}".format(gain_pop))

    return [POP_STR, gain_pop.species_index, gain_pop.card_index]


def is_pj_gb(value: Any) -> bool:
    """ Is the given value a PJ Gain Body?"""
    return is_list(value, length=PJ_GP_AND_GB_LEN) and (value[0] == BODY_STR) \
           and is_index(value[1]) and is_index(value[2])


def convert_from_pj_gb(pj_gb: PyJSON) -> GainBody:
    """ Convert from a PJ Gain Body to Gain Body """
    if not is_pj_gb(pj_gb):
        raise ValueError("convert_from_pj_gb: Must be PJ Gain Body, got: {}".format(pj_gb))

    return GainBody(pj_gb[1], pj_gb[2])


def convert_to_pj_gb(gain_body: GainBody) -> PyJSON:
    """ Convert from a Gain Body to PJ Gain Body """
    if not isinstance(gain_body, GainBody):
        raise ValueError("convert_to_pj_gb: Must be GainBody, got: {}".format(gain_body))

    return [BODY_STR, gain_body.species_index, gain_body.card_index]

def is_pj_bt(value: Any) -> bool:
    """ Is the given value a PJ Board Trade? """
    return is_list(value, of_type=Index, min_len=MIN_PJ_BT_LEN, max_len=MAX_PJ_BT_LEN)


def convert_from_pj_bt(pj_bt: PyJSON) -> GainBoard:
    """ Convert from a PJ Board Trade to Gain Board """
    if not is_pj_bt(pj_bt):
        raise ValueError("convert_from_pj_bt: Must be PJ Board Trade, got: {}".format(pj_bt))

    return GainBoard(pj_bt[0], pj_bt[1:])


def convert_to_pj_bt(gain_board: GainBoard) -> PyJSON:
    """ Convert from a Gain Board to PJ Gain Board """
    if not isinstance(gain_board, GainBoard):
        raise ValueError("convert_to_pj_bt: Must be GainBoard, got: {}".format(gain_board))

    return [gain_board.card_index] + gain_board.trait_indices


def is_pj_rt(value: Any) -> bool:
    """ Is the given value a PJ Replace Trait? """
    return is_list(value, of_type=Index, length=PJ_RT_LEN)


def convert_from_pj_rt(pj_rt: PyJSON) -> ReplaceTrait:
    """ Convert from a PJ Board Trade to Gain Board """
    if not is_pj_rt(pj_rt):
        raise ValueError("convert_from_pj_rt: Must be PJ Replace Trait, got: {}".format(pj_rt))

    return ReplaceTrait(*pj_rt)


def convert_to_pj_rt(replace_trait: ReplaceTrait) -> PyJSON:
    """ Convert from a Replace Trait to PJ Replace Trait """
    if not isinstance(replace_trait, ReplaceTrait):
        raise ValueError("convert_to_pj_rt: Must be ReplaceTrait, got: {}".format(replace_trait))

    return [replace_trait.species_index, replace_trait.trait_index, replace_trait.card_index]




