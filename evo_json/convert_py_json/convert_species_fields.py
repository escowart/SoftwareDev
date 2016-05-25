from evo_json.convert_py_json.convert_trait import *

"""----------- PyJSON Species food field <-> Natural -----------"""


PJ_Food = List[PyJSON] # of the format ["food", Natural]


def is_pj_food(value: Any):
    """ Is the given value a PyJSON Food?
    :param value: The value being checked
    :return: True the given value a PyJSON Food, False otherwise
    """
    return is_list(value, length=PJ_FIELD_LEN) and (value[0] == FOOD_STR) and is_natural(value[1])


def convert_from_pj_food(pj_food: PJ_Food) -> Natural:
    """ Convert the given PyJSON Food int a Natural
    :param pj_food: The PyJSON Food being converted
    :return: The resulting Natural
    """
    if not is_pj_food(pj_food):
        raise ValueError("convert_from_pj_food: Invalid PyJSON Food: {}".format(pj_food))

    return pj_food[1]


def convert_to_pj_food(food_nat: Natural) -> PJ_Food:
    """ Convert the given Natural into a PyJSON food
    :param food_nat: The Natural
    :return: The PyJSON Food

    food = [\"food\", Natural]
    """
    if not (is_natural(food_nat)):
        raise ValueError("convert_to_pj_food: Invalid Natural, got: {}".format(food_nat))

    return ["food", food_nat]


"""----------- PyJSON Species body field <-> Natural -----------"""


PJ_Body = List[PyJSON] # of format ["body", Natural]


def is_pj_body(value: Any):
    """ Is the given value a PyJSON Body?
    :param value: The value being checked
    :return: True the given value a PyJSON Body, False otherwise
    """
    return is_list(value, length=PJ_FIELD_LEN) and (value[0] == BODY_STR) and is_natural(value[1])


def convert_from_pj_body(pj_body: PJ_Body) -> Natural:
    """ Convert the given PyJSON Body into a Natural
    :param pj_body: The PyJSON Body being converted
    :return: The resulting Natural
    """
    if not is_pj_body(pj_body):
        raise ValueError("convert_from_pj_body: Invalid PyJSON Body, got: {}".format(pj_body))

    return pj_body[1]


def convert_to_pj_body(body_nat: Natural) -> PJ_Body:
    """ Convert the given Natural into a PyJSON Body
    :param body_nat: The Natural
    :return: PyJSON Body
    """
    if not (is_natural(body_nat)):
        raise ValueError("convert_to_pj_body: Invalid Natural, got: " + repr(body_nat))

    return [BODY_STR, body_nat]


"""----------- PyJSON Species population field <-> Natural -----------"""


PJ_Pop = List[PyJSON] # of format ["body", Natural]


def is_pj_pop(value: Any):
    """ Is the given value a PyJSON Population?
    :param value: The value being checked
    :return: True the given value a PyJSON Population, False otherwise
    """
    return is_list(value, length=PJ_FIELD_LEN) and (value[0] == POP_STR) and is_natural(value[1])


def convert_from_pj_pop(pj_pop: PJ_Pop) -> Natural:
    """ Convert the given PyJSON Population into a Natural
    :param pj_pop: The PyJSON Population being converted
    :return: The Natural
    """
    if not is_pj_pop(pj_pop):
        raise ValueError("convert_from_pj_population: Invalid PyJSON Population, got: {}".format(pj_pop))

    return pj_pop[1]


def convert_to_pj_pop(pop_nat: Natural) -> PJ_Pop:
    """ Convert the given Natural into a PyJSON Population
    :param pop_nat: The Natural being converted
    :return: The PyJSON Population
    """
    if not is_natural(pop_nat):
        raise ValueError("convert_to_pj_population: Invalid Natural, got: {}".format(pop_nat))

    return [POP_STR, pop_nat]


"""----------- PyJSON Species traits field <-> Listof[TraitCard] -----------"""


PJ_Traits = List[PyJSON] # of format ["traits", PJ_LOT]


def is_pj_traits(value: Any):
    """ Is the given value a PyJSON Traits?
    :param value: The value being checked
    :return: True the given value a PyJSON Traits, False otherwise
    """
    return is_list(value, length=PJ_FIELD_LEN) and (value[0] == TRAITS_STR) and is_pj_lot(value[1])


def convert_from_pj_traits(pj_traits: PJ_Traits) -> List[TraitCard]:
    """ Convert the given PyJSON Traits to a List of TraitCards
    :param pj_traits: The PyJSON Traits being converted
    :return: The resulting List of TraitCards
    """
    if not is_pj_traits(pj_traits):
        raise ValueError("convert_traits: Invalid PyJSON Traits, got: {}".format(pj_traits))

    return convert_from_pj_lot(pj_traits[1])


def convert_to_pj_traits(traits_list: List[TraitCard]) -> PJ_Traits:
    """ Convert the given List of TraitCards to a PyJSON Traits
    :param traits_list: The List of TraitCards traits being converted
    :return: The resulting PyJSON Traits
    """
    if not is_list(traits_list, TraitCard):
        raise ValueError("convert_traits: Invalid Listof[TraitCard], got: {}".format(traits_list))

    return [TRAITS_STR, convert_to_pj_lot(traits_list)]


"""----------- PyJSON Species fat-food field <-> Natural -----------"""


PJ_Fat_Food = List[PyJSON]  # of format ["fat-food", Natural]


def is_pj_fat_food(value: Any):
    """ Is the given value a PyJSON Fat-Food?
    :param value: The value being checked
    :return: True the given value a PyJSON Fat-Food, False otherwise
    """
    return is_list(value, length=PJ_FIELD_LEN) and (value[0] == FAT_FOOD_STR) and is_natural(value[1])


def convert_from_pj_fat_food(pj_fat_food: PJ_Fat_Food) -> Natural:
    """ Convert the given PyJSON Fat-Food to a Natural
    :param pj_fat_food: The PyJSON Fat-Food being converted
    :return: The resulting Natural
    """
    if not is_pj_fat_food(pj_fat_food):
        raise ValueError("convert_fat_food: Invalid PyJSON Fat-Food, got: {}".format(pj_fat_food))


    return pj_fat_food[1]


def convert_to_pj_fat_food(fat_food_nat: Natural) -> PJ_Fat_Food:
    """ Convert the given Natural to a PyJSON PJ_Fat_Food
    :param fat_food_nat: The Natural being converted
    :return: The resulting PyJSON PJ_Fat_Food

    fat-food = [\"fat-food\", Natural]
    """
    if not is_natural(fat_food_nat):
        raise ValueError("convert_fat_food: Invalid Natural], got: {}".format(fat_food_nat))

    return [FAT_FOOD_STR, fat_food_nat]
